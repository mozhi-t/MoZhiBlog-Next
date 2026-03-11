<template>
  <div class="category-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">{{ currentTitle }}</h1>
      <p class="page-description">共 {{ articles.length }} 篇文章</p>
    </header>

    <!-- Category Tags -->
    <div class="category-tags">
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="category-tag"
        :class="{ active: categoryId === cat.id }"
        @click="switchCategory(cat.id)"
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

    <!-- Empty State -->
    <div v-if="articles.length === 0 && !loading" class="empty-state">
      <p>暂无文章</p>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import { articlesApi, categoriesApi } from '../api/frontend'

const route = useRoute()
const router = useRouter()

// 当前分类ID
const categoryId = computed(() => {
  const id = route.query.category
  return id ? parseInt(id) : null
})

// 标题
const currentTitle = computed(() => {
  if (categoryId.value) {
    const cat = categories.value.find(c => c.id === categoryId.value)
    return cat ? cat.name : '分类'
  }
  return '分类'
})

// 分类列表
const categories = ref([])
const loading = ref(true)

// 文章列表
const articles = ref([])
const hasMore = ref(false)

// 加载分类列表
const loadCategories = async () => {
  try {
    const res = await categoriesApi.list()
    categories.value = res.data || []
  } catch (error) {
    console.error('加载分类失败:', error)
    categories.value = []
  }
}

// 加载文章列表
const loadArticles = async () => {
  try {
    loading.value = true
    const params = { page: 1, size: 20 }
    if (categoryId.value) {
      params.category_id = categoryId.value
    }
    const res = await articlesApi.list(params)
    articles.value = (res.data.items || []).map(item => ({
      id: item.id,
      title: item.title,
      excerpt: item.summary || '',
      date: new Date(item.create_time).toLocaleDateString('zh-CN'),
      category: item.category?.name || '',
      category_id: item.category_id || null,
      tag_list: item.tag_list || []
    }))
    hasMore.value = res.data.page < res.data.pages
  } catch (error) {
    console.error('加载文章失败:', error)
    articles.value = []
  } finally {
    loading.value = false
  }
}

const switchCategory = (id) => {
  if (id === categoryId.value) {
    router.push('/category')
  } else {
    router.push(`/category?category=${id}`)
  }
}

const loadMore = () => {
  // 实现加载更多逻辑
}

// 监听分类变化
watch(categoryId, () => {
  loadArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

onMounted(() => {
  loadCategories()
  loadArticles()
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--spacing-3xl);
  color: var(--color-text-tertiary);
}
</style>
