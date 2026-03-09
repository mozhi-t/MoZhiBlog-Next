<template>
  <div class="category-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">{{ categoryName }}</h1>
      <p class="page-description">共 {{ articles.length }} 篇文章</p>
    </header>

    <!-- Category Tags -->
    <div class="category-tags">
      <button
        v-for="cat in allCategories"
        :key="cat.slug"
        class="category-tag"
        :class="{ active: cat.slug === slug }"
        @click="switchCategory(cat.slug)"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- Articles List -->
    <div class="articles-list">
      <ArticleCard
        v-for="(article, index) in articles"
        :key="article.id"
        :article="article"
        :style="{ transitionDelay: `${index * 0.1}s` }"
      />
    </div>

    <!-- Load More -->
    <div class="load-more" v-if="hasMore">
      <button class="load-more-btn" @click="loadMore">
        加载更多
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'

const route = useRoute()
const router = useRouter()

const slug = computed(() => route.params.slug)

// Mock categories
const allCategories = ref([
  { name: '技术', slug: 'tech' },
  { name: '生活', slug: 'life' },
  { name: '随笔', slug: 'essay' }
])

const categoryName = computed(() => {
  const cat = allCategories.value.find(c => c.slug === slug.value)
  return cat ? cat.name : '分类'
})

// Mock articles
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
    id: 4,
    title: 'TypeScript 类型系统详解',
    excerpt: '全面解析 TypeScript 的高级类型特性，提升代码类型安全。',
    date: '2023-12-28',
    category: '技术',
    cover: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800'
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

const hasMore = ref(false)

const switchCategory = (newSlug) => {
  router.push(`/category/${newSlug}`)
}

const loadMore = () => {
  // 实现加载更多逻辑
}

// Watch for category change
watch(slug, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<style lang="scss" scoped>
/* ============================================
   Category Page - 分类页
   ============================================ */
.category-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-description {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
}

/* Category Tags */
.category-tags {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}

.category-tag {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-text-primary);
  }

  &.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
    transform: scale(1.02);
    box-shadow: var(--shadow-md);
  }
}

/* Articles List */
.articles-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-xl);
}

@media (max-width: 768px) {
  .articles-list {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: var(--font-size-3xl);
  }
}

/* Load More */
.load-more {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-2xl);
}

.load-more-btn {
  padding: var(--spacing-md) var(--spacing-2xl);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
  }
}
</style>
