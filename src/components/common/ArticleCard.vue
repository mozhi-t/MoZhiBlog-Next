<template>
  <article
    class="article-card"
    :class="{ visible: isVisible }"
    @click="goToArticle"
  >
    <div class="card-image" v-if="article.cover">
      <img :src="article.cover" :alt="article.title" loading="lazy" />
    </div>
    <div class="card-content">
      <div class="card-meta">
        <span class="category" v-if="article.category">{{ article.category }}</span>
        <span class="date">{{ formatDate(article.date) }}</span>
      </div>
      <h3 class="card-title">{{ article.title }}</h3>
      <p class="card-excerpt">{{ article.excerpt }}</p>
      <div class="card-footer">
        <span class="read-more">阅读全文 →</span>
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

const formatDate = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
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
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);

    .card-title {
      color: var(--color-accent);
    }

    .read-more {
      color: var(--color-accent);
      padding-left: var(--spacing-xs);
    }
  }

  &:active {
    transform: translateY(-5px) scale(0.99);
  }
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--color-bg-tertiary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform var(--transition-slow);
  }

  .article-card:hover & img {
    transform: scale(1.05);
  }
}

.card-content {
  padding: var(--spacing-lg);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);

  .category {
    padding: 2px 8px;
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: var(--radius-sm);
    font-weight: 500;
  }
}

.card-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  line-height: var(--line-height-tight);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  transition: color var(--transition-base);
}

.card-excerpt {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: var(--line-height-base);
  margin-bottom: var(--spacing-md);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  .read-more {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-tertiary);
    transition: all var(--transition-base);
  }
}

@media (max-width: 768px) {
  .card-image {
    height: 160px;
  }

  .card-content {
    padding: var(--spacing-md);
  }

  .card-title {
    font-size: var(--font-size-lg);
  }
}
</style>
