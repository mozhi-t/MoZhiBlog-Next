<template>
  <div class="space-page">
    <header class="page-header">
      <h1 class="page-title">空间</h1>
      <p class="page-description">记录一些日常碎碎念、瞬间想法和零散片段。</p>
    </header>

    <div v-if="initialLoading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <div v-else-if="monthGroups.length" class="timeline-group-list">
      <section
        v-for="group in monthGroups"
        :key="group.key"
        class="month-group"
        :class="{ 'is-expanded': expandedMonths.includes(group.key) }"
      >
        <button
          class="month-header"
          :class="{ expanded: expandedMonths.includes(group.key) }"
          @click="toggleMonth(group.key, $event)"
        >
          <span
            v-if="rippleStates[group.key]"
            :key="rippleStates[group.key].id"
            class="month-header-ripple"
            :style="{
              left: `${rippleStates[group.key].x}px`,
              top: `${rippleStates[group.key].y}px`
            }"
          ></span>
          <div class="month-header-main">
            <span class="month-title">{{ group.label }}</span>
          </div>
          <svg class="expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M6 9l6 6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>

        <Transition
          @before-enter="onAccordionBeforeEnter"
          @enter="onAccordionEnter"
          @after-enter="onAccordionAfterEnter"
          @before-leave="onAccordionBeforeLeave"
          @leave="onAccordionLeave"
          @after-leave="onAccordionAfterLeave"
        >
          <div v-if="expandedMonths.includes(group.key)" class="timeline-shell">
            <div class="timeline">
              <article
                v-for="(moment, index) in group.items"
                :key="moment.id"
                class="timeline-item"
                :style="{ '--item-delay': `${Math.min(index, 8) * 70}ms` }"
              >
                <div class="timeline-meta">
                  <span class="timeline-date">{{ formatDay(moment.create_time) }}</span>
                  <span class="timeline-time">{{ formatTime(moment.create_time) }}</span>
                </div>

                <div class="timeline-card">
                  <div v-if="moment.need_password" class="timeline-card-head">
                    <span class="lock-badge">加密</span>
                  </div>

                  <div v-if="moment.need_password" class="locked-state">
                    <p>这条说说已加密，输入密码后可查看内容。</p>
                    <button class="unlock-btn" @click="openPasswordModal(moment.id)">输入密码</button>
                  </div>

                  <p v-else class="timeline-content">{{ moment.content }}</p>

                  <div class="timeline-footer">
                    <span>发布于 {{ formatFull(moment.create_time) }}</span>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </Transition>
      </section>

      <div ref="loadMoreTrigger" class="load-more-trigger" aria-hidden="true"></div>

      <div v-if="loadingMore" class="loading-more-state">
        <div class="loading-spinner small"></div>
        <span>正在加载更多说说...</span>
      </div>

      <button
        v-else-if="hasMore"
        class="load-more-btn"
        @click="loadMoreMoments"
      >
        加载更多
      </button>
    </div>

    <div v-else class="empty-tip">还没有说说内容。</div>

    <section class="comments-section">
      <h2 class="comments-title">评论</h2>
      <div id="twikoo-container">
        <div id="tcomment"></div>
      </div>
    </section>

    <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
      <div class="password-modal">
        <div class="modal-header">
          <h2>查看加密说说</h2>
          <button class="close-btn" @click="closePasswordModal">×</button>
        </div>

        <div class="modal-body">
          <p class="modal-tip">请输入这条说说的访问密码。</p>
          <input
            v-model="passwordForm.password"
            type="password"
            class="password-input"
            placeholder="请输入密码"
            @keyup.enter="submitPassword"
          />
          <p v-if="passwordError" class="password-error">{{ passwordError }}</p>
        </div>

        <div class="modal-footer">
          <button class="ghost-btn" @click="closePasswordModal">取消</button>
          <button class="primary-btn" :disabled="unlocking" @click="submitPassword">
            {{ unlocking ? '验证中...' : '确认查看' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { momentsApi } from '@/api/frontend'
import { TWIKOO_CONFIG, TWIKOO_ENV_ID } from '@/config/twikoo'
import { updateSeo } from '@/utils/seo'

const PAGE_SIZE = 12

const initialLoading = ref(true)
const loadingMore = ref(false)
const moments = ref([])
const currentPage = ref(0)
const total = ref(0)
const expandedMonths = ref([])
const rippleStates = ref({})
const showPasswordModal = ref(false)
const unlocking = ref(false)
const passwordError = ref('')
const currentMomentId = ref(null)
const loadMoreTrigger = ref(null)
const passwordForm = reactive({
  password: ''
})

let loadMoreObserver = null
const rippleTimers = new Map()

const hasMore = computed(() => moments.value.length < total.value)

const formatDate = (dateStr) => new Date(dateStr)

const formatMonth = (dateStr) => {
  const date = formatDate(dateStr)
  return `${date.getMonth() + 1}月`
}

const formatDay = (dateStr) => {
  const date = formatDate(dateStr)
  return `${date.getDate()}日`
}

const formatTime = (dateStr) => {
  const date = formatDate(dateStr)
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const formatFull = (dateStr) => {
  const date = formatDate(dateStr)
  return date.toLocaleString('zh-CN', { hour12: false })
}

const formatMonthLabel = (dateStr) => {
  const date = formatDate(dateStr)
  return `${date.getFullYear()}年 ${date.getMonth() + 1}月`
}

const getMonthKey = (dateStr) => {
  const date = formatDate(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
}

const monthGroups = computed(() => {
  const groups = new Map()

  moments.value.forEach((moment) => {
    const key = getMonthKey(moment.create_time)
    if (!groups.has(key)) {
      groups.set(key, {
        key,
        label: formatMonthLabel(moment.create_time),
        items: []
      })
    }

    groups.get(key).items.push(moment)
  })

  return Array.from(groups.values())
})

const syncExpandedMonths = () => {
  if (!monthGroups.value.length) {
    expandedMonths.value = []
    return
  }

  const validKeys = new Set(monthGroups.value.map(group => group.key))
  const keptKeys = expandedMonths.value.filter(key => validKeys.has(key))

  if (!keptKeys.length) {
    keptKeys.push(monthGroups.value[0].key)
  }

  expandedMonths.value = keptKeys
}

const hydrateMoment = async (moment) => {
  const accessToken = sessionStorage.getItem(`moment_access_${moment.id}`)
  if (!moment.need_password || !accessToken) {
    return moment
  }

  try {
    const detailRes = await momentsApi.detail(moment.id)
    return detailRes.data || moment
  } catch (error) {
    return moment
  }
}

const fetchMomentsPage = async (page) => {
  const res = await momentsApi.list({ page, size: PAGE_SIZE })
  const baseMoments = res.data.items || []
  const hydratedMoments = await Promise.all(baseMoments.map(hydrateMoment))

  total.value = res.data.total || 0
  currentPage.value = page

  if (page === 1) {
    moments.value = hydratedMoments
  } else {
    moments.value = [...moments.value, ...hydratedMoments]
  }

  syncExpandedMonths()
}

const loadInitialMoments = async () => {
  try {
    initialLoading.value = true
    await fetchMomentsPage(1)
  } catch (error) {
    console.error('加载空间页面失败:', error)
  } finally {
    initialLoading.value = false
  }
}

const loadMoreMoments = async () => {
  if (loadingMore.value || initialLoading.value || !hasMore.value) {
    return
  }

  try {
    loadingMore.value = true
    await fetchMomentsPage(currentPage.value + 1)
  } catch (error) {
    console.error('加载更多说说失败:', error)
  } finally {
    loadingMore.value = false
  }
}

const setupLoadMoreObserver = () => {
  loadMoreObserver?.disconnect()

  if (!loadMoreTrigger.value) {
    return
  }

  loadMoreObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        loadMoreMoments()
      }
    })
  }, {
    rootMargin: '0px 0px 280px 0px',
    threshold: 0
  })

  loadMoreObserver.observe(loadMoreTrigger.value)
}

const triggerHeaderRipple = (monthKey, event) => {
  if (!event?.currentTarget) {
    return
  }

  const rect = event.currentTarget.getBoundingClientRect()
  rippleStates.value = {
    ...rippleStates.value,
    [monthKey]: {
      id: Date.now() + Math.random(),
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    }
  }

  const previousTimer = rippleTimers.get(monthKey)
  if (previousTimer) {
    window.clearTimeout(previousTimer)
  }

  const timer = window.setTimeout(() => {
    const nextState = { ...rippleStates.value }
    delete nextState[monthKey]
    rippleStates.value = nextState
    rippleTimers.delete(monthKey)
  }, 790)

  rippleTimers.set(monthKey, timer)
}

const toggleMonth = (monthKey, event) => {
  triggerHeaderRipple(monthKey, event)
  const index = expandedMonths.value.indexOf(monthKey)
  if (index >= 0) {
    expandedMonths.value.splice(index, 1)
    return
  }

  expandedMonths.value.push(monthKey)
}

const openPasswordModal = (momentId) => {
  currentMomentId.value = momentId
  passwordForm.password = ''
  passwordError.value = ''
  showPasswordModal.value = true
}

const closePasswordModal = () => {
  showPasswordModal.value = false
  passwordForm.password = ''
  passwordError.value = ''
  currentMomentId.value = null
}

const submitPassword = async () => {
  if (!currentMomentId.value || !passwordForm.password.trim()) {
    passwordError.value = '请输入密码'
    return
  }

  try {
    unlocking.value = true
    passwordError.value = ''
    const verifyRes = await momentsApi.verifyPassword(currentMomentId.value, passwordForm.password.trim())
    if (!verifyRes.data?.passed) {
      passwordError.value = '密码错误，请重试'
      return
    }

    if (verifyRes.data.access_token) {
      sessionStorage.setItem(`moment_access_${currentMomentId.value}`, verifyRes.data.access_token)
    }

    const detailRes = await momentsApi.detail(currentMomentId.value)
    const targetIndex = moments.value.findIndex(moment => moment.id === currentMomentId.value)
    if (targetIndex >= 0 && detailRes.data) {
      moments.value[targetIndex] = detailRes.data
    }

    closePasswordModal()
  } catch (error) {
    console.error('验证说说密码失败:', error)
    passwordError.value = '验证失败，请稍后重试'
  } finally {
    unlocking.value = false
  }
}

const initTwikoo = () => {
  nextTick(() => {
    if (window.twikoo) {
      initTwikooInstance()
      return
    }

    const script = document.createElement('script')
    script.src = '/twikoo.min.js'
    script.onload = () => {
      initTwikooInstance()
    }
    script.onerror = () => {
      console.error('Twikoo 脚本加载失败')
    }
    document.head.appendChild(script)
  })
}

const initTwikooInstance = () => {
  if (!window.twikoo) {
    console.error('Twikoo 未正确加载')
    return
  }

  window.twikoo.init({
    envId: TWIKOO_ENV_ID,
    el: TWIKOO_CONFIG.el,
    path: '/space',
    lang: TWIKOO_CONFIG.lang
  })
}

const onAccordionBeforeEnter = (el) => {
  el.style.height = '0px'
  el.style.opacity = '0'
  el.style.transform = 'translateY(-18px) scale(0.985)'
  el.style.filter = 'blur(10px)'
  el.style.overflow = 'hidden'
}

const onAccordionEnter = (el, done) => {
  void el.offsetHeight
  const height = `${el.scrollHeight}px`
  el.style.transition = [
    'height 620ms cubic-bezier(0.16, 1, 0.3, 1)',
    'opacity 320ms cubic-bezier(0.22, 1, 0.36, 1)',
    'transform 620ms cubic-bezier(0.16, 1, 0.3, 1)',
    'filter 620ms cubic-bezier(0.16, 1, 0.3, 1)'
  ].join(', ')

  requestAnimationFrame(() => {
    el.style.height = height
    el.style.opacity = '1'
    el.style.transform = 'translateY(0) scale(1)'
    el.style.filter = 'blur(0px)'
  })

  window.setTimeout(done, 620)
}

const onAccordionAfterEnter = (el) => {
  el.style.height = 'auto'
  el.style.overflow = 'visible'
  el.style.transition = ''
}

const onAccordionBeforeLeave = (el) => {
  el.style.height = `${el.scrollHeight}px`
  el.style.opacity = '1'
  el.style.transform = 'translateY(0) scale(1)'
  el.style.filter = 'blur(0px)'
  el.style.overflow = 'hidden'
}

const onAccordionLeave = (el, done) => {
  void el.offsetHeight
  el.style.transition = [
    'height 520ms cubic-bezier(0.55, 0, 0.2, 1)',
    'opacity 260ms ease',
    'transform 520ms cubic-bezier(0.4, 0, 0.2, 1)',
    'filter 520ms cubic-bezier(0.4, 0, 0.2, 1)'
  ].join(', ')

  requestAnimationFrame(() => {
    el.style.height = '0px'
    el.style.opacity = '0'
    el.style.transform = 'translateY(-14px) scale(0.985)'
    el.style.filter = 'blur(8px)'
  })

  window.setTimeout(done, 520)
}

const onAccordionAfterLeave = (el) => {
  el.style.transition = ''
}

watch(loadMoreTrigger, async () => {
  await nextTick()
  setupLoadMoreObserver()
})

onMounted(async () => {
  await loadInitialMoments()
  await nextTick()
  setupLoadMoreObserver()
  initTwikoo()

  updateSeo({
    title: '空间',
    description: '浏览 MoZhi 的空间时间线，记录零散想法、生活片段与短内容。',
    path: '/space',
    keywords: ['空间', '说说', '时间线', '日常记录']
  })
})

onUnmounted(() => {
  loadMoreObserver?.disconnect()
  rippleTimers.forEach(timer => window.clearTimeout(timer))
  rippleTimers.clear()
})
</script>

<style lang="scss" scoped>
.space-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

.page-header {
  margin-bottom: var(--spacing-2xl);
  text-align: center;
}

.page-title {
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-4xl);
  color: var(--color-text-primary);
}

.page-description {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-base);
}

.timeline-group-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.month-group {
  position: relative;
  border-radius: var(--radius-xl);

  &.is-expanded {
    .month-header {
      border-color: color-mix(in srgb, var(--color-accent) 46%, var(--glass-border));
      box-shadow:
        0 18px 44px rgba(15, 23, 42, 0.08),
        0 0 0 1px rgba(59, 130, 246, 0.06) inset;
    }
  }
}

.month-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--glass-bg-solid);
  border: 1px solid rgba(148, 163, 184, 0.24);
  border-radius: var(--radius-xl);
  cursor: pointer;
  overflow: hidden;
  transition:
    transform 420ms cubic-bezier(0.22, 1, 0.36, 1),
    border-color 420ms cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 420ms cubic-bezier(0.22, 1, 0.36, 1),
    background 420ms cubic-bezier(0.22, 1, 0.36, 1);

  > * {
    position: relative;
    z-index: 1;
  }

  &:hover {
    transform: translateY(-2px);
    border-color: rgba(148, 163, 184, 0.34);
    box-shadow: 0 18px 42px rgba(15, 23, 42, 0.1);
  }

  &:active {
    transform: translateY(1px) scale(0.985);
    transition-duration: 140ms;
    box-shadow:
      0 10px 20px rgba(15, 23, 42, 0.12),
      inset 0 2px 10px rgba(15, 23, 42, 0.08);
  }

  &.expanded {
    background: var(--glass-bg-solid);
    box-shadow: 0 20px 48px rgba(15, 23, 42, 0.12);
    border-color: color-mix(in srgb, var(--color-accent) 46%, rgba(148, 163, 184, 0.24));

    .expand-icon {
      transform: rotate(180deg) scale(1.04);
    }
  }
}

.month-header-ripple {
  position: absolute;
  z-index: 0;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(100, 116, 139, 0.36) 0%, rgba(148, 163, 184, 0.28) 24%, rgba(148, 163, 184, 0.16) 46%, rgba(148, 163, 184, 0.07) 62%, rgba(148, 163, 184, 0) 76%);
  transform: translate(-50%, -50%) scale(0);
  pointer-events: none;
  will-change: transform, opacity;
  animation: headerRipple 790ms cubic-bezier(0.22, 0.9, 0.3, 1) forwards;
}

.month-header-main {
  display: flex;
  align-items: center;
  text-align: left;
}

.month-title {
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
  font-weight: 700;
  letter-spacing: 0.01em;
}

.expand-icon {
  width: 20px;
  height: 20px;
  color: var(--color-text-tertiary);
  transition: transform 620ms cubic-bezier(0.16, 1, 0.3, 1);
}

.timeline-shell {
  transform-origin: top center;
  will-change: height, opacity, transform, filter;
}

.timeline {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
  margin: var(--spacing-lg) 0 0 72px;
  padding: 4px 2px 2px 0;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: -36px;
    width: 2px;
    background:
      linear-gradient(180deg, rgba(59, 130, 246, 0.9), rgba(59, 130, 246, 0.16) 45%, rgba(148, 163, 184, 0.18));
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.14);
    transform-origin: top center;
    animation: timelineLineGrow 900ms cubic-bezier(0.19, 1, 0.22, 1) both;
  }
}

.timeline-item {
  position: relative;
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: var(--spacing-lg);
  align-items: start;

  &::before {
    content: '';
    position: absolute;
    left: -43px;
    top: 22px;
    width: 14px;
    height: 14px;
    border: 3px solid var(--color-accent);
    border-radius: 50%;
    background: var(--color-bg-primary);
    box-shadow:
      0 0 0 8px rgba(59, 130, 246, 0.08),
      0 0 20px rgba(59, 130, 246, 0.16);
    opacity: 0;
    transform: scale(0.25);
    animation: timelineNodePop 520ms cubic-bezier(0.22, 1.28, 0.36, 1) forwards;
    animation-delay: var(--item-delay);
  }
}

.timeline-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  padding-top: var(--spacing-md);
  opacity: 0;
  transform: translateX(-20px);
  animation: timelineMetaReveal 560ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--item-delay) + 40ms);
}

.timeline-date {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.timeline-time {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
}

.timeline-card {
  padding: var(--spacing-xl);
  background: var(--glass-bg-solid);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  box-shadow:
    0 10px 30px rgba(15, 23, 42, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  transition:
    transform 300ms ease,
    box-shadow 300ms ease,
    border-color 300ms ease;
  opacity: 0;
  transform: translateX(-36px) translateY(8px) scale(0.985);
  filter: blur(8px);
  animation: timelineCardSlideIn 760ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--item-delay) + 70ms);

  &:hover {
    transform: translateY(-2px);
    border-color: color-mix(in srgb, var(--color-accent) 32%, var(--glass-border));
    box-shadow:
      0 18px 40px rgba(15, 23, 42, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.14);
  }
}

.timeline-card-head {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.timeline-badge,
.lock-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: var(--font-size-xs);
}

.timeline-badge {
  color: var(--color-accent);
  background: var(--color-accent-light);
}

.lock-badge {
  color: #b45309;
  background: rgba(245, 158, 11, 0.14);
}

.timeline-content {
  margin: 0;
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
  line-height: 1.9;
  white-space: pre-wrap;
  word-break: break-word;
}

.locked-state {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-md);
  color: var(--color-text-secondary);
}

.unlock-btn,
.primary-btn,
.ghost-btn,
.load-more-btn {
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition:
    transform 260ms cubic-bezier(0.22, 1, 0.36, 1),
    background 260ms ease,
    box-shadow 260ms ease,
    color 260ms ease;
}

.unlock-btn,
.primary-btn,
.load-more-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  color: #fff;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-hover));
  box-shadow: 0 12px 28px rgba(59, 130, 246, 0.22);

  &:hover:not(:disabled) {
    transform: translateY(-1px);
  }
}

.ghost-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary);
}

.timeline-footer {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-divider);
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
}

.load-more-trigger {
  height: 1px;
}

.loading-more-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg) 0 var(--spacing-sm);
  color: var(--color-text-tertiary);
}

.load-more-btn {
  align-self: center;
  min-width: 148px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  background: rgba(15, 23, 42, 0.45);
}

.password-modal {
  width: min(100%, 420px);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}

.modal-header,
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) var(--spacing-xl);
}

.modal-header {
  border-bottom: 1px solid var(--color-divider);
}

.modal-body {
  padding: var(--spacing-xl);
}

.modal-tip,
.password-error {
  margin: 0 0 var(--spacing-md);
}

.password-input {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  outline: none;

  &:focus {
    border-color: var(--color-accent);
  }
}

.password-error {
  margin-top: var(--spacing-sm);
  color: #dc2626;
  font-size: var(--font-size-sm);
}

.close-btn {
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 24px;
  cursor: pointer;
}

.loading-state,
.empty-tip {
  display: flex;
  justify-content: center;
  padding: var(--spacing-3xl);
  color: var(--color-text-tertiary);
}

.comments-section {
  max-width: 800px;
  margin: var(--spacing-3xl) auto 0;
}

.comments-title {
  margin: 0 0 var(--spacing-lg);
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
}

#twikoo-container {
  min-height: 200px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;

  &.small {
    width: 18px;
    height: 18px;
    border-width: 2px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes timelineLineGrow {
  from {
    opacity: 0;
    transform: scaleY(0);
  }

  to {
    opacity: 1;
    transform: scaleY(1);
  }
}

@keyframes timelineNodePop {
  0% {
    opacity: 0;
    transform: scale(0.25);
  }

  58% {
    opacity: 1;
    transform: scale(1.18);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes timelineMetaReveal {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes timelineCardSlideIn {
  0% {
    opacity: 0;
    transform: translateX(-36px) translateY(8px) scale(0.985);
    filter: blur(8px);
  }

  62% {
    opacity: 1;
    transform: translateX(6px) translateY(0) scale(1.005);
    filter: blur(0);
  }

  100% {
    opacity: 1;
    transform: translateX(0) translateY(0) scale(1);
    filter: blur(0);
  }
}

@keyframes headerRipple {
  0% {
    opacity: 0.64;
    transform: translate(-50%, -50%) scale(0);
  }

  42% {
    opacity: 0.34;
  }

  72% {
    opacity: 0.16;
  }

  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(2.15);
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: var(--font-size-3xl);
  }

  .month-header {
    padding: var(--spacing-md) var(--spacing-lg);
  }

  .month-header-main {
    align-items: center;
  }

  .timeline {
    margin-left: 0;

    &::before {
      left: 16px;
    }
  }

  .timeline-item {
    grid-template-columns: 1fr;

    &::before {
      left: 9px;
      top: 18px;
    }
  }

  .timeline-meta {
    align-items: flex-start;
    padding-left: 44px;
  }
}
</style>
