<template>
  <div class="moments-page">
    <div class="page-header">
      <h1 class="page-title">说说管理</h1>
      <button class="add-btn" @click="openModal()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        新增说说
      </button>
    </div>

    <div class="moments-list">
      <article v-for="moment in moments" :key="moment.id" class="moment-card">
        <div class="moment-head">
          <div>
            <div class="moment-time">{{ formatDateTime(moment.create_time) }}</div>
          </div>
          <span class="status-pill" :class="{ protected: moment.has_password }">
            {{ moment.has_password ? '已加密' : '公开' }}
          </span>
        </div>

        <p class="moment-content">{{ moment.content }}</p>

        <div class="moment-actions">
          <button class="action-btn edit" @click="openModal(moment)">编辑</button>
          <button class="action-btn delete" @click="handleDelete(moment.id)">删除</button>
        </div>
      </article>

      <div v-if="!moments.length" class="empty-tip">暂无说说</div>
    </div>

    <div class="pagination" v-if="total > 0">
      <button class="page-btn" :disabled="page <= 1" @click="page--; loadMoments()">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button class="page-btn" :disabled="page >= totalPages" @click="page++; loadMoments()">下一页</button>
    </div>

    <Transition name="modal-pop">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <h2>{{ editingId ? '编辑说说' : '新增说说' }}</h2>
            <button class="close-btn" @click="closeModal">×</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>内容</label>
              <textarea
                v-model="form.content"
                class="form-textarea"
                rows="8"
                placeholder="记录这一刻想说的话"
              ></textarea>
            </div>

            <div class="form-group">
              <label>创建时间</label>
              <input
                v-model="form.create_time"
                type="datetime-local"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label>访问密码</label>
              <input
                v-model="form.access_password"
                type="text"
                class="form-input"
                placeholder="留空表示无需密码"
              />
            </div>

            <p class="field-tip">留空则保留原密码，输入 @@ 则取消加密，输入其它内容则更新密码</p>
          </div>

          <div class="modal-footer">
            <button class="cancel-btn" @click="closeModal">取消</button>
            <button class="submit-btn" :disabled="submitting" @click="handleSubmit">
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { momentApi } from '@/api'

const moments = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)
const showModal = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const form = reactive({
  content: '',
  access_password: '',
  create_time: ''
})

const totalPages = computed(() => Math.ceil(total.value / size.value))

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', { hour12: false })
}

const toDatetimeLocal = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hour}:${minute}`
}

const normalizeDatetime = (value) => {
  if (!value) return null
  return value.length === 16 ? `${value}:00` : value
}

const loadMoments = async () => {
  try {
    const res = await momentApi.list({
      page: page.value,
      size: size.value
    })
    moments.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (error) {
    console.error('加载说说失败:', error)
  }
}

const resetForm = () => {
  editingId.value = null
  form.content = ''
  form.access_password = ''
  form.create_time = toDatetimeLocal(new Date())
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const openModal = (moment = null) => {
  if (moment) {
    editingId.value = moment.id
    form.content = moment.content || ''
    form.access_password = ''
    form.create_time = toDatetimeLocal(moment.create_time)
  } else {
    resetForm()
  }

  showModal.value = true
}

const handleSubmit = async () => {
  if (!form.content.trim()) {
    alert('请输入说说内容')
    return
  }

  try {
    submitting.value = true
    const payload = {
      content: form.content.trim(),
      access_password: form.access_password.trim(),
      create_time: normalizeDatetime(form.create_time)
    }

    if (editingId.value) {
      await momentApi.update(editingId.value, payload)
    } else {
      await momentApi.create(payload)
    }

    closeModal()
    await loadMoments()
  } catch (error) {
    console.error('保存说说失败:', error)
    alert(`保存失败: ${error.message}`)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定删除这条说说吗？')) return

  try {
    await momentApi.delete(id)
    await loadMoments()
  } catch (error) {
    console.error('删除说说失败:', error)
    alert(`删除失败: ${error.message}`)
  }
}

onMounted(() => {
  resetForm()
  loadMoments()
})
</script>

<style lang="scss" scoped>
.moments-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.moments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.moment-card {
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  transition: background var(--transition-base), box-shadow var(--transition-base);

  &:hover {
    background: var(--color-bg-tertiary);
  }
}

.moment-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.moment-time {
  color: var(--color-text-primary);
  font-weight: 600;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  font-size: 11px;
  font-weight: 600;
  color: #047857;
  background: rgba(16, 185, 129, 0.14);
  border-color: rgba(16, 185, 129, 0.2);

  &.protected {
    color: #b45309;
    background: rgba(245, 158, 11, 0.16);
    border-color: rgba(245, 158, 11, 0.24);
  }
}

.moment-content {
  margin: 0;
  color: var(--color-text-primary);
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
}

.moment-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

.action-btn,
.page-btn,
.cancel-btn,
.submit-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);
}

.action-btn.edit {
  color: var(--color-accent);
  background: var(--color-accent-light);

  &:hover {
    background: var(--color-accent);
    color: #fff;
  }
}

.action-btn.delete {
  color: #dc2626;
  background: rgba(239, 68, 68, 0.12);

  &:hover {
    background: #ff3b30;
    color: #fff;
  }
}

.empty-tip {
  padding: var(--spacing-2xl);
  text-align: center;
  color: var(--color-text-tertiary);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.page-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-sm);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);

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

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  background: rgba(0, 0, 0, 0.5);
}

.modal {
  width: min(100%, 680px);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transform-origin: center;
}

.modal-header,
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) var(--spacing-xl);
}

.modal-header {
  border-bottom: 1px solid var(--color-divider);
}

.modal-body {
  padding: var(--spacing-xl);
}

.form-group + .form-group {
  margin-top: var(--spacing-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.form-input,
.form-textarea {
  width: 100%;
  box-sizing: border-box;
  padding: var(--spacing-md);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;

  &:focus {
    border-color: var(--color-accent);
  }
}

.form-input {
  min-height: 46px;
  line-height: 1.4;
}

input[type="datetime-local"].form-input,
input[type="text"].form-input {
  appearance: none;
  -webkit-appearance: none;
}

.form-textarea {
  resize: vertical;
}

.field-tip {
  margin: var(--spacing-sm) 0 0;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
  line-height: 1.5;
}

.cancel-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-md);

  &:hover {
    background: var(--color-bg-primary);
  }
}

.submit-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  color: #fff;
  background: var(--color-accent);
  border-radius: var(--radius-md);

  &:hover {
    background: var(--color-accent-hover);
  }
}

.close-btn {
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 24px;
  cursor: pointer;
}

.modal-pop-enter-active,
.modal-pop-leave-active {
  transition: opacity 220ms ease;
}

.modal-pop-enter-active .modal,
.modal-pop-leave-active .modal {
  transition:
    transform 340ms cubic-bezier(0.22, 1, 0.36, 1),
    opacity 240ms ease;
}

.modal-pop-enter-from,
.modal-pop-leave-to {
  opacity: 0;
}

.modal-pop-enter-from .modal {
  opacity: 0;
  transform: scale(0.88);
}

.modal-pop-leave-to .modal {
  opacity: 0;
  transform: scale(0.94);
}

</style>
