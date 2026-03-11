<template>
  <div class="messages-page">
    <div class="page-header">
      <h1 class="page-title">留言管理</h1>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === '' }"
        @click="filter.isShow = ''; loadMessages()"
      >全部</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === 1 }"
        @click="filter.isShow = 1; loadMessages()"
      >展示中</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isShow === 0 }"
        @click="filter.isShow = 0; loadMessages()"
      >已隐藏</button>
    </div>

    <!-- 留言列表 -->
    <div class="messages-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>昵称</th>
            <th>邮箱</th>
            <th>内容</th>
            <th>时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="message in messages" :key="message.id">
            <td>{{ message.id }}</td>
            <td>{{ message.nickname }}</td>
            <td>{{ message.email || '-' }}</td>
            <td class="content-cell">
              <span class="content-text">{{ message.content }}</span>
            </td>
            <td>{{ formatTime(message.create_time) }}</td>
            <td>
              <span class="status-tag" :class="message.is_show ? 'show' : 'hidden'">
                {{ message.is_show ? '展示中' : '已隐藏' }}
              </span>
            </td>
            <td>
              <button
                class="action-btn"
                :class="message.is_show ? 'hide' : 'show'"
                @click="handleToggleShow(message.id, message.is_show)"
              >
                {{ message.is_show ? '隐藏' : '展示' }}
              </button>
              <button class="action-btn delete" @click="handleDelete(message.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!messages.length" class="empty-tip">暂无留言</div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <button
        class="page-btn"
        :disabled="page <= 1"
        @click="page--; loadMessages()"
      >上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button
        class="page-btn"
        :disabled="page >= totalPages"
        @click="page++; loadMessages()"
      >下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { messageApi } from '@/api'

const messages = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)

const filter = reactive({
  isShow: ''
})

const totalPages = computed(() => Math.ceil(total.value / size.value))

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const loadMessages = async () => {
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (filter.isShow !== '') {
      params.is_show = filter.isShow
    }

    const res = await messageApi.all(params)
    messages.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error('加载留言失败:', error)
  }
}

const handleToggleShow = async (id, isShow) => {
  try {
    await messageApi.update(id, { is_show: isShow ? 0 : 1 })
    loadMessages()
  } catch (error) {
    console.error('更新留言失败:', error)
    alert('操作失败: ' + error.message)
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这条留言吗？')) return

  try {
    await messageApi.delete(id)
    loadMessages()
  } catch (error) {
    console.error('删除留言失败:', error)
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadMessages()
})
</script>

<style lang="scss" scoped>
.messages-page {
  max-width: 1200px;
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

.messages-table {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  overflow: hidden;

  table {
    width: 100%;
    border-collapse: collapse;

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
  }
}

.content-cell {
  max-width: 300px;
}

.content-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-tag {
  display: inline-block;
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

.action-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-right: var(--spacing-xs);

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
