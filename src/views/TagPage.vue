<template>
  <div class="tag-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">标签</h1>
      <p class="page-description">共 {{ tags.length }} 个标签</p>
    </header>

    <!-- Tags Grid -->
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

    <!-- Empty State -->
    <div v-if="tags.length === 0 && !loading" class="empty-state">
      <p>暂无标签</p>
    </div>

    <!-- Selected Tag Articles -->
    <div v-if="selectedTag && articles.length > 0" class="tag-articles">
      <h2 class="section-title">{{ selectedTagName }} 下的文章</h2>
      <div class="articles-list">
        <ArticleCard
          v-for="(article, index) in articles"
          :key="article.id"
          :article="article"
          :style="{ transitionDelay: `${index * 0.1}s` }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArticleCard from '../components/common/ArticleCard.vue'
import { tagsApi, articlesApi } from '../api/frontend'

const router = useRouter()

const tags = ref([])
const loading = ref(true)
const selectedTag = ref(null)
const articles = ref([])

const selectedTagName = computed(() => {
  if (selectedTag.value) {
    const tag = tags.value.find(t => t.id === selectedTag.value)
    return tag ? tag.name : ''
  }
  return ''
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

const selectTag = async (tag) => {
  if (selectedTag.value === tag.id) {
    // 取消选择
    selectedTag.value = null
    articles.value = []
  } else {
    selectedTag.value = tag.id
    // 加载该标签下的文章
    try {
      const res = await articlesApi.list({ tag_id: tag.id, page: 1, size: 20 })
      articles.value = (res.data.items || []).map(item => ({
        id: item.id,
        title: item.title,
        excerpt: item.summary || '',
        date: new Date(item.create_time).toLocaleDateString('zh-CN'),
        category: item.category?.name || '',
        category_id: item.category_id || null,
        tag_list: item.tag_list || []
      }))
    } catch (error) {
      console.error('加载文章失败:', error)
      articles.value = []
    }
  }
}

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

/* Page Header */
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

/* Tags Grid */
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

/* Selected Tag Articles */
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--spacing-3xl);
  color: var(--color-text-tertiary);
}
</style>
