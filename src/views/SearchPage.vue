<template>
  <div class="search-page">
    <header class="page-header">
      <h1 class="page-title">搜索结果</h1>
      <p v-if="hasActiveKeyword" class="page-description">
        关键词“{{ activeKeyword }}”共找到 {{ total }} 篇相关文章
      </p>
      <p v-else class="page-description">
        输入关键词搜索站内文章
      </p>
    </header>

    <div class="search-bar">
      <input
        v-model="keyword"
        type="text"
        class="search-input"
        placeholder="输入关键词搜索..."
        @keyup.enter="handleSearch"
      />
      <button class="search-btn" @click="handleSearch" aria-label="搜索">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2" />
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
    </div>

    <div v-if="!hasActiveKeyword" class="state-panel">
      <p>输入标题、摘要或正文关键词开始搜索。</p>
    </div>

    <div v-else-if="loading" class="state-panel">
      <p>搜索中...</p>
    </div>

    <template v-else>
      <div v-if="articles.length > 0" class="articles-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :highlight-keyword="activeKeyword"
        />
      </div>

      <div v-else class="state-panel">
        <p>没有找到相关文章，换个关键词试试。</p>
      </div>

      <Pagination
        v-if="total > pageSize"
        :current-page="currentPage"
        :total="total"
        :page-size="pageSize"
        :total-pages="totalPages"
        @page-change="handlePageChange"
      />
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import Pagination from '../components/common/Pagination.vue'
import { articlesApi } from '../api/frontend'
import { updateSeo } from '../utils/seo'

const route = useRoute()
const router = useRouter()

const pageSize = 20

const keyword = ref(typeof route.query.q === 'string' ? route.query.q : '')
const activeKeyword = ref('')
const articles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const total = ref(0)
const totalPages = ref(0)

const hasActiveKeyword = computed(() => activeKeyword.value.length > 0)

const mapArticle = (item) => ({
  id: item.id,
  title: item.title,
  excerpt: item.summary || '',
  date: item.create_time ? new Date(item.create_time).toLocaleDateString('zh-CN') : '',
  category: item.category?.name || '',
  category_id: item.category_id || null,
  tag_list: item.tag_list || [],
  type: item.type || 0,
  is_top: !!item.is_top,
  need_password: !!item.need_password,
  read_count: item.read_count || 0,
  content: item.content || '',
  create_time: item.create_time,
  update_time: item.update_time
})

const syncStateFromRoute = () => {
  keyword.value = typeof route.query.q === 'string' ? route.query.q : ''
  activeKeyword.value = keyword.value.trim()

  const nextPage = Number.parseInt(String(route.query.page || '1'), 10)
  currentPage.value = Number.isFinite(nextPage) && nextPage > 0 ? nextPage : 1
}

const fetchArticles = async () => {
  const trimmedKeyword = activeKeyword.value
  if (!trimmedKeyword) {
    articles.value = []
    total.value = 0
    totalPages.value = 0
    loading.value = false
    return
  }

  loading.value = true
  try {
    const res = await articlesApi.list({
      page: currentPage.value,
      size: pageSize,
      keyword: trimmedKeyword
    })

    const data = res.data || {}
    const items = Array.isArray(data.items) ? data.items : []

    articles.value = items.map(mapArticle)
    total.value = data.total || 0
    totalPages.value = data.pages || 0
  } catch (error) {
    console.error('搜索失败:', error)
    articles.value = []
    total.value = 0
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  const trimmedKeyword = keyword.value.trim()
  if (!trimmedKeyword) {
    router.push({ path: '/search' })
    return
  }

  router.push({
    path: '/search',
    query: { q: trimmedKeyword, page: '1' }
  })
}

const handlePageChange = (page) => {
  const trimmedKeyword = keyword.value.trim()
  if (!trimmedKeyword) {
    return
  }

  router.push({
    path: '/search',
    query: {
      q: trimmedKeyword,
      page: String(page)
    }
  })

  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(
  () => [route.query.q, route.query.page],
  () => {
    syncStateFromRoute()
    fetchArticles()
  },
  { immediate: true }
)

watch(
  () => [activeKeyword.value, total.value, currentPage.value],
  ([currentKeyword, articleTotal]) => {
    updateSeo({
      title: currentKeyword ? `搜索：${currentKeyword}` : '搜索',
      description: currentKeyword
        ? `站内搜索“${currentKeyword}”的结果页，共找到 ${articleTotal} 篇相关文章。`
        : '站内文章搜索页，用于按关键词查找博客内容。',
      path: currentKeyword
        ? `/search?q=${encodeURIComponent(currentKeyword)}&page=${currentPage.value}`
        : '/search',
      keywords: ['搜索', currentKeyword].filter(Boolean),
      noindex: true
    })
  },
  { immediate: true }
)
</script>

<style lang="scss" scoped>
.search-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.page-title {
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.page-description {
  font-size: var(--font-size-lg);
  color: var(--color-text-tertiary);
}

.search-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  max-width: 600px;
  margin: 0 auto var(--spacing-2xl);
  padding: var(--spacing-sm);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
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
    color: #fff;
  }

  &:hover {
    background: var(--color-accent-hover);
    transform: scale(1.05);
  }
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.state-panel {
  padding: var(--spacing-xxl);
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-lg);
}

@media (max-width: 768px) {
  .search-page {
    padding: calc(var(--nav-height) + 20px) var(--spacing-md) var(--spacing-xl);
  }

  .page-title {
    font-size: var(--font-size-3xl);
  }
}
</style>
