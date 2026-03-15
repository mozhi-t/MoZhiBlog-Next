<template>
  <div class="editor-page">
    <!-- 顶部导航 -->
    <div class="editor-header">
      <button class="back-btn" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        返回列表
      </button>
      <h1 class="editor-title">{{ isEditing ? '编辑文章' : '新增文章' }}</h1>
      <div class="header-actions">
        <button class="save-btn" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>

    <!-- 消息提示 -->
    <Transition name="fade">
      <div v-if="message.show" class="message-toast" :class="message.type">
        {{ message.text }}
      </div>
    </Transition>

    <!-- 编辑器主体 -->
    <div class="editor-body">
      <!-- 左侧编辑区 -->
      <div class="editor-main">
        <!-- 标题 -->
        <div class="form-group">
          <label>标题</label>
          <input
            v-model="form.title"
            type="text"
            class="title-input"
            placeholder="请输入文章标题"
          />
        </div>

        <!-- 摘要 -->
        <div class="form-group">
          <label>摘要</label>
          <textarea
            v-model="form.summary"
            class="summary-input"
            placeholder="请输入文章摘要（选填）"
            rows="2"
          ></textarea>
        </div>

        <!-- 元信息 -->
        <div class="meta-row">
          <div class="meta-item">
            <label>分类</label>
            <select v-model="form.category_id" class="meta-select">
              <option :value="null">请选择分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="meta-item">
            <label>创建时间</label>
            <input
              v-model="form.create_time"
              type="datetime-local"
              class="meta-input"
            />
          </div>

          <div class="meta-item">
            <label>更新时间</label>
            <input
              v-model="form.update_time"
              type="datetime-local"
              class="meta-input"
            />
          </div>

          <div class="meta-item">
            <label>文章属性</label>
            <select v-model="form.type" class="meta-select">
              <option :value="0">普通文章</option>
              <option :value="1">置顶文章</option>
              <option :value="2">密码访问</option>
            </select>
          </div>
        </div>

        <div v-if="form.type === 2" class="form-group">
          <label>访问密码</label>
          <input
            v-model="form.access_password"
            type="password"
            class="meta-input"
            :placeholder="hasExistingPassword ? '留空则保留原密码，输入新值则覆盖' : '请输入文章访问密码'"
          />
          <p class="field-tip">密码不会随文章详情接口返回，访客需先校验密码才能查看正文。</p>
        </div>

        <!-- 标签多选 -->
        <div class="form-group">
          <label>标签</label>
          <div class="tags-selector">
            <div
              v-for="tag in tags"
              :key="tag.id"
              class="tag-option"
              :class="{ selected: form.tag_ids.includes(tag.id) }"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </div>
            <div v-if="!tags.length" class="no-tags">暂无标签</div>
          </div>
        </div>

        <!-- 内容编辑器 -->
        <div class="editor-container">
          <div class="editor-pane">
            <div class="pane-header">
              <span>编辑</span>
            </div>
            <textarea
              v-model="form.content"
              class="content-editor"
              placeholder="请输入文章内容 (支持 Markdown)"
            ></textarea>
          </div>
          <div class="preview-pane">
            <div class="pane-header">
              <span>预览</span>
            </div>
            <div class="preview-content" v-html="previewContent"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { articleApi, categoryApi, tagApi } from '@/api'

const route = useRoute()
const router = useRouter()

// 判断是编辑还是新增
const isEditing = computed(() => !!route.params.id)

// 表单数据
const form = reactive({
  title: '',
  summary: '',
  content: '',
  category_id: null,
  tag_ids: [],
  type: 0,
  access_password: '',
  create_time: '',
  update_time: ''
})

// 数据
const categories = ref([])
const tags = ref([])
const submitting = ref(false)
const hasExistingPassword = ref(false)

// 消息提示
const message = ref({
  show: false,
  text: '',
  type: 'success' // 'success' | 'error'
})

// 预览内容
const previewContent = computed(() => {
  if (!form.content) return '<p class="empty-preview">预览内容...</p>'
  return marked(form.content)
})

// 加载分类
const loadCategories = async () => {
  try {
    const res = await categoryApi.list()
    categories.value = res.data
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 加载标签
const loadTags = async () => {
  try {
    const res = await tagApi.list()
    tags.value = res.data
  } catch (error) {
    console.error('加载标签失败:', error)
  }
}

// 切换标签选中状态
const toggleTag = (tagId) => {
  const index = form.tag_ids.indexOf(tagId)
  if (index > -1) {
    form.tag_ids.splice(index, 1)
  } else {
    form.tag_ids.push(tagId)
  }
}

// 加载文章详情（编辑时）
const loadArticle = async () => {
  if (!isEditing.value) return

  try {
    const res = await articleApi.detail(route.params.id)
    const data = res.data

    form.title = data.title || ''
    form.summary = data.summary || ''
    form.content = data.content || ''
    form.category_id = data.category?.id || null
    form.type = data.type ?? 0
    hasExistingPassword.value = !!data.has_password
    form.access_password = ''

    // 设置标签
    if (data.tag_list && data.tag_list.length > 0) {
      form.tag_ids = data.tag_list.map(t => t.id)
    }

    // 格式化时间
    if (data.create_time) {
      form.create_time = formatDateForInput(data.create_time)
    }
    if (data.update_time) {
      form.update_time = formatDateForInput(data.update_time)
    }
  } catch (error) {
    console.error('加载文章失败:', error)
    alert('加载文章失败: ' + error.message)
    router.push('/admin/articles')
  }
}

// 格式化时间为 datetime-local 输入框格式
// 后端返回的是本地时间字符串（如 "2024-03-12T00:00:00"），直接截取即可
const formatDateForInput = (dateStr) => {
  if (!dateStr) return ''
  // 直接处理字符串，去掉可能的 Z 后缀，截取到分钟
  return dateStr.replace('Z', '').slice(0, 16)
}

// 返回列表
const goBack = () => {
  router.push('/admin/articles')
}

// 显示消息提示
const showMessage = (text, type = 'success') => {
  message.value = {
    show: true,
    text,
    type
  }
  setTimeout(() => {
    message.value.show = false
  }, 2000)
}

// 保存文章
const handleSubmit = async () => {
  if (!form.title || !form.content) {
    showMessage('请填写标题和内容', 'error')
    return
  }

  if (form.type === 2 && !form.access_password.trim() && !hasExistingPassword.value) {
    showMessage('密码访问文章必须设置访问密码', 'error')
    return
  }

  submitting.value = true
  try {
    const data = {
      title: form.title,
      summary: form.summary,
      content: form.content,
      category_id: form.category_id,
      type: form.type,
      tags: form.tag_ids.length > 0 ? form.tag_ids.join(',') : ''
    }

    if (form.type === 2 && form.access_password.trim()) {
      data.access_password = form.access_password.trim()
    }

    // 如果填写了时间，则添加到请求中
    // 直接使用 datetime-local 的值，不再转换为 ISO 格式
    if (form.create_time) {
      data.create_time = form.create_time
    }
    if (form.update_time) {
      data.update_time = form.update_time
    }

    if (isEditing.value) {
      await articleApi.update(route.params.id, data)
    } else {
      await articleApi.create(data)
    }

    showMessage('保存成功', 'success')
    setTimeout(() => {
      router.push('/admin/articles')
    }, 1000)
  } catch (error) {
    console.error('保存文章失败:', error)
    showMessage('保存失败: ' + error.message, 'error')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadCategories()
  loadTags()
  loadArticle()
})
</script>

<style lang="scss" scoped>
.editor-page {
  min-height: 100vh;
  background: var(--color-bg-primary);
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 16px;
    height: 16px;
  }

  &:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-text-primary);
  }
}

.editor-title {
  flex: 1;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.save-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.editor-body {
  flex: 1;
  padding: var(--spacing-xl);
}

.editor-main {
  max-width: 1400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: var(--spacing-lg);

  label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-sm);
  }
}

.title-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  outline: none;
  transition: border-color var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
  }
}

.summary-input {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  resize: vertical;
  transition: border-color var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
  }
}

.field-tip {
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.meta-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.meta-item {
  label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-sm);
  }
}

.meta-select,
.meta-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color var(--transition-base);

  &:focus {
    border-color: var(--color-accent);
  }
}

.meta-input {
  cursor: pointer;
}

// 标签选择器
.tags-selector {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.tag-option {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
  }

  &.selected {
    background: var(--color-accent-light);
    border-color: var(--color-accent);
    color: var(--color-accent);
  }
}

.no-tags {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

// 编辑器容器
.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  min-height: 500px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.editor-pane,
.preview-pane {
  display: flex;
  flex-direction: column;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.pane-header {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary);
  border-bottom: 1px solid var(--color-border);
}

.content-editor {
  flex: 1;
  width: 100%;
  min-height: 450px;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
  line-height: 1.6;
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: none;
  outline: none;
  resize: none;

  &::placeholder {
    color: var(--color-text-tertiary);
  }
}

.preview-content {
  flex: 1;
  min-height: 450px;
  padding: var(--spacing-md);
  overflow-y: auto;

  :deep(h1), :deep(h2), :deep(h3), :deep(h4) {
    margin-top: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
    color: var(--color-text-primary);
  }

  :deep(p) {
    margin-bottom: var(--spacing-sm);
    color: var(--color-text-primary);
    line-height: 1.7;
  }

  :deep(code) {
    padding: 2px 6px;
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-sm);
    font-family: monospace;
    font-size: 13px;
  }

  :deep(pre) {
    padding: var(--spacing-md);
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-md);
    overflow-x: auto;

    code {
      padding: 0;
      background: none;
    }
  }

  :deep(blockquote) {
    margin: var(--spacing-md) 0;
    padding: var(--spacing-sm) var(--spacing-md);
    border-left: 4px solid var(--color-accent);
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
  }

  :deep(img) {
    max-width: 100%;
    border-radius: var(--radius-md);
  }

  :deep(ul), :deep(ol) {
    padding-left: var(--spacing-lg);
    margin: var(--spacing-sm) 0;
  }

  :deep(li) {
    margin: var(--spacing-xs) 0;
    color: var(--color-text-primary);
  }

  .empty-preview {
    color: var(--color-text-tertiary);
    font-style: italic;
  }
}

// 消息提示弹窗
.message-toast {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: #fff;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

  &.success {
    background: #34c759;
  }

  &.error {
    background: #ff3b30;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px);
}
</style>
