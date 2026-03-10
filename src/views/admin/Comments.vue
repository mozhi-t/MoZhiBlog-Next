<template>
  <div class="comments-page">
    <div class="page-header">
      <h1 class="page-title">评论管理</h1>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <button
        class="filter-btn"
        :class="{ active: filter.isApproved === '' }"
        @click="filter.isApproved = ''; loadComments()"
      >全部</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isApproved === 1 }"
        @click="filter.isApproved = 1; loadComments()"
      >已通过</button>
      <button
        class="filter-btn"
        :class="{ active: filter.isApproved === 0 }"
        @click="filter.isApproved = 0; loadComments()"
      >未通过</button>
    </div>

    <!-- 评论列表 -->
    <div class="comments-list">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-card"
      >
        <div class="comment-header">
          <div class="comment-author">
            <span class="author-name">{{ comment.nickname }}</span>
            <span class="comment-email" v-if="comment.email">{{ comment.email }}</span>
          </div>
          <span class="comment-time">{{ formatDate(comment.create_time) }}</span>
        </div>

        <div class="comment-article">
          来自文章: {{ comment.article?.title || '未知' }}
        </div>

        <div class="comment-content" :class="{ expanded: expandedId === comment.id }">
          {{ comment.content }}
        </div>
        <button
          v-if="comment.content.length > 100"
          class="expand-btn"
          @click="expandedId = expandedId === comment.id ? null : comment.id"
        >
          {{ expandedId === comment.id ? '收起' : '展开' }}
        </button>

        <div class="comment-actions">
          <span class="status-tag" :class="comment.is_approved ? 'approved' : 'pending'">
            {{ comment.is_approved ? '已通过' : '未通过' }}
          </span>
          <button
            class="action-btn"
            :class="comment.is_approved ? 'reject' : 'approve'"
            @click="handleApprove(comment.id, comment.is_approved ? 0 : 1)"
          >
            {{ comment.is_approved ? '拒绝' : '通过' }}
          </button>
          <button class="action-btn delete" @click="handleDelete(comment.id)">删除</button>
        </div>
      </div>

      <div v-if="!comments.length" class="empty-tip">暂无评论</div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <button
        class="page-btn"
        :disabled="page <= 1"
        @click="page--; loadComments()"
      >上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button
        class="page-btn"
        :disabled="page >= totalPages"
        @click="page++; loadComments()"
      >下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { commentApi } from '@/api'

const comments = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)
const expandedId = ref(null)

const filter = reactive({
  isApproved: ''
})

const totalPages = computed(() => Math.ceil(total.value / size.value))

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const loadComments = async () => {
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (filter.isApproved !== '') {
      params.is_approved = filter.isApproved
    }

    const res = await commentApi.all(params)
    comments.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

const handleApprove = async (id, isApproved) => {
  try {
    await commentApi.approve(id, isApproved)
    loadComments()
  } catch (error) {
    console.error('审核评论失败:', error)
    alert('操作失败: ' + error.message)
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这条评论吗？')) return

  try {
    await commentApi.delete(id)
    loadComments()
  } catch (error) {
    console.error('删除评论失败:', error)
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadComments()
})
</script>

<style lang="scss" scoped>
.comments-page {
  max-width: 1000px;
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

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.comment-card {
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.comment-author {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.author-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.comment-email {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.comment-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.comment-article {
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  margin-bottom: var(--spacing-md);
}

.comment-content {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: var(--spacing-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;

  &.expanded {
    display: block;
    -webkit-line-clamp: unset;
  }
}

.expand-btn {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;

  &:hover {
    text-decoration: underline;
  }
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.status-tag {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border-radius: var(--radius-sm);

  &.approved {
    color: #34c759;
    background: rgba(52, 199, 89, 0.1);
  }

  &.pending {
    color: #ff9500;
    background: rgba(255, 149, 0, 0.1);
  }
}

.action-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--font-size-xs);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);

  &.approve {
    color: #34c759;
    background: rgba(52, 199, 89, 0.1);

    &:hover {
      background: #34c759;
      color: #fff;
    }
  }

  &.reject {
    color: #ff9500;
    background: rgba(255, 149, 0, 0.1);

    &:hover {
      background: #ff9500;
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
