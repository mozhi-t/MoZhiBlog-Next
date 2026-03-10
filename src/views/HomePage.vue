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
            <div class="author-avatar">
              <img src="@/assets/tx.jpg" alt="头像" />
            </div>
            <h3 class="author-name">MoZhi</h3>
            <p class="author-bio">远方很远，步履不停，未来可期</p>
          </div>
        </aside>

        <!-- Right Content - Article List -->
        <div class="articles-list">
          <ArticleCard
            v-for="(article, index) in articles"
            :key="article.id"
            :article="article"
            :style="{ transitionDelay: `${index * 0.1}s` }"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ArticleCard from '../components/common/ArticleCard.vue'

const subtitles = [
  '远方很远，步履不停，未来可期',
  'Far away, walking incessantly, with a promising future ahead'
]

const currentSubtitleIndex = ref(0)
const currentSubtitle = ref(subtitles[0])
const isAnimating = ref(false)
const showSubtitle = ref(true)
let timer = null

const currentChars = computed(() => currentSubtitle.value.split(''))

const startAnimation = () => {
  if (isAnimating.value) return
  isAnimating.value = true

  // 根据文字长度计算显示时间（每个字符0.08s + 额外2s）
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
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
})

// Mock Data - 模拟数据
const articles = ref([
  {
    id: 1,
    title: '探索 Vue 3 Composition API 的最佳实践',
    excerpt: '深入理解 Vue 3 的 Composition API，学习如何编写更清晰、可维护的组件代码。',
    date: '2025/4/6',
    category: '技术',
    tags: ['RAG', 'LLM', '生成式 AI', '检索增强生成']
  },
  {
    id: 2,
    title: '设计系统的美学：从苹果设计哲学学到的',
    excerpt: '分析苹果设计系统的核心原则，探讨如何打造简洁优雅的用户界面。',
    date: '2025/4/1',
    category: '设计',
    tags: ['UI', 'UX', '设计系统']
  },
  {
    id: 3,
    title: '在忙碌的生活中寻找平衡',
    excerpt: '分享一些关于时间管理、心态调整的思考与实践。',
    date: '2025/3/25',
    category: '生活',
    tags: ['生活', '自我成长']
  },
  {
    id: 4,
    title: 'TypeScript 类型系统详解',
    excerpt: '全面解析 TypeScript 的高级类型特性，提升代码类型安全。',
    date: '2025/3/18',
    category: '技术',
    tags: ['TypeScript', '前端']
  },
  {
    id: 5,
    title: '极简主义：少即是多',
    excerpt: '探讨极简主义生活方式带来的内心平静与效率提升。',
    date: '2025/3/10',
    category: '随笔',
    tags: ['极简主义', '生活方式']
  },
  {
    id: 6,
    title: 'CSS Grid 布局完全指南',
    excerpt: '掌握现代 CSS Grid 布局，创建复杂的响应式网页结构。',
    date: '2025/3/5',
    category: '技术',
    tags: ['CSS', 'Grid', '布局']
  }
])

onMounted(() => {
  // 可以在这里从API获取数据
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
}

/* Right Content - Article List */
.articles-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
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
