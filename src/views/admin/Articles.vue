<template>
  <div class="articles-page">
    <div class="page-header">
      <h1 class="page-title">文章管理</h1>
      <button class="add-btn" @click="openModal()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        新增文章
      </button>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <select v-model="filter.categoryId" class="filter-select" @change="loadArticles">
        <option :value="null">全部分类</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>

      <select v-model="filter.tagId" class="filter-select" @change="loadArticles">
        <option :value="null">全部标签</option>
        <option v-for="tag in tags" :key="tag.id" :value="tag.id">
          {{ tag.name }}
        </option>
      </select>
    </div>

    <!-- 文章列表 -->
    <div class="articles-table">
      <table>
        <thead>
          <tr>
            <th>标题</th>
            <th>分类</th>
            <th>标签</th>
            <th>属性</th>
            <th>阅读量</th>
            <th>发布时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td class="title-cell">{{ article.title }}</td>
            <td>
              <span class="category-tag" v-if="article.category">
                {{ article.category.name }}
              </span>
              <span class="text-muted" v-else>-</span>
            </td>
            <td>
              <span class="tag" v-for="tag in article.tag_list" :key="tag.id">{{ tag.name }}</span>
              <span class="text-muted" v-if="!article.tag_list || article.tag_list.length === 0">-</span>
            </td>
            <td>
              <span class="attr-badge" :class="articleAttrClass(article.type)">{{ articleAttrText(article.type) }}</span>
            </td>
            <td>{{ article.read_count }}</td>
            <td class="time-cell">{{ formatDate(article.create_time) }}</td>
            <td>
              <div class="actions">
                <button class="action-btn edit" @click="openModal(article)">编辑</button>
                <button class="action-btn delete" @click="handleDelete(article.id)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!articles.length" class="empty-tip">暂无文章</div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <button
        class="page-btn"
        :disabled="page <= 1"
        @click="page--; loadArticles()"
      >上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button
        class="page-btn"
        :disabled="page >= totalPages"
        @click="page++; loadArticles()"
      >下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi, categoryApi, tagApi } from '@/api'

const router = useRouter()

// 数据
const articles = ref([])
const categories = ref([])
const tags = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)

const filter = reactive({
  categoryId: null,
  tagId: null
})

const openModal = (article = null) => {
  if (article) {
    router.push(`/admin/articles/${article.id}/edit`)
  } else {
    router.push('/admin/articles/new')
  }
}

// 计算属性
const totalPages = computed(() => Math.ceil(total.value / size.value))

const articleAttrText = (type) => {
  if (type === 1) return '置顶'
  if (type === 2) return '密码'
  return '普通'
}

const articleAttrClass = (type) => {
  if (type === 1) return 'top'
  if (type === 2) return 'password'
  return 'normal'
}

// 方法
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const loadArticles = async () => {
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (filter.categoryId) params.category_id = filter.categoryId
    if (filter.tagId) params.tag_id = filter.tagId

    const res = await articleApi.list(params)
    articles.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error('加载文章失败:', error)
  }
}

const loadCategories = async () => {
  try {
    const res = await categoryApi.list()
    categories.value = res.data
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const loadTags = async () => {
  try {
    const res = await tagApi.list()
    tags.value = res.data
  } catch (error) {
    console.error('加载标签失败:', error)
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这篇文章吗？')) return

  try {
    await articleApi.delete(id)
    loadArticles()
  } catch (error) {
    console.error('删除文章失败:', error)
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadArticles()
  loadCategories()
  loadTags()
})
</script>

<style lang="scss" scoped>
.articles-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    background: var(--color-accent-hover);
    transform: translateY(-1px);
  }
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.filter-select {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  cursor: pointer;

  &:focus {
    border-color: var(--color-accent);
  }
}

.articles-table {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: var(--spacing-md) var(--spacing-lg);
    text-align: left;
    border-bottom: 1px solid var(--color-divider);
  }

  th {
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--color-text-secondary);
    background: var(--color-bg-tertiary);
  }

  td {
    font-size: var(--font-size-sm);
    color: var(--color-text-primary);
  }

  tbody tr {
    transition: background var(--transition-base);

    &:hover {
      background: var(--color-bg-tertiary);
    }
  }
}

.title-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.category-tag {
  display: inline-block;
  padding: 2px 8px;
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  background: var(--color-accent-light);
  border-radius: var(--radius-sm);
}

.attr-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;

  &.normal {
    color: var(--color-text-secondary);
    background: var(--color-bg-tertiary);
  }

  &.top {
    color: #b85c00;
    background: rgba(255, 183, 77, 0.22);
  }

  &.password {
    color: #8a3ffc;
    background: rgba(138, 63, 252, 0.12);
  }
}

.tag {
  display: inline-block;
  padding: 2px 6px;
  font-size: 11px;
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-sm);
}

.time-cell {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
}

.actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);

  &.edit {
    color: var(--color-accent);
    background: var(--color-accent-light);

    &:hover {
      background: var(--color-accent);
      color: #fff;
    }
  }

  &.delete {
    color: #ff3b30;
    background: rgba(255, 59, 48, 0.1);

    &:hover {
      background: #ff3b30;
      color: #fff;
    }
  }
}

.text-muted {
  color: var(--color-text-tertiary);
}

.empty-tip {
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-2xl);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.page-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    border-color: var(--color-accent);
    color: var(--color-accent);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.page-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
</style>
