<template>
  <div class="links-page">
    <header class="page-header">
      <h1 class="page-title">友链</h1>
      <p class="page-desc">山海相逢，心意相通</p>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <div v-else>
      <div v-if="bestFriends.length > 0" class="link-section">
        <h2 class="section-title">挚友</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in bestFriends"
            :key="'best-' + index"
            :href="link.url"
            target="_blank"
            rel="noopener"
            class="link-card best-friend"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="link-avatar">
              <img :src="link.avatar" :alt="link.name" />
            </div>
            <div class="link-info">
              <h3 class="link-name">{{ link.name }}</h3>
              <p class="link-desc">{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>

      <div v-if="friends.length > 0" class="link-section">
        <h2 class="section-title">朋友</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in friends"
            :key="'friend-' + index"
            :href="link.url"
            target="_blank"
            rel="noopener"
            class="link-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="link-avatar">
              <img :src="link.avatar" :alt="link.name" />
            </div>
            <div class="link-info">
              <h3 class="link-name">{{ link.name }}</h3>
              <p class="link-desc">{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>

      <div v-if="visitors.length > 0" class="link-section">
        <h2 class="section-title">来客</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in visitors"
            :key="'visitor-' + index"
            :href="link.url"
            target="_blank"
            rel="noopener"
            class="link-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="link-avatar">
              <img :src="link.avatar" :alt="link.name" />
            </div>
            <div class="link-info">
              <h3 class="link-name">{{ link.name }}</h3>
              <p class="link-desc">{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>

      <div v-if="links.length === 0" class="empty-tip">
        暂无友链
      </div>
    </div>

    <div class="contact-section">
      <h2 class="section-title">交换友链</h2>
      <p class="contact-text">{{ SITE_CONFIG.friendLink.intro }}</p>

      <div class="info-block">
        <h3 class="info-title">友链信息</h3>
        <pre class="code-block">name: {{ SITE_CONFIG.friendLink.siteName }}
link: {{ SITE_CONFIG.friendLink.siteUrl }}
avatar: {{ SITE_CONFIG.friendLink.avatar }}
descr: {{ SITE_CONFIG.friendLink.description }}</pre>
      </div>

      <div class="info-block">
        <h3 class="info-title">HTML</h3>
        <pre class="code-block">{{ friendLinkHtml }}</pre>
      </div>
    </div>

    <section class="comments-section">
      <h2 class="section-title">评论</h2>
      <div id="twikoo-container">
        <div id="tcomment"></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { friendLinksApi } from '../api/frontend'
import { SITE_CONFIG } from '../config/site'
import { TWIKOO_CONFIG, TWIKOO_ENV_ID } from '../config/twikoo'
import { updateSeo } from '../utils/seo'

const loading = ref(true)
const links = ref([])

const bestFriends = computed(() =>
  links.value.filter(link => link.weight === 0).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
)

const friends = computed(() =>
  links.value.filter(link => link.weight === 1).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
)

const visitors = computed(() =>
  links.value.filter(link => link.weight === 2).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
)

const friendLinkHtml = computed(
  () => `<a href="${SITE_CONFIG.friendLink.siteUrl}"><img src="${SITE_CONFIG.friendLink.avatar}" alt="avatar">${SITE_CONFIG.friendLink.siteName}</a>`
)

const loadLinks = async () => {
  try {
    loading.value = true
    const res = await friendLinksApi.list()
    links.value = res.data || []
    updateSeo({
      title: '友链',
      description: `浏览 ${SITE_CONFIG.name} 的友链页面，当前展示 ${links.value.length} 个站点，并支持留言申请互链。`,
      path: '/links',
      keywords: ['友链', '友情链接', '博客推荐']
    })
  } catch (error) {
    console.error('加载友链失败:', error)
  } finally {
    loading.value = false
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
    path: '/links',
    lang: TWIKOO_CONFIG.lang
  })
}

onMounted(() => {
  updateSeo({
    title: '友链',
    description: `浏览 ${SITE_CONFIG.name} 的友链页面，发现值得访问的博客与站点，并支持留言申请互链。`,
    path: '/links',
    keywords: ['友链', '友情链接', '博客推荐']
  })
  loadLinks()
  initTwikoo()
})
</script>

<style lang="scss" scoped>
.links-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.page-title {
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-desc {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-3xl);
}

.link-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  text-decoration: none;
  transition: all var(--transition-smooth);
  animation: cardFadeIn 0.4s ease forwards;
  opacity: 0;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);

    .link-name {
      color: var(--color-accent);
    }
  }

  &:active {
    transform: translateY(-4px) scale(0.99);
  }
}

[data-theme="dark"] .link-card {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
  }
}

.link-avatar {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: var(--radius-full);
  overflow: hidden;
  background: var(--color-bg-tertiary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.link-info {
  flex: 1;
  min-width: 0;
}

.link-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
  transition: color var(--transition-base);
}

.link-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-section {
  position: relative;
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

[data-theme="dark"] .contact-section {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.contact-text {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}

.info-block {
  margin-bottom: var(--spacing-lg);
}

.info-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.code-block {
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
  white-space: pre-wrap;
  word-break: break-all;
  overflow-x: auto;
  margin: 0;
}

.comments-section {
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
}

#twikoo-container {
  min-height: 200px;
}

@media (max-width: 768px) {
  .links-grid {
    grid-template-columns: 1fr;
  }
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: var(--spacing-3xl);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-3xl);
}
</style>
