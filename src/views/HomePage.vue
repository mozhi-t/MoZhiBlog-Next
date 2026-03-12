<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">MoZhi's blog</h1>
        <p class="hero-subtitle" :class="{ hiding: !showSubtitle }" :key="currentSubtitleIndex">
          <span
            v-for="(char, index) in currentChars"
            :key="index"
            class="char"
            :style="{ animationDelay: `${index * 0.08}s` }"
          >{{ char }}</span>
        </p>
      </div>
    </section>

    <!-- Main Content - Two Column Layout -->
    <section class="main-content">
      <div class="content-wrapper">
        <!-- Left Sidebar - Author Card -->
        <aside class="sidebar">
          <div class="author-card">
            <div
              class="greeting-cylinder"
              :class="{ pressing: isPressing }"
              @click="handleCylinderClick"
              @mouseenter="handleMouseEnter"
              @mouseleave="handleMouseLeave"
            >
              {{ greetingText }}
            </div>
            <div class="author-avatar">
              <img src="@/assets/tx.jpg" alt="头像" />
            </div>
            <h3 class="author-name">MoZhi</h3>
            <p class="author-bio">远方很远，步履不停，未来可期</p>
            <div class="author-links">
              <a href="https://github.com/mozhi-it" target="_blank" rel="noopener" class="author-btn" title="GitHub">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a href="mailto:mozhi.it@qq.com" class="author-btn" title="邮箱">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </a>
            </div>

            <!-- Year Progress Card -->
            <div class="year-progress-card">
              <div class="year-progress-header">
                <span class="year-label">{{ currentYear }}</span>
                <span class="year-progress-value">{{ yearProgress7 }}%</span>
              </div>
              <div class="year-progress-bar">
                <div class="progress-ring">
                  <div class="progress-ring-fill" :style="{ width: yearProgress2 + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <!-- Right Content - Article List -->
        <div class="articles-list">
          <ArticleCard
            v-for="article in articles"
            :key="article.id"
            :article="article"
          />

          <!-- Pagination -->
          <Pagination
            v-if="total > pageSize"
            :current-page="currentPage"
            :total="total"
            :page-size="pageSize"
            @page-change="handlePageChange"
            class="article-pagination"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ArticleCard from '../components/common/ArticleCard.vue'
import Pagination from '../components/common/Pagination.vue'
import { articlesApi } from '../api/frontend'

// 问候语数据
const greetingData = {
  morning: ['早安呀，记得吃饭！', '早上好，元气满满！', '早安，天天开心！'],
  noon: ['午安呀，好好吃饭！', '午后好，温柔相伴！', '中午好，别饿肚子！'],
  afternoon: ['下午好，多喝水呀！', '下午好，劳逸结合！', '下午好，心情明朗！'],
  evening: ['晚上好，今天辛苦！', '晚安呀，早点睡觉！', '晚安，丢掉烦恼！'],
  lateNight: ['凌晨好，别熬啦！', '深夜好，该休息啦！', '凌晨好，放下手机！'],
  special: ['愿美好，如约而至！', '存热爱，平安顺遂！', '常欢喜，岁岁无忧！', '|´・ω・)ノ']
}

// 获取当前时间段
const getTimePeriod = () => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 9) return 'morning'
  if (hour >= 9 && hour < 12) return 'noon'
  if (hour >= 12 && hour < 18) return 'afternoon'
  if (hour >= 18 && hour < 24) return 'evening'
  return 'lateNight'
}

// 随机选择问候语（10%概率显示特殊话语）
const getRandomGreeting = () => {
  const isSpecial = Math.random() < 0.1
  if (isSpecial) {
    const specialList = greetingData.special
    return specialList[Math.floor(Math.random() * specialList.length)]
  }
  const period = getTimePeriod()
  const list = greetingData[period]
  return list[Math.floor(Math.random() * list.length)]
}

const greetingText = ref(getRandomGreeting())
const originalGreeting = ref(greetingText.value)

// 点击计数器
const clickCount = ref(0)
const isPressing = ref(false)
const hasEntered = ref(false)

const clickMessages = ['点这里干什么', '怎么还点？', '那你点吧']

const handleCylinderClick = () => {
  if (!hasEntered.value) return

  isPressing.value = true
  setTimeout(() => {
    isPressing.value = false
  }, 150)

  clickCount.value++
  if (clickCount.value <= 3) {
    greetingText.value = clickMessages[clickCount.value - 1]
  } else if (clickCount.value > 3 && clickCount.value < 99) {
    greetingText.value = `x${clickCount.value}`
  } else if (clickCount.value === 99) {
    greetingText.value = '你真有毅力'
  } else {
    greetingText.value = `x${clickCount.value}`
  }
}

const handleMouseEnter = () => {
  hasEntered.value = true
}

const handleMouseLeave = () => {
  hasEntered.value = false
  clickCount.value = 0
  greetingText.value = originalGreeting.value
}

// 年份进度
const currentYear = computed(() => new Date().getFullYear())

const getYearProgress = () => {
  const now = new Date()
  const year = now.getFullYear()
  const start = new Date(year, 0, 0)
  const end = new Date(year + 1, 0, 0)
  const passed = now - start
  const total = end - start
  return (passed / total) * 100
}

const yearProgress = ref(getYearProgress())
const yearProgress2 = computed(() => yearProgress.value.toFixed(2))
const yearProgress7 = computed(() => yearProgress.value.toFixed(7))

// 每秒更新进度
let progressTimer = null
const updateProgress = () => {
  yearProgress.value = getYearProgress()
}

const subtitles = [
  '远方很远，步履不停，未来可期',
  'Far away, walking incessantly, with a promising future ahead'
]

const currentSubtitleIndex = ref(0)
const currentSubtitle = ref(subtitles[0])
const isAnimating = ref(false)
const showSubtitle = ref(true)
const loading = ref(true)
let timer = null

const currentChars = computed(() => currentSubtitle.value.split(''))

// 文章列表
const articles = ref([])
const currentPage = ref(1)
const total = ref(0)
const pageSize = 20

// 加载文章列表
const loadArticles = async (page = 1) => {
  try {
    loading.value = true
    const res = await articlesApi.list({ page, size: pageSize })
    articles.value = res.data.items.map(item => ({
      id: item.id,
      title: item.title,
      excerpt: item.summary || '',
      date: new Date(item.create_time).toLocaleDateString('zh-CN'),
      category: item.category?.name || '',
      category_id: item.category_id || null,
      tag_list: item.tag_list || [],
      read_count: item.read_count || 0,
      content: item.content || '',
      create_time: item.create_time,
      update_time: item.update_time
    }))
    total.value = res.data.total || 0
    currentPage.value = page
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  loadArticles(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const startAnimation = () => {
  if (isAnimating.value) return
  isAnimating.value = true

  // 根据文字长度计算显示时间
  const displayTime = currentSubtitle.value.length * 100 + 4000

  timer = setTimeout(() => {
    showSubtitle.value = false

    // 等待消失动画完成
    setTimeout(() => {
      // 切换到下一段文字
      currentSubtitleIndex.value = (currentSubtitleIndex.value + 1) % subtitles.length
      currentSubtitle.value = subtitles[currentSubtitleIndex.value]
      showSubtitle.value = true
      isAnimating.value = false

      // 继续轮播
      startAnimation()
    }, 600)
  }, displayTime)
}

onMounted(() => {
  startAnimation()
  loadArticles()
  progressTimer = setInterval(updateProgress, 1000)
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
  if (progressTimer) clearInterval(progressTimer)
})
</script>

<style lang="scss" scoped>
/* ============================================
   Home Page - 首页
   ============================================ */
.home-page {
  min-height: 100vh;
  padding-top: calc(var(--nav-height) + 60px);
  padding-bottom: var(--spacing-3xl);
}

/* Hero Section */
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
  text-align: center;
}

.hero-content {
  animation: heroFadeIn 0.5s ease-out;
}

.hero-title {
  font-size: var(--font-size-5xl);
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -1px;
  margin-bottom: var(--spacing-md);
}

.hero-subtitle {
  font-size: var(--font-size-xl);
  color: var(--color-text-secondary);
  font-weight: 400;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2px;
  transition: all 0.6s ease;
}

.hero-subtitle.hiding {
  filter: blur(6px);
  opacity: 0;
  transform: translateY(15px);
}

.char {
  display: inline-block;
  filter: blur(4px);
  opacity: 0;
  animation: typewriter 0.5s ease-out forwards;
}

@keyframes typewriter {
  0% {
    opacity: 0;
    filter: blur(4px);
    transform: translateY(8px);
  }
  60% {
    opacity: 1;
    filter: blur(0);
    transform: translateY(-2px);
  }
  100% {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0);
  }
}

@keyframes heroFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Main Content - Two Column Layout */
.main-content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.content-wrapper {
  display: flex;
  gap: var(--spacing-2xl);
}

/* Left Sidebar - Author Card */
.sidebar {
  flex-shrink: 0;
  width: 290px;
}

.author-card {
  position: sticky;
  top: calc(var(--nav-height) + 40px);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-smooth);

  &:hover {
    box-shadow: var(--shadow-md);
  }
}

.greeting-cylinder {
  position: relative;
  display: inline-block;
  width: 180px;
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-md);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  user-select: none;

  &::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 10px solid var(--color-border);
  }

  &::before {
    content: '';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid var(--color-bg-tertiary);
    z-index: 1;
  }

  &:hover {
    transform: scale(1.05);
    background: var(--color-accent-light);
    opacity: 0.8;

    &::before {
      border-top-color: var(--color-accent-light);
    }
  }

  &.pressing {
    animation: press 0.15s ease forwards;
  }
}

@keyframes press {
  0% { transform: scale(1); }
  50% { transform: scale(0.92); }
  100% { transform: scale(1); }
}

.author-avatar {
  width: 100px;
  height: 100px;
  margin: 0 auto var(--spacing-lg);
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--color-accent-light);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.author-name {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.author-bio {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: var(--line-height-base);
  margin-bottom: var(--spacing-lg);
}

.author-links {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.author-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  text-decoration: none;
  transition: all var(--transition-base);
  color: var(--color-text-secondary);

  &:hover {
    color: var(--color-text-primary);
    transform: scale(1.1);
  }
}

/* Year Progress Card */
.year-progress-card {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  text-align: center;
}

.year-progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.year-label {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.year-progress-value {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.year-progress-bar {
  display: flex;
  justify-content: center;
}

.progress-ring {
  width: 100%;
  height: 6px;
  background: var(--color-bg-tertiary);
  border-radius: 3px;
  overflow: hidden;
}

.progress-ring-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Right Content - Article List */
.articles-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Article Pagination */
.article-pagination {
  margin-top: var(--spacing-xl);
}

/* Responsive */
@media (max-width: 900px) {
  .content-wrapper {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .author-card {
    position: static;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: var(--font-size-4xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-lg);
  }
}
</style>
