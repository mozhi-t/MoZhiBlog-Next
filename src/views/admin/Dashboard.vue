<template>
  <div class="dashboard">
    <h1 class="page-title">仪表盘</h1>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon articles">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalArticles }}</span>
          <span class="stat-label">文章总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon links">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalFriendLinks }}</span>
          <span class="stat-label">友链总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon tags">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
            <line x1="7" y1="7" x2="7.01" y2="7"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalTags }}</span>
          <span class="stat-label">标签总数</span>
        </div>
      </div>
    </div>

    <div class="recent-grid">
      <div class="recent-card">
        <h3 class="card-title">最近文章</h3>
        <div class="recent-list">
          <div
            v-for="article in recentArticles"
            :key="article.id"
            class="recent-item"
          >
            <span class="item-title">{{ article.title }}</span>
            <span class="item-meta">{{ article.read_count }} 阅读</span>
          </div>
          <div v-if="!recentArticles.length" class="empty-tip">暂无文章</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { articleApi, friendLinkApi, tagApi } from '@/api'

const stats = ref({
  totalArticles: 0,
  totalFriendLinks: 0,
  totalTags: 0
})

const recentArticles = ref([])

const loadData = async () => {
  try {
    const [articlesRes, tagsRes, linksRes] = await Promise.all([
      articleApi.list({ page: 1, size: 5 }),
      tagApi.all({ page: 1, size: 1 }),
      friendLinkApi.all({ page: 1, size: 1 })
    ])

    stats.value.totalArticles = articlesRes.data.total || 0
    recentArticles.value = articlesRes.data.items || []
    stats.value.totalTags = tagsRes.data.total || 0
    stats.value.totalFriendLinks = linksRes.data.total || 0
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);

  svg {
    width: 28px;
    height: 28px;
  }

  &.articles {
    background: rgba(0, 102, 204, 0.1);
    color: var(--color-accent);
  }

  &.comments {
    background: rgba(52, 199, 89, 0.1);
    color: #34c759;
  }

  &.links {
    background: rgba(255, 149, 0, 0.1);
    color: #ff9500;
  }

  &.tags {
    background: rgba(175, 82, 222, 0.1);
    color: #af52de;
  }
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.recent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
}

.recent-card {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-divider);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border-radius: var(--radius-md);
  transition: background var(--transition-base);

  &:hover {
    background: var(--color-bg-tertiary);
  }
}

.item-title {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.item-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.item-content {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.empty-tip {
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-xl);
}
</style>
