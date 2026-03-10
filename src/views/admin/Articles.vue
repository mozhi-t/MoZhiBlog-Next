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
              <span class="tag" v-if="article.tag">{{ article.tag.name }}</span>
              <span class="text-muted" v-else>-</span>
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

    <!-- 编辑弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? '编辑文章' : '新增文章' }}</h2>
          <button class="close-btn" @click="showModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>标题</label>
            <input v-model="form.title" type="text" class="form-input" placeholder="请输入文章标题" />
          </div>

          <div class="form-group">
            <label>摘要</label>
            <textarea v-model="form.summary" class="form-textarea" placeholder="请输入文章摘要" rows="3"></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>分类</label>
              <select v-model="form.category_id" class="form-select">
                <option :value="null">请选择分类</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>标签</label>
              <select v-model="form.tag_id" class="form-select">
                <option :value="null">请选择标签</option>
                <option v-for="tag in tags" :key="tag.id" :value="tag.id">
                  {{ tag.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>类型</label>
              <select v-model="form.type" class="form-select">
                <option :value="0">文章</option>
                <option :value="1">说说</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>内容 (Markdown)</label>
            <div class="editor-container">
              <textarea
                v-model="form.content"
                class="form-editor"
                placeholder="请输入文章内容 (支持 Markdown)"
              ></textarea>
              <div class="preview-pane" v-html="previewContent"></div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="cancel-btn" @click="showModal = false">取消</button>
          <button class="submit-btn" @click="handleSubmit" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { marked } from 'marked'
import { articleApi, categoryApi, tagApi } from '@/api'

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

const showModal = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const form = reactive({
  title: '',
  summary: '',
  content: '',
  category_id: null,
  tag_id: null,
  type: 0
})

// 计算属性
const totalPages = computed(() => Math.ceil(total.value / size.value))

const previewContent = computed(() => {
  if (!form.content) return ''
  return marked(form.content)
})

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

const openModal = (article = null) => {
  if (article) {
    editingId.value = article.id
    form.title = article.title
    form.summary = article.summary || ''
    form.content = article.content
    form.category_id = article.category_id
    form.tag_id = article.tag_id
    form.type = article.type || 0
  } else {
    editingId.value = null
    form.title = ''
    form.summary = ''
    form.content = ''
    form.category_id = null
    form.tag_id = null
    form.type = 0
  }
  showModal.value = true
}

const handleSubmit = async () => {
  if (!form.title || !form.content) return

  submitting.value = true
  try {
    const data = {
      title: form.title,
      summary: form.summary,
      content: form.content,
      category_id: form.category_id,
      tag_id: form.tag_id,
      type: form.type
    }

    if (editingId.value) {
      await articleApi.update(editingId.value, data)
    } else {
      await articleApi.create(data)
    }

    showModal.value = false
    loadArticles()
  } catch (error) {
    console.error('保存文章失败:', error)
    alert('保存失败: ' + error.message)
  } finally {
    submitting.value = false
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

// 弹窗样式
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-lg);
}

.modal {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modalSlide 0.3s ease;
}

@keyframes modalSlide {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--color-divider);

  h2 {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--color-text-primary);
  }
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: all var(--transition-base);

  svg {
    width: 20px;
    height: 20px;
  }

  &:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-text-primary);
  }
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-xl);
}

.form-group {
  margin-bottom: var(--spacing-lg);

  label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-sm);
  }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color var(--transition-base);

  &:focus {
    border-color: var(--color-accent);
  }
}

.form-textarea {
  resize: vertical;
}

.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  min-height: 300px;
}

.form-editor {
  width: 100%;
  min-height: 300px;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  font-family: monospace;
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  resize: vertical;

  &:focus {
    border-color: var(--color-accent);
  }
}

.preview-pane {
  min-height: 300px;
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow-y: auto;

  :deep(h1), :deep(h2), :deep(h3) {
    margin-top: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
  }

  :deep(p) {
    margin-bottom: var(--spacing-sm);
  }

  :deep(code) {
    padding: 2px 6px;
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-sm);
    font-family: monospace;
  }

  :deep(pre) {
    padding: var(--spacing-md);
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-md);
    overflow-x: auto;
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
}

.cancel-btn,
.submit-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.cancel-btn {
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary);
  border: none;

  &:hover {
    background: var(--color-bg-primary);
  }
}

.submit-btn {
  color: #fff;
  background: var(--color-accent);
  border: none;

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}
</style>
