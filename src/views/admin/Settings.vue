<template>
  <div class="settings-page">
    <div class="page-header">
      <h1 class="page-title">设置</h1>
    </div>

    <!-- 当前账户信息 -->
    <div class="info-card">
      <h2 class="card-title">当前账户</h2>
      <div class="info-item">
        <span class="info-label">用户名</span>
        <span class="info-value">{{ adminInfo.username }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">邮箱</span>
        <span class="info-value">{{ adminInfo.email || '未设置' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">创建时间</span>
        <span class="info-value">{{ formatDate(adminInfo.create_time) }}</span>
      </div>
    </div>

    <!-- 修改账户信息 -->
    <div class="settings-card">
      <h2 class="card-title">修改账户信息</h2>
      <p class="card-tip">修改用户名或密码后，需要重新登录</p>

      <div class="form">
        <div class="form-group">
          <label class="form-label">当前密码 <span class="required">*</span></label>
          <input
            v-model="form.current_password"
            type="password"
            class="form-input"
            placeholder="请输入当前密码"
          />
        </div>

        <div class="form-group">
          <label class="form-label">新用户名</label>
          <input
            v-model="form.new_username"
            type="text"
            class="form-input"
            placeholder="不修改则留空"
          />
        </div>

        <div class="form-group">
          <label class="form-label">新密码</label>
          <input
            v-model="form.new_password"
            type="password"
            class="form-input"
            placeholder="不修改则留空"
          />
        </div>

        <div class="form-group">
          <label class="form-label">确认新密码</label>
          <input
            v-model="form.confirm_password"
            type="password"
            class="form-input"
            placeholder="请再次输入新密码"
          />
        </div>

        <div class="form-actions">
          <button class="submit-btn" @click="handleSubmit" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存修改' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 成功提示 -->
    <div class="modal-overlay" v-if="showSuccessModal" @click.self="showSuccessModal = false">
      <div class="modal success-modal">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        </div>
        <h2>设置已更新</h2>
        <p>用户名或密码已修改，请重新登录</p>
        <button class="confirm-btn" @click="handleReLogin">重新登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/api'
import { useAdminStore } from '@/stores/admin'

const router = useRouter()
const adminStore = useAdminStore()

const adminInfo = ref({
  username: '',
  email: '',
  create_time: ''
})

const form = reactive({
  current_password: '',
  new_username: '',
  new_password: '',
  confirm_password: ''
})

const submitting = ref(false)
const showSuccessModal = ref(false)

// 加载管理员信息
const loadAdminInfo = async () => {
  try {
    const res = await adminApi.getInfo()
    adminInfo.value = res.data
  } catch (error) {
    console.error('加载管理员信息失败', error)
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 提交表单
const handleSubmit = async () => {
  // 验证当前密码
  if (!form.current_password) {
    alert('请输入当前密码')
    return
  }

  // 如果填写了新用户名或新密码
  if (!form.new_username && !form.new_password) {
    alert('请填写新用户名或新密码')
    return
  }

  // 验证确认密码
  if (form.new_password !== form.confirm_password) {
    alert('两次输入的密码不一致')
    return
  }

  // 验证密码长度
  if (form.new_password && form.new_password.length < 6) {
    alert('新密码长度不能少于6位')
    return
  }

  submitting.value = true

  try {
    const data = {
      current_password: form.current_password,
      new_username: form.new_username || null,
      new_password: form.new_password || null
    }

    const res = await adminApi.updateSettings(data)

    if (res.data && res.data.token) {
      // 保存新token
      localStorage.setItem('admin_token', res.data.token)
      adminStore.token = res.data.token

      // 显示成功提示
      showSuccessModal.value = true
    }
  } catch (error) {
    const message = error.response?.data?.detail || '修改失败，请重试'
    alert(message)
  } finally {
    submitting.value = false
  }
}

// 重新登录
const handleReLogin = () => {
  adminStore.logout()
  router.push('/admin/login')
}

onMounted(() => {
  loadAdminInfo()
})
</script>

<style lang="scss" scoped>
.settings-page {
  max-width: 600px;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
}

.info-card,
.settings-card {
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.card-tip {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-bottom: var(--spacing-lg);
  margin-top: calc(var(--spacing-lg) * -1);
}

.info-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none;
  }
}

.info-label {
  width: 100px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.info-value {
  flex: 1;
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.required {
  color: var(--color-accent);
}

.form-input {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);

  &:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 2px var(--color-accent-light);
  }

  &::placeholder {
    color: var(--color-text-quaternary);
  }
}

.form-actions {
  margin-top: var(--spacing-xl);
}

.submit-btn {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    opacity: 0.9;
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

// 成功弹窗
.success-modal {
  text-align: center;
  padding: var(--spacing-xl);

  h2 {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-sm);
  }

  p {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-xl);
  }
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--spacing-lg);
  color: var(--color-success);

  svg {
    width: 100%;
    height: 100%;
  }
}

.confirm-btn {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    opacity: 0.9;
  }
}

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
}

.modal {
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  min-width: 320px;
  max-width: 90%;
}
</style>
