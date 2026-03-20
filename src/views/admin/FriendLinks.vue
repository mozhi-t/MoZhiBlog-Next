<template>
  <div class="friend-links-page">
    <div class="page-header">
      <h1 class="page-title">友链管理</h1>
      <button class="add-btn" @click="openModal()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        新增友链
      </button>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === '' }"
        @click="filter.isShow = ''; loadLinks()"
      >全部</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === 1 }"
        @click="filter.isShow = 1; loadLinks()"
      >展示中</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === 0 }"
        @click="filter.isShow = 0; loadLinks()"
      >已隐藏</button>
      <span class="filter-divider">|</span>
      <button
        class="filter-btn"
        :class="{ active: filter.weight === '' }"
        @click="filter.weight = ''; loadLinks()"
      >全部类型</button>
      <button
        class="filter-btn"
        :class="{ active: filter.weight === 0 }"
        @click="filter.weight = 0; loadLinks()"
      >挚友</button>
      <button
        class="filter-btn"
        :class="{ active: filter.weight === 1 }"
        @click="filter.weight = 1; loadLinks()"
      >朋友</button>
      <button
        class="filter-btn"
        :class="{ active: filter.weight === 2 }"
        @click="filter.weight = 2; loadLinks()"
      >来客</button>
    </div>

    <!-- 友链列表 -->
    <div class="links-grid">
      <div
        v-for="link in links"
        :key="link.id"
        class="link-card"
      >
        <div class="link-icon">
          <img v-if="link.icon_url" :src="link.icon_url" alt="icon" />
          <div v-else class="icon-placeholder">{{ link.username.charAt(0) }}</div>
        </div>
        <div class="link-info">
          <h3 class="link-name">{{ link.username }}</h3>
          <p class="link-signature">{{ link.signature || '暂无签名' }}</p>
          <a :href="link.link_url" target="_blank" class="link-url">{{ link.link_url }}</a>
        </div>
        <div class="link-actions">
          <span class="status-tag" :class="link.is_show ? 'show' : 'hidden'">
            {{ link.is_show ? '展示中' : '已隐藏' }}
          </span>
          <span class="weight-tag" :class="'weight-' + link.weight">
            {{ getWeightText(link.weight) }}
          </span>
          <button
            class="action-btn"
            :class="link.is_show ? 'hide' : 'show'"
            @click="handleToggleShow(link.id, link.is_show)"
          >
            {{ link.is_show ? '隐藏' : '展示' }}
          </button>
          <button class="action-btn edit" @click="openModal(link)">编辑</button>
          <button class="action-btn delete" @click="handleDelete(link.id)">删除</button>
        </div>
      </div>

      <div v-if="!links.length" class="empty-tip">暂无友链</div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <button
        class="page-btn"
        :disabled="page <= 1"
        @click="page--; loadLinks()"
      >上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button
        class="page-btn"
        :disabled="page >= totalPages"
        @click="page++; loadLinks()"
      >下一页</button>
    </div>

    <!-- 编辑弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? '编辑友链' : '新增友链' }}</h2>
          <button class="close-btn" @click="showModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>名称</label>
            <input v-model="form.username" type="text" class="form-input" placeholder="请输入友链名称" />
          </div>

          <div class="form-group">
            <label>签名</label>
            <input v-model="form.signature" type="text" class="form-input" placeholder="请输入个性签名" />
          </div>

          <div class="form-group">
            <label>图标URL</label>
            <input v-model="form.icon_url" type="text" class="form-input" placeholder="请输入图标地址" />
          </div>

          <div class="form-group">
            <label>链接地址</label>
            <input v-model="form.link_url" type="text" class="form-input" placeholder="请输入跳转链接" />
          </div>

          <div class="form-group">
            <label>权重</label>
            <select v-model="form.weight" class="form-input">
              <option :value="0">挚友</option>
              <option :value="1">朋友</option>
              <option :value="2">来客</option>
            </select>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { friendLinkApi } from '@/api'

const links = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)

const filter = reactive({
  isShow: '',
  weight: ''
})

const showModal = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const form = reactive({
  username: '',
  signature: '',
  icon_url: '',
  link_url: '',
  weight: 2
})

const getWeightText = (weight) => {
  const weightMap = {
    0: '挚友',
    1: '朋友',
    2: '来客'
  }
  return weightMap[weight] || '来客'
}

const totalPages = computed(() => Math.ceil(total.value / size.value))

const loadLinks = async () => {
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (filter.isShow !== '') {
      params.is_show = filter.isShow
    }
    if (filter.weight !== '') {
      params.weight = filter.weight
    }

    const res = await friendLinkApi.all(params)
    links.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error('加载友链失败:', error)
  }
}

const openModal = (link = null) => {
  if (link) {
    editingId.value = link.id
    form.username = link.username
    form.signature = link.signature || ''
    form.icon_url = link.icon_url || ''
    form.link_url = link.link_url
    form.weight = link.weight !== undefined ? link.weight : 2
  } else {
    editingId.value = null
    form.username = ''
    form.signature = ''
    form.icon_url = ''
    form.link_url = ''
    form.weight = 2
  }
  showModal.value = true
}

const handleSubmit = async () => {
  if (!form.username || !form.link_url) return

  submitting.value = true
  try {
    const data = {
      username: form.username,
      signature: form.signature,
      icon_url: form.icon_url,
      link_url: form.link_url,
      weight: form.weight
    }

    if (editingId.value) {
      await friendLinkApi.update(editingId.value, data)
    } else {
      await friendLinkApi.create(data)
    }

    showModal.value = false
    loadLinks()
  } catch (error) {
    console.error('保存友链失败:', error)
    alert('保存失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

const handleToggleShow = async (id, isShow) => {
  try {
    await friendLinkApi.update(id, { is_show: isShow ? 0 : 1 })
    loadLinks()
  } catch (error) {
    console.error('更新友链失败:', error)
    alert('操作失败: ' + error.message)
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个友链吗？')) return

  try {
    await friendLinkApi.delete(id)
    loadLinks()
  } catch (error) {
    console.error('删除友链失败:', error)
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadLinks()
})
</script>

<style lang="scss" scoped>
.friend-links-page {
  max-width: 1200px;
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
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
}

.filter-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
  }

  &.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: #fff;
  }
}

.filter-divider {
  display: flex;
  align-items: center;
  color: var(--color-text-tertiary);
  padding: 0 var(--spacing-xs);
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--spacing-lg);
}

.link-card {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);

  &:hover {
    box-shadow: var(--shadow-md);
  }
}

.link-icon {
  width: 56px;
  height: 56px;
  margin-bottom: var(--spacing-md);

  img {
    width: 100%;
    height: 100%;
    border-radius: var(--radius-md);
    object-fit: cover;
  }
}

.icon-placeholder {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: #fff;
  background: var(--color-accent);
  border-radius: var(--radius-md);
}

.link-info {
  flex: 1;
  margin-bottom: var(--spacing-md);
}

.link-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.link-signature {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.link-url {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;

  &:hover {
    text-decoration: underline;
  }
}

.link-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-divider);
}

.status-tag {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border-radius: var(--radius-sm);

  &.show {
    color: #34c759;
    background: rgba(52, 199, 89, 0.1);
  }

  &.hidden {
    color: var(--color-text-tertiary);
    background: var(--color-bg-tertiary);
  }
}

.weight-tag {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border-radius: var(--radius-sm);

  &.weight-0 {
    color: #ff9500;
    background: rgba(255, 149, 0, 0.1);
  }

  &.weight-1 {
    color: #007aff;
    background: rgba(0, 122, 255, 0.1);
  }

  &.weight-2 {
    color: #8e8e93;
    background: rgba(142, 142, 147, 0.1);
  }
}

.action-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);

  &.show {
    color: #34c759;
    background: rgba(52, 199, 89, 0.1);

    &:hover {
      background: #34c759;
      color: #fff;
    }
  }

  &.hide {
    color: var(--color-text-secondary);
    background: var(--color-bg-tertiary);

    &:hover {
      background: var(--color-bg-primary);
    }
  }

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
  grid-column: 1 / -1;
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
  max-width: 480px;
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

  label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-sm);
  }
}

.form-input {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
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
