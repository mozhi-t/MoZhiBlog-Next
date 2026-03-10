<template>
  <div class="links-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">友链</h1>
      <p class="page-desc">交换友链？随时欢迎！</p>
    </header>

    <!-- Links Grid -->
    <div class="links-grid">
      <a
        v-for="(link, index) in links"
        :key="index"
        :href="link.url"
        target="_blank"
        class="link-card"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="link-avatar">
          <img :src="link.avatar" :alt="link.name" />
        </div>
        <div class="link-info">
          <h3 class="link-name">{{ link.name }}</h3>
          <p class="link-desc">{{ link.description }}</p>
        </div>
      </a>
    </div>

    <!-- Contact Section -->
    <div class="contact-section">
      <h2 class="section-title">交换友链</h2>
      <p class="contact-text">如果你想交换友链，欢迎通过以下方式联系我：</p>
      <div class="contact-info">
        <div class="contact-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="22,6 12,13 2,6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>email@example.com</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const links = ref([
  {
    name: 'Vue 官方文档',
    description: '渐进式 JavaScript 框架',
    url: 'https://vuejs.org',
    avatar: 'https://vuejs.org/logo.svg'
  },
  {
    name: 'MDN Web Docs',
    description: 'Mozilla 开发者网络',
    url: 'https://developer.mozilla.org',
    avatar: 'https://developer.mozilla.org/mdn-social-share.0ca8b497.png'
  },
  {
    name: 'GitHub',
    description: '全球最大代码托管平台',
    url: 'https://github.com',
    avatar: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'
  },
  {
    name: 'CSS-Tricks',
    description: 'CSS 技巧与前端资源',
    url: 'https://css-tricks.com',
    avatar: 'https://css-tricks.com/apple-touch-icon.png'
  },
  {
    name: '掘金',
    description: '程序员的技术社区',
    url: 'https://juejin.cn',
    avatar: 'https://p1-juejin.byteimg.com/tos-cn-i-qvj2lxx49k/favicon.ico~tplv-qvj2lxx49k-favicon.ico'
  },
  {
    name: 'Vite',
    description: '下一代前端构建工具',
    url: 'https://vitejs.dev',
    avatar: 'https://vitejs.dev/logo.svg'
  }
])
</script>

<style lang="scss" scoped>
/* ============================================
   Links Page - 友链页
   ============================================ */
.links-page {
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

/* Links Grid */
.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-3xl);
}

.link-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  text-decoration: none;
  transition: all var(--transition-smooth);
  animation: cardFadeIn 0.4s ease forwards;
  opacity: 0;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);

    .link-name {
      color: var(--color-accent);
    }
  }

  &:active {
    transform: translateY(-4px) scale(0.99);
  }
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
  }
}

.link-avatar {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: var(--radius-full);
  overflow: hidden;
  background: var(--color-bg-tertiary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.link-info {
  flex: 1;
  min-width: 0;
}

.link-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
  transition: color var(--transition-base);
}

.link-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Contact Section */
.contact-section {
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.contact-text {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);

  svg {
    width: 18px;
    height: 18px;
    color: var(--color-accent);
  }
}

@media (max-width: 768px) {
  .links-grid {
    grid-template-columns: 1fr;
  }
}
</style>
