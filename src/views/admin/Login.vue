<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">MoZhi Blog</h1>
        <p class="login-subtitle">后台管理系统</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <input
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="请输入密码"
            required
          />
        </div>

        <div v-if="errorMsg" class="error-tip">{{ errorMsg }}</div>

        <button
          type="submit"
          class="login-btn"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/admin'

const router = useRouter()
const adminStore = useAdminStore()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  errorMsg.value = ''
  loading.value = true

  try {
    await adminStore.login(form.username, form.password)
    router.push('/admin/dashboard')
  } catch (error) {
    errorMsg.value = error.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
  padding: var(--spacing-lg);
}

.login-card {
  width: 100%;
  max-width: 380px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(10px);
  animation: cardFadeIn 0.4s ease-out;
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.login-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.login-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  margin-bottom: var(--spacing-sm);
}

.form-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 2px solid transparent;
  border-radius: var(--radius-lg);
  outline: none;
  transition: all var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
    background: var(--color-bg-secondary);
  }
}

.error-tip {
  color: #ff3b30;
  font-size: var(--font-size-sm);
  text-align: center;
  padding: var(--spacing-sm);
}

.login-btn {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-base);
  font-weight: 600;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-top: var(--spacing-sm);

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}
</style>
