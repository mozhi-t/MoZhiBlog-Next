<template>
  <div class="category-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">{{ currentTitle }}</h1>
      <p class="page-description">共 {{ total }} 篇文章</p>
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
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </div>

    <!-- Empty State -->
    <div v-if="articles.length === 0 && !loading" class="empty-state">
      <p>暂无文章</p>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import Pagination from '../components/common/Pagination.vue'
import { articlesApi, categoriesApi } from '../api/frontend'
import { updateSeo } from '../utils/seo'

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
const currentPage = ref(1)
const total = ref(0)
const pageSize = 20

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
const loadArticles = async (page = 1) => {
  try {
    loading.value = true
    const params = { page, size: pageSize }
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
      tag_list: item.tag_list || [],
      type: item.type || 0,
      is_top: !!item.is_top,
      need_password: !!item.need_password,
      read_count: item.read_count || 0,
      content: item.content || '',
      create_time: item.create_time,
      update_time: item.update_time
    }))
    total.value = res.data.total || 0
    currentPage.value = page
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

const handlePageChange = (page) => {
  loadArticles(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(
  () => [categoryId.value, currentTitle.value, total.value],
  ([id, title, articleTotal]) => {
    const path = id ? `/category?category=${id}` : '/category'
    const description = id
      ? `${title} 分类下当前共有 ${articleTotal} 篇文章，聚合展示该主题的最新内容与相关文章。`
      : `浏览博客的全部分类，目前共收录 ${categories.value.length} 个分类，方便按主题查找文章。`

    updateSeo({
      title: id ? `${title} 分类` : '分类',
      description,
      path,
      keywords: id ? ['分类', title, `${title} 分类`] : ['分类', '文章分类', '博客分类']
    })
  },
  { immediate: true }
)

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
