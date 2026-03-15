<template>
  <div class="message-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">留言板</h1>
      <p class="page-desc">纸短情长，见字如晤</p>
    </header>

    <!-- Twikoo Comments Section -->
    <section class="comments-section">
      <div id="twikoo-container">
        <div id="tcomment"></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, nextTick } from 'vue'
import { TWIKOO_ENV_ID, TWIKOO_CONFIG } from '../config/twikoo'
import { updateSeo } from '../utils/seo'

// 初始化 Twikoo 评论（作为留言板）
const initTwikoo = () => {
  nextTick(() => {
    // 如果 Twikoo 已经加载，直接初始化
    if (window.twikoo) {
      initTwikooInstance()
      return
    }

    // 动态加载 Twikoo 脚本
    const script = document.createElement('script')
    script.src = '/twikoo.min.js'
    script.onload = () => {
      initTwikooInstance()
    }
    script.onerror = () => {
      console.error('Twikoo 脚本加载失败')
    }
    document.head.appendChild(script)
  })
}

// 初始化 Twikoo 实例
const initTwikooInstance = () => {
  if (!window.twikoo) {
    console.error('Twikoo 未正确加载')
    return
  }

  window.twikoo.init({
    envId: TWIKOO_ENV_ID,
    el: TWIKOO_CONFIG.el,
    path: '/message',
    lang: TWIKOO_CONFIG.lang
  })
}

onMounted(() => {
  updateSeo({
    title: '留言板',
    description: '在留言板页面留下你的想法、建议与交流内容，和 MoZhi Blog 产生互动。',
    path: '/message',
    keywords: ['留言板', '评论', '互动']
  })
  initTwikoo()
})
</script>

<style lang="scss" scoped>
/* ============================================
   Message Page - 留言板页
   ============================================ */
.message-page {
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

.page-desc {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

/* Comments Section */
.comments-section {
  max-width: 800px;
  margin: 0 auto;
}

#twikoo-container {
  min-height: 200px;
}
</style>
