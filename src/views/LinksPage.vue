<template>
  <div class="links-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">友链</h1>
      <p class="page-desc">交换友链？随时欢迎！</p>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <!-- Links Grid -->
    <div v-else class="links-grid">
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

      <div v-if="links.length === 0" class="empty-tip">
        暂无友链
      </div>
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
import { ref, onMounted } from 'vue'
import { friendLinksApi } from '../api/frontend'

// 加载状态
const loading = ref(true)

// 友链数据
const links = ref([])

// 从API加载数据
const loadLinks = async () => {
  try {
    loading.value = true
    const res = await friendLinksApi.list()
    links.value = res.data.map(item => ({
      name: item.username,
      description: item.signature || '暂无签名',
      url: item.link_url,
      avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
    }))
  } catch (error) {
    console.error('加载友链失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLinks()
})
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

/* Loading & Empty States */
.loading-state {
  display: flex;
  justify-content: center;
  padding: var(--spacing-3xl);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-3xl);
}
</style>
