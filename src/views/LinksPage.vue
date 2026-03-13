<template>
  <div class="links-page">
    <!-- Page Header -->
    <header class="page-header">
      <h1 class="page-title">友链</h1>
      <p class="page-desc">山海相逢，心意相通</p>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
    </div>

    <!-- Links by Category -->
    <div v-else>
      <!-- Best Friends (挚友) -->
      <div v-if="bestFriends.length > 0" class="link-section">
        <h2 class="section-title">挚友</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in bestFriends"
            :key="'best-' + index"
            :href="link.url"
            target="_blank"
            class="link-card best-friend"
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
      </div>

      <!-- Friends (朋友) -->
      <div v-if="friends.length > 0" class="link-section">
        <h2 class="section-title">朋友</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in friends"
            :key="'friend-' + index"
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
      </div>

      <!-- Visitors (来客) -->
      <div v-if="visitors.length > 0" class="link-section">
        <h2 class="section-title">来客</h2>
        <div class="links-grid">
          <a
            v-for="(link, index) in visitors"
            :key="'visitor-' + index"
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
      </div>

      <div v-if="links.length === 0" class="empty-tip">
        暂无友链
      </div>
    </div>

    <!-- Contact Section -->
    <div class="contact-section">
      <h2 class="section-title">交换友链</h2>
      <p class="contact-text">如果你想交换友链，可以在下方评论发出你的友链信息或用邮箱联系我，我看到之后会第一时间添加的</p>

      <!-- 默认友链信息 -->
      <div class="info-block">
        <h3 class="info-title">友链信息</h3>
        <pre class="code-block">name: MoZhi's Blog
link: https://blog.mozhi.top
avatar: https://mozhi.s3.bitiful.net/cropped-tou.jpg
descr: 远方很远，步履不停，未来可期</pre>
      </div>

      <!-- HTML版信息 -->
      <div class="info-block">
        <h3 class="info-title">HTML</h3>
        <pre class="code-block">&lt;a href="https://blog.mozhi.top"&gt;&lt;img src="https://mozhi.s3.bitiful.net/cropped-tou.jpg" alt="avatar"&gt;MoZhi's Blog&lt;/a&gt;</pre>
      </div>
    </div>

    <!-- Twikoo Comments Section -->
    <section class="comments-section">
      <h2 class="section-title">评论</h2>
      <div id="twikoo-container">
        <div id="tcomment"></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { friendLinksApi } from '../api/frontend'
import { TWIKOO_ENV_ID, TWIKOO_CONFIG } from '../config/twikoo'

// 加载状态
const loading = ref(true)

// 友链数据
const links = ref([])

// 按权重分类
const bestFriends = computed(() => {
  return links.value.filter(link => link.weight === 0).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
})

const friends = computed(() => {
  return links.value.filter(link => link.weight === 1).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
})

const visitors = computed(() => {
  return links.value.filter(link => link.weight === 2).map(item => ({
    name: item.username,
    description: item.signature || '暂无签名',
    url: item.link_url,
    avatar: item.icon_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${item.username}`
  }))
})

// 从API加载数据
const loadLinks = async () => {
  try {
    loading.value = true
    const res = await friendLinksApi.list()
    links.value = res.data
  } catch (error) {
    console.error('加载友链失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLinks()
  initTwikoo()
})

// 初始化 Twikoo 评论
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
    path: '/links',
    lang: TWIKOO_CONFIG.lang
  })
}
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

.info-block {
  margin-bottom: var(--spacing-lg);
}

.info-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.code-block {
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
  white-space: pre-wrap;
  word-break: break-all;
  overflow-x: auto;
  margin: 0;
}

.comments-section {
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
}

#twikoo-container {
  min-height: 200px;
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
