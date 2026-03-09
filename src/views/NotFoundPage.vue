<template>
  <div class="not-found-page">
    <div class="content">
      <!-- 404 Number with breathing animation -->
      <div class="error-code">
        <span class="digit">4</span>
        <span class="digit">0</span>
        <span class="digit">4</span>
      </div>

      <h1 class="title">页面未找到</h1>
      <p class="description">
        抱歉，您访问的页面不存在或已被移除。
      </p>

      <router-link to="/" class="back-home">
        <span>返回首页</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
/* ============================================
   Not Found Page - 404 页面
   ============================================ */
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-lg);
  text-align: center;
}

.content {
  max-width: 500px;
}

/* 404 Error Code with breathing animation */
.error-code {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.digit {
  font-size: 120px;
  font-weight: 800;
  color: var(--color-text-primary);
  line-height: 1;
  animation: breathe 3s ease-in-out infinite;
  text-shadow: var(--shadow-lg);

  &:nth-child(1) { animation-delay: 0s; }
  &:nth-child(2) { animation-delay: 0.3s; }
  &:nth-child(3) { animation-delay: 0.6s; }
}

@keyframes breathe {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
}

.title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.description {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
}

/* Back Home Button */
.back-home {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-base);

  svg {
    width: 18px;
    height: 18px;
    transition: transform var(--transition-base);
  }

  &:hover {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
    transform: scale(1.02);

    svg {
      transform: translateX(4px);
    }
  }
}

@media (max-width: 768px) {
  .digit {
    font-size: 80px;
  }

  .title {
    font-size: var(--font-size-2xl);
  }
}
</style>
