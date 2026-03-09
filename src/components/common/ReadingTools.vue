<template>
  <div class="reading-tools">
    <!-- Font Size Adjuster -->
    <div class="tool-item font-size-tool">
      <button
        class="tool-btn"
        @click="cycleFontSize"
        :title="`字号: ${fontSizeLabel}`"
      >
        <span class="font-size-indicator">A</span>
      </button>
      <span class="font-size-label">{{ fontSizeLabel }}</span>
    </div>

    <!-- Back to Top -->
    <Transition name="fade-scale">
      <button
        v-if="isScrolled"
        class="tool-btn back-to-top"
        @click="scrollToTop"
        title="返回顶部"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M12 19V5M5 12l7-7 7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useReadingStore } from '../../stores/reading'
import { useScrollObserver } from '../../composables/useObserver'

const readingStore = useReadingStore()
const { isScrolled } = useScrollObserver(300)

const fontSize = computed(() => readingStore.fontSize)
const fontSizeLabel = computed(() => {
  const labels = { small: '小', medium: '中', large: '大' }
  return labels[fontSize.value] || '中'
})

const cycleFontSize = () => readingStore.cycleFontSize()

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style lang="scss" scoped>
/* ============================================
   Reading Tools - 阅读辅助工具
   ============================================ */
.reading-tools {
  position: fixed;
  right: var(--spacing-xl);
  bottom: var(--spacing-2xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  z-index: 100;
}

.tool-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.tool-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 20px;
    height: 20px;
    color: var(--color-text-secondary);
    transition: color var(--transition-base);
  }

  &:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-lg);

    svg {
      color: var(--color-accent);
    }
  }

  &:active {
    transform: scale(0.98);
  }
}

.font-size-tool {
  .tool-btn {
    font-weight: 600;
  }

  .font-size-indicator {
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
  }

  .font-size-label {
    font-size: var(--font-size-xs);
    color: var(--color-text-tertiary);
  }

  &:hover {
    .font-size-indicator,
    .font-size-label {
      color: var(--color-accent);
    }
  }
}

.back-to-top {
  svg {
    width: 18px;
    height: 18px;
  }
}

/* Fade Scale Animation */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all var(--transition-smooth);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(10px);
}

@media (max-width: 768px) {
  .reading-tools {
    right: var(--spacing-md);
    bottom: var(--spacing-lg);
  }

  .tool-btn {
    width: 40px;
    height: 40px;
  }
}
</style>
