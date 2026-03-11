<template>
  <div class="message-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">留言板</h1>
      <p class="page-desc">想对我说些什么？</p>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <!-- Message Form -->
    <div class="message-form-section">
      <h2 class="section-title">发表留言</h2>
      <form class="message-form" @submit.prevent="handleSubmit">
        <div class="form-row">
          <input
            v-model="form.nickname"
            type="text"
            class="form-input"
            placeholder="昵称"
            required
          />
          <input
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="邮箱（选填）"
          />
        </div>
        <textarea
          v-model="form.content"
          class="form-textarea"
          placeholder="写下你想说的话..."
          rows="4"
          required
        ></textarea>
        <button type="submit" class="submit-btn" :disabled="submitting">
          {{ submitting ? '提交中...' : '提交留言' }}
        </button>
      </form>
    </div>

    <!-- Messages List -->
    <div class="messages-section">
      <h2 class="section-title">全部留言</h2>
      <div class="messages-list">
        <div
          v-for="(message, index) in messages"
          :key="message.id"
          class="message-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="message-avatar">
            <img :src="`https://api.dicebear.com/7.x/identicon/svg?seed=${message.nickname}`" :alt="message.nickname" />
          </div>
          <div class="message-content">
            <div class="message-header">
              <span class="message-nickname">{{ message.nickname }}</span>
              <span class="message-time">{{ formatTime(message.create_time) }}</span>
            </div>
            <p class="message-text">{{ message.content }}</p>
          </div>
        </div>

        <div v-if="messages.length === 0 && !loading" class="empty-tip">
          暂无留言，快来抢沙发吧！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { messageBoardApi } from '../api/frontend'

// 加载状态
const loading = ref(true)
const submitting = ref(false)

// 留言数据
const messages = ref([])

// 表单数据
const form = reactive({
  nickname: '',
  email: '',
  content: ''
})

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return minutes <= 1 ? '刚刚' : `${minutes}分钟前`
    }
    return `${hours}小时前`
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days}天前`
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}

// 加载留言
const loadMessages = async () => {
  try {
    loading.value = true
    const res = await messageBoardApi.list()
    messages.value = res.data
  } catch (error) {
    console.error('加载留言失败:', error)
  } finally {
    loading.value = false
  }
}

// 提交留言
const handleSubmit = async () => {
  if (!form.nickname || !form.content) return

  submitting.value = true
  try {
    await messageBoardApi.create({
      nickname: form.nickname,
      email: form.email,
      content: form.content
    })

    // 清空表单
    form.nickname = ''
    form.email = ''
    form.content = ''

    // 重新加载留言
    await loadMessages()
  } catch (error) {
    console.error('提交留言失败:', error)
    alert('提交失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadMessages()
})
</script>

<style lang="scss" scoped>
/* ============================================
   Message Page - 留言板页
   ============================================ */
.message-page {
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

.page-desc {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

/* Message Form Section */
.message-form-section {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-3xl);
  box-shadow: var(--shadow-sm);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.message-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.form-input,
.form-textarea {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 2px solid transparent;
  border-radius: var(--radius-lg);
  outline: none;
  transition: all var(--transition-base);
  font-family: inherit;

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
    background: var(--color-bg-secondary);
  }
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  align-self: flex-end;
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

/* Messages Section */
.messages-section {
  margin-bottom: var(--spacing-3xl);
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.message-card {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  animation: cardFadeIn 0.4s ease forwards;
  opacity: 0;

  &:hover {
    box-shadow: var(--shadow-md);
  }
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
  }
}

.message-avatar {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-full);
  overflow: hidden;
  background: var(--color-bg-tertiary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xs);
}

.message-nickname {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.message-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.message-text {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Loading & Empty States */
.loading-state {
  display: flex;
  justify-content: center;
  padding: var(--spacing-3xl);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-tip {
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-3xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
}
</style>
