<template>
  <article
    ref="targetRef"
    class="article-card"
    :class="{ visible: isVisible }"
    @click="goToArticle"
  >
    <div class="card-content">
      <div v-if="article.category" class="card-category" @click.stop="goToCategory">
        <svg class="category-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <span>{{ article.category }}</span>
      </div>

      <div class="card-title-row">
        <h3 class="card-title" v-html="highlightedTitle"></h3>
        <div v-if="article.is_top || article.need_password" class="card-badges">
          <span v-if="article.is_top" class="badge top">置顶</span>
          <span v-if="article.need_password" class="badge password">加密</span>
        </div>
      </div>

      <p class="card-excerpt" v-html="highlightedExcerpt"></p>

      <div class="card-footer">
        <div v-if="article.tag_list && article.tag_list.length > 0" class="tags">
          <span
            v-for="tag in article.tag_list"
            :key="tag.id"
            class="tag"
            @click.stop="goToTag(tag.id)"
          >
            #{{ tag.name }}
          </span>
        </div>
        <div v-else-if="article.tag" class="tags">
          <span class="tag" @click.stop="goToTag(article.tag.id)">#{{ article.tag.name }}</span>
        </div>

        <div class="right-info">
          <div class="dates">
            <span class="date-item">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              {{ formatDate(article.create_time, true) }}
            </span>
            <span v-if="article.update_time && article.update_time !== article.create_time" class="date-item">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              {{ formatDate(article.update_time, true) }}
            </span>
          </div>

          <div class="stats">
            <span class="stat-item">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              {{ article.read_count || 0 }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useIntersectionObserver } from '../../composables/useObserver'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  highlightKeyword: {
    type: String,
    default: ''
  }
})

const router = useRouter()
const { targetRef, isVisible } = useIntersectionObserver()

const escapeHtml = (value = '') => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;')

const escapeRegExp = (value = '') => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

const formatDate = (date, includeTime = false) => {
  if (!date) return ''

  if (includeTime) {
    return new Date(date).toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const highlightText = (value = '') => {
  const keyword = props.highlightKeyword.trim()
  const safeText = escapeHtml(value)

  if (!keyword) {
    return safeText
  }

  return safeText.replace(
    new RegExp(`(${escapeRegExp(keyword)})`, 'gi'),
    '<mark class="keyword-highlight">$1</mark>'
  )
}

const defaultExcerpt = computed(() => (
  props.article.excerpt || (props.article.need_password ? '这是一篇密码保护文章，输入正确密码后可查看完整内容。' : '')
))

const highlightedTitle = computed(() => highlightText(props.article.title || ''))
const highlightedExcerpt = computed(() => highlightText(defaultExcerpt.value))

const goToArticle = () => {
  router.push(`/article/${props.article.id}`)
}

const goToCategory = () => {
  if (props.article.category_id) {
    router.push(`/category?id=${props.article.category_id}`)
  }
}

const goToTag = (tagId) => {
  router.push(`/tag?id=${tagId}`)
}
</script>

<style lang="scss" scoped>
.article-card {
  position: relative;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  cursor: pointer;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.2s ease, transform 0.2s ease, box-shadow var(--transition-base);

  &.visible {
    opacity: 1;
    transform: translateY(0);
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);

    .card-title {
      color: var(--color-accent);
    }
  }

  &:active {
    transform: translateY(-4px) scale(0.99);
  }
}

.card-content {
  padding: var(--spacing-xl);
}

.card-category {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 6px 12px;
  margin-bottom: var(--spacing-md);
  background: var(--color-accent-light);
  color: var(--color-accent);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-accent);
    color: #fff;
  }
}

.category-icon {
  width: 12px;
  height: 12px;
}

.card-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  line-height: var(--line-height-tight);
  color: var(--color-text-primary);
  transition: color var(--transition-base);
}

.card-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.card-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  flex-shrink: 0;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;

  &.top {
    color: #b85c00;
    background: rgba(255, 183, 77, 0.2);
  }

  &.password {
    color: #8a3ffc;
    background: rgba(138, 63, 252, 0.12);
  }
}

.card-excerpt {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: var(--line-height-base);
  margin-bottom: var(--spacing-lg);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.tag {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  transition: color var(--transition-base);
  cursor: pointer;

  &:hover {
    color: var(--color-accent);
  }
}

.right-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.dates {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.date-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);

  .icon {
    width: 12px;
    height: 12px;
    opacity: 0.7;
  }
}

.stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.stat-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);

  .icon {
    width: 12px;
    height: 12px;
    opacity: 0.7;
  }
}

:deep(.keyword-highlight) {
  padding: 0 4px;
  color: inherit;
  background: rgba(255, 196, 0, 0.26);
  border-radius: 4px;
}

.card-excerpt :deep(.keyword-highlight) {
  color: var(--color-text-primary);
}

@media (max-width: 768px) {
  .card-content {
    padding: var(--spacing-md);
  }

  .card-title {
    font-size: var(--font-size-base);
  }
}
</style>
