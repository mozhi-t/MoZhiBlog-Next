<template>
  <div class="archive-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">归档</h1>
      <p class="page-description">时光流转，文字永存</p>
    </header>

    <!-- Timeline -->
    <div class="timeline">
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
            <path d="M6 9l6 6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Mock archive data
const archiveData = {
  '2024': [
    { id: 1, title: '探索 Vue 3 Composition API 的最佳实践', date: '01-15' },
    { id: 2, title: '设计系统的美学：从苹果设计哲学学到的', date: '01-10' },
    { id: 3, title: '在忙碌的生活中寻找平衡', date: '01-05' }
  ],
  '2023': [
    { id: 4, title: 'TypeScript 类型系统详解', date: '12-28' },
    { id: 5, title: '极简主义：少即是多', date: '12-20' },
    { id: 6, title: 'CSS Grid 布局完全指南', date: '12-15' },
    { id: 7, title: 'JavaScript 异步编程完全指南', date: '11-28' },
    { id: 8, title: 'React Hooks 最佳实践', date: '11-10' }
  ],
  '2022': [
    { id: 9, title: 'Node.js 性能优化实战', date: '12-25' },
    { id: 10, title: '微服务架构设计模式', date: '11-15' },
    { id: 11, title: 'Docker 容器化部署指南', date: '10-20' }
  ]
}

// Expanded years state
const expandedYears = ref(['2024'])

// Toggle year expansion
const toggleYear = (year) => {
  const index = expandedYears.value.indexOf(year)
  if (index > -1) {
    expandedYears.value.splice(index, 1)
  } else {
    expandedYears.value.push(year)
  }
}
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

.page-description {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
}

/* Timeline */
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

/* Year Articles */
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

/* Expand Animation */
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
</style>
