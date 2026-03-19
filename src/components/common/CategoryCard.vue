<template>
  <router-link
    ref="cardRef"
    :to="`/category/${slug}`"
    class="category-card"
    :class="{ visible: isVisible }"
  >
    <div class="category-icon">
      <slot name="icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </slot>
    </div>
    <div class="category-info">
      <h3 class="category-name">{{ name }}</h3>
      <p class="category-count">{{ count }} 篇文章</p>
    </div>
  </router-link>
</template>

<script setup>
import { ref } from 'vue'
import { useIntersectionObserver } from '../../composables/useObserver'

defineProps({
  name: {
    type: String,
    required: true
  },
  slug: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0
  }
})

const cardRef = ref(null)
const { isVisible } = useIntersectionObserver({ threshold: 0.2 }, cardRef)
</script>

<style lang="scss" scoped>
/* ============================================
   Category Card - 分类卡片
   ============================================ */
.category-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  text-decoration: none;
  opacity: 0;
  transform: translateX(10px);
  transition: all var(--transition-smooth);

  &.visible {
    opacity: 1;
    transform: translateX(0);
  }

  &:hover {
    background: var(--color-bg-tertiary);
    box-shadow: var(--shadow-md);

    .category-icon {
      background: var(--color-accent-light);

      svg {
        color: var(--color-accent);
      }
    }

    .category-name {
      color: var(--color-accent);
    }
  }
}

[data-theme="dark"] .category-card {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

.category-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);

  svg {
    width: 24px;
    height: 24px;
    color: var(--color-text-secondary);
    transition: color var(--transition-base);
  }
}

.category-info {
  flex: 1;
}

.category-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
  transition: color var(--transition-base);
}

.category-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}
</style>
