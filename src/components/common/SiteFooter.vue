<template>
  <footer class="site-footer" :class="{ visible: isVisible }">
    <div class="footer-content">
      <p class="copyright">
        &copy; {{ currentYear }} MoZhi. All rights reserved.
      </p>
      <div class="footer-links">
        <a href="https://github.com" target="_blank" rel="noopener">GitHub</a>
        <span class="divider">·</span>
        <a href="/rss.xml">RSS</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const currentYear = computed(() => new Date().getFullYear())

const checkScrollPosition = () => {
  const scrollHeight = document.documentElement.scrollHeight
  const clientHeight = window.innerHeight
  const scrollTop = window.scrollY

  // 当滚动到页面底部附近时显示
  isVisible.value = scrollTop + clientHeight >= scrollHeight - 100
}

onMounted(() => {
  window.addEventListener('scroll', checkScrollPosition, { passive: true })
  checkScrollPosition()
})

onUnmounted(() => {
  window.removeEventListener('scroll', checkScrollPosition)
})
</script>

<style lang="scss" scoped>
/* ============================================
   Site Footer - 简约页脚
   ============================================ */
.site-footer {
  padding: var(--spacing-3xl) var(--spacing-lg);
  margin-top: var(--spacing-3xl);
  background: var(--color-bg-tertiary);
  opacity: 0;
  transform: translateY(20px);
  transition: all var(--transition-smooth);

  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
}

.footer-content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  text-align: center;
}

.copyright {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-bottom: var(--spacing-sm);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);

  a {
    color: var(--color-text-tertiary);
    text-decoration: none;
    transition: color var(--transition-base);

    &:hover {
      color: var(--color-accent);
    }
  }

  .divider {
    color: var(--color-text-tertiary);
  }
}
</style>
