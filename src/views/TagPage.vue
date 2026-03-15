<template>
  <div class="tag-page">
    <header class="page-header">
      <h1 class="page-title">标签</h1>
      <p class="page-description">共 {{ tags.length }} 个标签</p>
    </header>

    <div class="tags-grid">
      <div
        v-for="tag in tags"
        :key="tag.id"
        class="tag-box"
        :class="{ active: selectedTag === tag.id }"
        :style="{ '--tag-color': tag.color || '#007AFF' }"
        @click="selectTag(tag)"
      >
        <span class="tag-name">{{ tag.name }}</span>
      </div>
    </div>

    <div v-if="tags.length === 0 && !loading" class="empty-state">
      <p>暂无标签</p>
    </div>

    <div v-if="selectedTag && articles.length > 0" class="tag-articles">
      <h2 class="section-title">{{ selectedTagName }} 下的文章</h2>
      <div class="articles-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
      </div>

      <Pagination
        v-if="total > pageSize"
        :current-page="currentPage"
        :total="total"
        :page-size="pageSize"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import Pagination from '../components/common/Pagination.vue'
import { tagsApi, articlesApi } from '../api/frontend'
import { updateSeo } from '../utils/seo'

const route = useRoute()
const router = useRouter()

const tags = ref([])
const loading = ref(true)
const articles = ref([])
const currentPage = ref(1)
const total = ref(0)
const pageSize = 20

const selectedTag = computed(() => {
  const id = route.query.tag
  return id ? parseInt(id, 10) : null
})

const selectedTagName = computed(() => {
  if (!selectedTag.value) return ''
  const tag = tags.value.find(item => item.id === selectedTag.value)
  return tag ? tag.name : ''
})

const loadTags = async () => {
  try {
    loading.value = true
    const res = await tagsApi.list()
    tags.value = res.data || []
  } catch (error) {
    console.error('加载标签失败:', error)
    tags.value = []
  } finally {
    loading.value = false
  }
}

const selectTag = (tag) => {
  if (selectedTag.value === tag.id) {
    router.push('/tag')
    return
  }

  router.push(`/tag?tag=${tag.id}`)
}

const loadArticlesByTag = async (tagId, page = 1) => {
  try {
    const res = await articlesApi.list({ tag_id: tagId, page, size: pageSize })
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
    console.error('加载标签文章失败:', error)
    articles.value = []
    total.value = 0
  }
}

const handlePageChange = (page) => {
  loadArticlesByTag(selectedTag.value, page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(
  () => selectedTag.value,
  (tagId) => {
    currentPage.value = 1

    if (!tagId) {
      articles.value = []
      total.value = 0
      return
    }

    loadArticlesByTag(tagId, 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  },
  { immediate: true }
)

watch(
  () => [selectedTag.value, selectedTagName.value, total.value, tags.value.length],
  ([tagId, tagName, articleTotal, tagTotal]) => {
    const path = tagId ? `/tag?tag=${tagId}` : '/tag'
    const description = tagId
      ? `查看标签“${tagName}”下的 ${articleTotal} 篇相关文章，快速聚合同主题内容。`
      : `浏览博客全部标签，目前共收录 ${tagTotal} 个标签，方便快速定位相关文章。`

    updateSeo({
      title: tagId ? `${tagName} 标签` : '标签',
      description,
      path,
      keywords: tagId ? ['标签', tagName, `${tagName} 标签`] : ['标签', '文章标签', '博客标签']
    })
  },
  { immediate: true }
)

onMounted(() => {
  loadTags()
})
</script>

<style lang="scss" scoped>
/* ============================================
   Tag Page - 标签页
   ============================================ */
.tag-page {
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

.page-description {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
}

.tags-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-3xl);
}

.tag-box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 2px solid var(--tag-color);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--tag-color);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--tag-color);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.active {
    background: var(--tag-color);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.tag-name {
  white-space: nowrap;
}

.tag-articles {
  margin-top: var(--spacing-2xl);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

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

  .tags-grid {
    gap: var(--spacing-sm);
  }

  .tag-box {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
  }
}

.empty-state {
  text-align: center;
  padding: var(--spacing-3xl);
  color: var(--color-text-tertiary);
}
</style>
