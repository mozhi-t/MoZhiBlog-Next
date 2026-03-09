<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">MoZhi Blog</h1>
        <p class="hero-subtitle">探索技术与生活的美好</p>
      </div>
    </section>

    <!-- Categories Section -->
    <section class="categories-section">
      <h2 class="section-title">分类</h2>
      <div class="categories-grid">
        <CategoryCard
          v-for="(category, index) in categories"
          :key="category.slug"
          :name="category.name"
          :slug="category.slug"
          :count="category.count"
          :style="{ transitionDelay: `${index * 0.1}s` }"
        />
      </div>
    </section>

    <!-- Articles Section -->
    <section class="articles-section">
      <h2 class="section-title">最新文章</h2>
      <div class="articles-grid">
        <ArticleCard
          v-for="(article, index) in articles"
          :key="article.id"
          :article="article"
          :style="{ transitionDelay: `${index * 0.1}s` }"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArticleCard from '../components/common/ArticleCard.vue'
import CategoryCard from '../components/common/CategoryCard.vue'

// Mock Data - 模拟数据
const categories = ref([
  { name: '技术', slug: 'tech', count: 12 },
  { name: '生活', slug: 'life', count: 8 },
  { name: '随笔', slug: 'essay', count: 15 }
])

const articles = ref([
  {
    id: 1,
    title: '探索 Vue 3 Composition API 的最佳实践',
    excerpt: '深入理解 Vue 3 的 Composition API，学习如何编写更清晰、可维护的组件代码。',
    date: '2024-01-15',
    category: '技术',
    cover: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800'
  },
  {
    id: 2,
    title: '设计系统的美学：从苹果设计哲学学到的',
    excerpt: '分析苹果设计系统的核心原则，探讨如何打造简洁优雅的用户界面。',
    date: '2024-01-10',
    category: '设计',
    cover: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800'
  },
  {
    id: 3,
    title: '在忙碌的生活中寻找平衡',
    excerpt: '分享一些关于时间管理、心态调整的思考与实践。',
    date: '2024-01-05',
    category: '生活',
    cover: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800'
  },
  {
    id: 4,
    title: 'TypeScript 类型系统详解',
    excerpt: '全面解析 TypeScript 的高级类型特性，提升代码类型安全。',
    date: '2023-12-28',
    category: '技术',
    cover: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800'
  },
  {
    id: 5,
    title: '极简主义：少即是多',
    excerpt: '探讨极简主义生活方式带来的内心平静与效率提升。',
    date: '2023-12-20',
    category: '随笔',
    cover: 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?w=800'
  },
  {
    id: 6,
    title: 'CSS Grid 布局完全指南',
    excerpt: '掌握现代 CSS Grid 布局，创建复杂的响应式网页结构。',
    date: '2023-12-15',
    category: '技术',
    cover: 'https://images.unsplash.com/photo-1507721999472-8ed4421c4af2?w=800'
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

/* Section Styles */
.section-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xl);
  padding-left: var(--spacing-md);
  border-left: 3px solid var(--color-accent);
}

/* Categories Section */
.categories-section {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-lg);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
}

@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }
}

/* Articles Section */
.articles-section {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-lg);
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-xl);
}

@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: var(--font-size-4xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-lg);
  }
}
</style>
