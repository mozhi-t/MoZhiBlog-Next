<template>
  <div class="search-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">搜索结果</h1>
      <p class="page-description">关键词: "{{ keyword }}" - 共找到 {{ total }} 篇文章</p>
    </header>

    <!-- Search Input -->
    <div class="search-bar">
      <input
        type="text"
        v-model="keyword"
        placeholder="输入关键词搜索..."
        @keyup.enter="handleSearch"
        class="search-input"
      />
      <button class="search-btn" @click="handleSearch">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <!-- Articles List -->
    <div class="articles-list">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </div>

    <!-- Empty State -->
    <div v-if="articles.length === 0 && !loading" class="empty-state">
      <p>未找到相关文章</p>
    </div>

    <!-- Pagination -->
    <Pagination
      v-if="total > pageSize"
      :current-page="currentPage"
      :total="total"
      :page-size="pageSize"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import Pagination from '../components/common/Pagination.vue'
import { articlesApi } from '../api/frontend'

const route = useRoute()
const router = useRouter()

// 搜索关键词
const keyword = ref(route.query.q || '')

// 文章列表
const articles = ref([])
const loading = ref(true)
const currentPage = ref(1)
const total = ref(0)
const pageSize = 20

// 搜索
const handleSearch = () => {
  if (keyword.value.trim()) {
    router.push({ path: '/search', query: { q: keyword.value.trim() } })
  }
}

// 获取搜索结果
const fetchArticles = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize,
      keyword: keyword.value
    }
    const data = await articlesApi.list(params)
    articles.value = data.list || []
    total.value = data.total || 0
  } catch (error) {
    console.error('搜索失败:', error)
    articles.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 页码变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 监听路由变化
watch(
  () => route.query.q,
  (newQ) => {
    keyword.value = newQ || ''
    currentPage.value = 1
    fetchArticles()
  },
  { immediate: true }
)

onMounted(() => {
  if (keyword.value) {
    fetchArticles()
  }
})
</script>

<style lang="scss" scoped>
/* ============================================
   Search Page - 搜索页
   ============================================ */
.search-page {
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

/* Search Bar */
.search-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  max-width: 600px;
  margin: 0 auto var(--spacing-2xl);
  padding: var(--spacing-sm);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.search-input {
  flex: 1;
  padding: var(--spacing-md);
  background: transparent;
  border: none;
  outline: none;
  font-size: var(--font-size-base);
  color: var(--color-text-primary);

  &::placeholder {
    color: var(--color-text-tertiary);
  }
}

.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 20px;
    height: 20px;
    color: white;
  }

  &:hover {
    background: var(--color-accent-hover);
    transform: scale(1.05);
  }
}

/* Articles List */
.articles-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--spacing-xxl);
  color: var(--color-text-tertiary);
  font-size: var(--font-size-lg);
}

/* Responsive */
@media (max-width: 768px) {
  .search-page {
    padding: calc(var(--nav-height) + 20px) var(--spacing-md) var(--spacing-xl);
  }

  .page-title {
    font-size: var(--font-size-3xl);
  }
}
</style>
