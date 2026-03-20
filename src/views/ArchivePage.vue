<template>
  <div class="archive-page">
    <header class="page-header">
      <h1 class="page-title">归档</h1>
      <p class="page-description">时光流转，文字长存</p>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <div v-else class="timeline">
      <div
        v-for="(yearGroup, year) in archiveData"
        :key="year"
        class="timeline-year"
      >
        <button
          class="year-header"
          :class="{ expanded: expandedYears.includes(year) }"
          @click="toggleYear(year)"
        >
          <span class="year-label">{{ year }}</span>
          <span class="year-count">{{ yearGroup.length }} 篇</span>
          <svg class="expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M6 9l6 6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>

        <Transition name="expand">
          <ul v-if="expandedYears.includes(year)" class="year-articles">
            <li
              v-for="(article, index) in yearGroup"
              :key="article.id"
              class="timeline-item"
              :style="{ transitionDelay: `${index * 0.05}s` }"
            >
              <span class="article-date">{{ article.date }}</span>
              <router-link :to="`/article/${article.id}`" class="article-link">
                {{ article.title }}
              </router-link>
            </li>
          </ul>
        </Transition>
      </div>

      <div v-if="Object.keys(archiveData).length === 0" class="empty-tip">
        暂无文章
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { articlesApi } from '../api/frontend'
import { updateSeo } from '../utils/seo'

const loading = ref(true)
const articles = ref([])

const loadArticles = async () => {
  try {
    loading.value = true
    const res = await articlesApi.list({ page: 1, size: 100 })
    articles.value = (res.data.items || []).map(item => ({
      id: item.id,
      title: item.title,
      date: new Date(item.create_time)
    }))
  } catch (error) {
    console.error('加载归档失败:', error)
  } finally {
    loading.value = false
  }
}

const archiveData = computed(() => {
  const groups = {}

  articles.value.forEach(article => {
    const year = article.date.getFullYear().toString()
    const monthDay = `${String(article.date.getMonth() + 1).padStart(2, '0')}-${String(article.date.getDate()).padStart(2, '0')}`

    if (!groups[year]) {
      groups[year] = []
    }

    groups[year].push({
      id: article.id,
      title: article.title,
      date: monthDay
    })
  })

  const sortedGroups = {}
  Object.keys(groups).sort((a, b) => b - a).forEach((key) => {
    sortedGroups[key] = groups[key]
  })

  return sortedGroups
})

const totalArticles = computed(() => articles.value.length)
const yearCount = computed(() => Object.keys(archiveData.value).length)
const expandedYears = ref(['2024'])

const toggleYear = (year) => {
  const index = expandedYears.value.indexOf(year)
  if (index > -1) {
    expandedYears.value.splice(index, 1)
  } else {
    expandedYears.value.push(year)
  }
}

onMounted(() => {
  loadArticles().then(() => {
    expandedYears.value = Object.keys(archiveData.value)
    updateSeo({
      title: '归档',
      description: `按时间轴浏览博客归档内容，当前收录 ${totalArticles.value} 篇文章，跨越 ${yearCount.value} 个年份。`,
      path: '/archive',
      keywords: ['归档', '文章归档', '时间轴']
    })
  })
})
</script>

<style lang="scss" scoped>
/* ============================================
   Archive Page - 归档页
   ============================================ */
.archive-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

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

.page-description {
  font-size: var(--font-size-lg);
  color: var(--color-text-tertiary);
}

.timeline {
  position: relative;
  padding-left: var(--spacing-xl);

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--color-divider);
  }
}

.timeline-year {
  margin-bottom: var(--spacing-xl);
}

.year-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  width: 100%;
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-bg-tertiary);
    transform: scale(1.01);

    .year-label {
      color: var(--color-accent);
    }
  }

  &.expanded {
    .expand-icon {
      transform: rotate(180deg);
    }
  }
}

.year-label {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  transition: color var(--transition-base);
}

.year-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  flex: 1;
}

.expand-icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-tertiary);
  transition: transform var(--transition-base);
}

.year-articles {
  list-style: none;
  margin-top: var(--spacing-md);
  padding-left: var(--spacing-md);
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) 0;
  opacity: 0;
  animation: fadeIn 0.3s ease forwards;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: calc(-1 * var(--spacing-xl) - 5px);
    width: 10px;
    height: 10px;
    background: var(--color-bg-secondary);
    border: 2px solid var(--color-accent);
    border-radius: 50%;
    transition: all var(--transition-base);
  }

  &:hover::before {
    background: var(--color-accent);
    transform: scale(1.2);
  }

  &:hover {
    .article-link {
      color: var(--color-accent);
    }
  }
}

.article-date {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  min-width: 40px;
  font-family: monospace;
}

.article-link {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color var(--transition-base);
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.expand-enter-active,
.expand-leave-active {
  transition: all var(--transition-smooth);
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  max-height: 500px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: var(--font-size-3xl);
  }

  .timeline {
    padding-left: var(--spacing-md);
  }
}

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
}
</style>
