<template>
  <div class="article-page">
    <!-- Article Header -->
    <header class="article-header">
      <div class="header-meta">
        <router-link :to="`/category/${article.categorySlug}`" class="category-tag">
          {{ article.category }}
        </router-link>
        <span class="publish-date">{{ formatDate(article.date) }}</span>
      </div>
      <h1 class="article-title">{{ article.title }}</h1>
      <div class="article-tags">
        <span v-for="tag in article.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
    </header>

    <!-- Article Content -->
    <article class="article-content" :style="{ '--reading-font-size': fontSize }">
      <!-- Table of Contents -->
      <aside class="toc" v-if="toc.length > 0">
        <h4 class="toc-title">目录</h4>
        <ul class="toc-list">
          <li
            v-for="item in toc"
            :key="item.id"
            class="toc-item"
            :class="{ active: activeAnchor === item.id }"
          >
            <a :href="`#${item.id}`" @click.prevent="scrollToAnchor(item.id)">
              {{ item.text }}
            </a>
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <div class="content-body" ref="contentRef">
        <p class="intro">{{ article.excerpt }}</p>

        <h2 id="section-1">开始之前</h2>
        <p>
          在现代前端开发中，用户体验已经成为了一个不可或缺的部分。一个好的用户体验不仅仅是功能的实现，更是细节的体现。苹果公司作为全球最具影响力的科技公司之一，其设计哲学一直为业界所称道。
        </p>
        <p>
          极简主义设计并不意味着简陋，而是通过精心的设计，让每一个元素都有其存在的意义。在这篇文章中，我们将探讨如何在前端项目中实现这种设计理念。
        </p>

        <h2 id="section-2">核心设计原则</h2>
        <p>
          <strong>留白</strong>是极简设计的核心之一。适当的留白可以让页面看起来更加清爽，也让用户能够更专注于内容本身。
        </p>

        <h3 id="section-2-1">色彩运用</h3>
        <p>
          在色彩选择上，我们应该遵循「少即是多」的原则。使用低饱和度的颜色可以让页面看起来更加高级，同时也能减少视觉疲劳。
        </p>

        <figure class="article-image">
          <img
            src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200"
            alt="代码示例"
            loading="lazy"
            @load="imageLoaded = true"
            :class="{ loaded: imageLoaded }"
          />
          <figcaption>优雅的代码编辑器界面</figcaption>
        </figure>

        <h2 id="section-3">动效设计</h2>
        <p>
          细腻的动效可以提升用户体验，但要注意动效不应该过于夸张。一个好的动效应该是自然、流畅的，让用户感受到流畅而不是干扰。
        </p>

        <blockquote>
          <p>「设计不仅仅是外观和感觉。设计是关于它如何运作的。」—— 史蒂夫·乔布斯</p>
        </blockquote>

        <h2 id="section-4">总结</h2>
        <p>
          通过这篇文章，我们了解了极简设计的核心原则，以及如何在前端项目中实现这些原则。希望这些内容能够帮助你在未来的项目中创造出更好的用户体验。
        </p>
      </div>
    </article>

    <!-- Related Articles -->
    <section class="related-articles">
      <h3 class="related-title">相关文章</h3>
      <div class="related-grid">
        <router-link
          v-for="related in relatedArticles"
          :key="related.id"
          :to="`/article/${related.id}`"
          class="related-card"
        >
          <h4>{{ related.title }}</h4>
          <span class="related-date">{{ formatDate(related.date) }}</span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useReadingStore } from '../stores/reading'
import { useActiveAnchor, useScrollObserver } from '../composables/useObserver'

const route = useRoute()
const readingStore = useReadingStore()

// Font size
const fontSize = computed(() => readingStore.currentFontSize)

// Mock article data
const article = ref({
  id: route.params.id,
  title: '探索 Vue 3 Composition API 的最佳实践',
  excerpt: '深入理解 Vue 3 的 Composition API，学习如何编写更清晰、可维护的组件代码。',
  date: '2024-01-15',
  category: '技术',
  categorySlug: 'tech',
  tags: ['Vue', 'JavaScript', '前端']
})

// Table of Contents
const toc = ref([
  { id: 'section-1', text: '开始之前' },
  { id: 'section-2', text: '核心设计原则' },
  { id: 'section-2-1', text: '色彩运用' },
  { id: 'section-3', text: '动效设计' },
  { id: 'section-4', text: '总结' }
])

// Image lazy loading
const imageLoaded = ref(false)

// Active anchor tracking
const { activeAnchor } = useActiveAnchor(toc.value.map(t => t.id))

// Scroll to anchor
const scrollToAnchor = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80
    const top = element.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

// Related articles
const relatedArticles = ref([
  { id: 2, title: 'TypeScript 类型系统详解', date: '2023-12-28' },
  { id: 4, title: 'CSS Grid 布局完全指南', date: '2023-12-15' }
])

// Format date
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Paragraph animation on mount
const contentRef = ref(null)
onMounted(() => {
  const paragraphs = contentRef.value?.querySelectorAll('p, h2, h3, blockquote, figure')
  if (paragraphs) {
    paragraphs.forEach((p, index) => {
      p.style.opacity = '0'
      p.style.transform = 'translateY(10px)'
      p.style.transition = 'opacity 0.3s ease, transform 0.3s ease'

      setTimeout(() => {
        p.style.opacity = '1'
        p.style.transform = 'translateY(0)'
      }, 100 + index * 80)
    })
  }
})
</script>

<style lang="scss" scoped>
/* ============================================
   Article Page - 文章详情页
   ============================================ */
.article-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

/* Article Header */
.article-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--color-divider);
}

.header-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.category-tag {
  padding: 4px 12px;
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: var(--font-size-sm);
  font-weight: 500;
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-accent);
    color: white;
  }
}

.publish-date {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

.article-title {
  font-size: var(--font-size-4xl);
  font-weight: 700;
  line-height: 1.2;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.article-tags {
  display: flex;
  justify-content: center;
  gap: var(--spacing-sm);

  .tag {
    padding: 2px 10px;
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    font-size: var(--font-size-xs);
    border-radius: var(--radius-full);
  }
}

/* Article Content Layout */
.article-content {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: var(--spacing-2xl);

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

/* Table of Contents */
.toc {
  position: sticky;
  top: 100px;
  align-self: start;
  padding: var(--spacing-lg);
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-md);

  @media (max-width: 1024px) {
    display: none;
  }
}

.toc-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.toc-list {
  list-style: none;
}

.toc-item {
  margin-bottom: var(--spacing-sm);

  a {
    display: block;
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
    border-left: 1px solid transparent;
    transition: all var(--transition-base);

    &:hover {
      color: var(--color-accent);
    }
  }

  &.active a {
    color: var(--color-accent);
    border-left-color: var(--color-accent);
    background: var(--color-accent-light);
  }
}

/* Content Body */
.content-body {
  font-size: var(--reading-font-size, var(--font-size-base));
  line-height: var(--line-height-relaxed);

  .intro {
    font-size: 1.1em;
    color: var(--color-text-secondary);
    font-style: italic;
    margin-bottom: var(--spacing-xl);
    padding: var(--spacing-lg);
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-md);
    border-left: 3px solid var(--color-accent);
  }

  h2 {
    font-size: var(--font-size-2xl);
    font-weight: 600;
    margin-top: var(--spacing-2xl);
    margin-bottom: var(--spacing-md);
    padding-top: var(--spacing-md);
    color: var(--color-text-primary);
  }

  h3 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    margin-top: var(--spacing-xl);
    margin-bottom: var(--spacing-sm);
    color: var(--color-text-primary);
  }

  p {
    margin-bottom: var(--spacing-lg);
    color: var(--color-text-primary);
  }

  blockquote {
    margin: var(--spacing-xl) 0;
    padding: var(--spacing-lg);
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-md);
    border-left: 3px solid var(--color-accent);

    p {
      margin: 0;
      font-style: italic;
      color: var(--color-text-secondary);
    }
  }

  strong {
    font-weight: 600;
    color: var(--color-text-primary);
  }
}

/* Article Image */
.article-image {
  margin: var(--spacing-xl) 0;

  img {
    width: 100%;
    border-radius: var(--radius-md);
    background: var(--color-bg-tertiary);
    opacity: 0;
    transition: opacity var(--transition-smooth);

    &.loaded {
      opacity: 1;
    }
  }

  figcaption {
    margin-top: var(--spacing-sm);
    font-size: var(--font-size-sm);
    color: var(--color-text-tertiary);
    text-align: center;
  }
}

/* Related Articles */
.related-articles {
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
}

.related-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.related-card {
  display: block;
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all var(--transition-smooth);

  h4 {
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-xs);
    transition: color var(--transition-base);
  }

  .related-date {
    font-size: var(--font-size-sm);
    color: var(--color-text-tertiary);
  }

  &:hover {
    border-color: var(--color-accent);
    box-shadow: var(--shadow-md);

    h4 {
      color: var(--color-accent);
    }
  }
}

@media (max-width: 768px) {
  .article-title {
    font-size: var(--font-size-2xl);
  }

  .related-grid {
    grid-template-columns: 1fr;
  }
}
</style>
