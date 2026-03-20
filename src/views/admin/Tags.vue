<template>
  <div class="tags-page">
    <div class="page-header">
      <h1 class="page-title">标签管理</h1>
    </div>

    <!-- 新增标签 -->
    <div class="add-form">
      <input
        v-model="newTagName"
        type="text"
        class="form-input"
        placeholder="请输入新标签名称"
        @keyup.enter="handleAdd"
      />
      <button class="add-btn" @click="handleAdd" :disabled="!newTagName.trim()">
        新增标签
      </button>
    </div>

    <!-- 标签列表 -->
    <div class="tags-list">
      <div
        v-for="tag in tags"
        :key="tag.id"
        class="tag-card"
      >
        <div class="tag-info">
          <span class="tag-name">{{ tag.name }}</span>
        </div>
        <div class="tag-actions">
          <button class="action-btn edit" @click="handleEdit(tag)">编辑</button>
          <button class="action-btn delete" @click="handleDelete(tag.id)">
            删除
          </button>
        </div>
      </div>

      <div v-if="!tags.length" class="empty-tip">暂无标签</div>
    </div>

    <!-- 编辑弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>编辑标签</h2>
          <button class="close-btn" @click="showModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>标签名称</label>
            <input
              v-model="editName"
              type="text"
              class="form-input"
              placeholder="请输入标签名称"
            />
          </div>
        </div>

        <div class="modal-footer">
          <button class="cancel-btn" @click="showModal = false">取消</button>
          <button class="submit-btn" @click="handleUpdate" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tagApi } from '@/api'

const tags = ref([])
const newTagName = ref('')
const showModal = ref(false)
const editingId = ref(null)
const editName = ref('')
const submitting = ref(false)

// 加载标签列表
const loadTags = async () => {
  try {
    const res = await tagApi.list()
    tags.value = res.data || []
  } catch (error) {
    console.error('加载标签失败:', error)
  }
}

const handleAdd = async () => {
  const name = newTagName.value.trim()
  if (!name) return

  try {
    await tagApi.create({ name })
    newTagName.value = ''
    loadTags()
  } catch (error) {
    console.error('添加标签失败:', error)
    alert('添加失败: ' + error.message)
  }
}

const handleEdit = (tag) => {
  editingId.value = tag.id
  editName.value = tag.name
  showModal.value = true
}

const handleUpdate = async () => {
  const name = editName.value.trim()
  if (!name || !editingId.value) return

  submitting.value = true
  try {
    await tagApi.update(editingId.value, { name })
    showModal.value = false
    loadTags()
  } catch (error) {
    console.error('更新标签失败:', error)
    alert('更新失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个标签吗？')) return

  try {
    await tagApi.delete(id)
    loadTags()
  } catch (error) {
    console.error('删除标签失败:', error)
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadTags()
})
</script>

<style lang="scss" scoped>
.tags-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
}

.add-form {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  align-items: center;
}

.form-input {
  flex: 1;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-sm);
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

.add-btn {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.tags-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.tag-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);

  &:hover {
    box-shadow: var(--shadow-md);
  }
}

.tag-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.tag-name {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-primary);
}

.tag-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

.tag-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--font-size-sm);
  border: none;
  border-radius: var(--radius-md);
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

.empty-tip {
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-2xl);
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
  max-width: 400px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
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
  padding: var(--spacing-xl);
}

.form-group {
  margin-bottom: var(--spacing-lg);

  &:last-child {
    margin-bottom: 0;
  }

  label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-sm);
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
