<template>
  <article
    ref="targetRef"
    class="article-card"
    :class="{ visible: isVisible }"
    @click="goToArticle"
  >
    <div class="card-content">
      <!-- 分类小标签 -->
      <div class="card-category">
        <svg class="category-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>{{ article.category }}</span>
      </div>

      <!-- 文章标题 -->
      <h3 class="card-title">{{ article.title }}</h3>

      <!-- 简短摘要 -->
      <p class="card-excerpt">{{ article.excerpt }}</p>

      <!-- 底部：标签云 + 日期 -->
      <div class="card-footer">
        <div class="tags" v-if="article.tags && article.tags.length">
          <span class="tag" v-for="tag in article.tags" :key="tag">#{{ tag }}</span>
        </div>
        <span class="date">{{ article.date }}</span>
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
  }
})

const router = useRouter()
const { targetRef, isVisible } = useIntersectionObserver()

const goToArticle = () => {
  router.push(`/article/${props.article.id}`)
}
</script>

<style lang="scss" scoped>
/* ============================================
   Article Card - 文章卡片
   ============================================ */
.article-card {
  position: relative;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  cursor: pointer;
  opacity: 0;
  transform: translateY(20px);
  transition: all var(--transition-smooth);

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

/* 分类小标签 */
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
}

.category-icon {
  width: 12px;
  height: 12px;
}

/* 文章标题 */
.card-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  line-height: var(--line-height-tight);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  transition: color var(--transition-base);
}

/* 简短摘要 */
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

/* 底部：标签云 + 日期 */
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

  &:hover {
    color: var(--color-accent);
  }
}

.date {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
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
