<template>
  <div class="article-page" v-if="!loading && !notFound">
    <!-- Article Header -->
    <header class="article-header">
      <div class="header-meta">
        <router-link :to="`/category/${article.categorySlug}`" class="category-tag">
          {{ article.category }}
        </router-link>
        <span class="publish-date">{{ formatDate(article.date) }}</span>
      </div>
      <h1 class="article-title">{{ article.title }}</h1>
      <div class="article-tags" v-if="article.tag">
        <span class="tag">#{{ article.tag.name }}</span>
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
        <p class="intro" v-if="article.excerpt">{{ article.excerpt }}</p>

        <!-- 渲染Markdown内容 -->
        <div v-html="renderedContent"></div>
      </div>
    </article>

    <!-- Comments Section -->
    <section class="comments-section">
      <h3 class="comments-title">评论</h3>

      <!-- Comment Form -->
      <div class="comment-form">
        <div class="form-row">
          <input
            v-model="commentForm.nickname"
            type="text"
            placeholder="昵称 *"
            class="comment-input"
          />
          <input
            v-model="commentForm.email"
            type="email"
            placeholder="邮箱（选填）"
            class="comment-input"
          />
        </div>
        <textarea
          v-model="commentForm.content"
          placeholder="写下你的评论... *"
          class="comment-textarea"
          rows="4"
        ></textarea>
        <div class="form-footer">
          <span v-if="commentError" class="error-text">{{ commentError }}</span>
          <button class="submit-btn" @click="submitComment" :disabled="submitting">
            {{ submitting ? '提交中...' : '提交评论' }}
          </button>
        </div>
      </div>

      <!-- Comments List -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-author">{{ comment.nickname }}</span>
            <span class="comment-time">{{ formatDate(comment.date) }}</span>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
        </div>
        <div v-if="comments.length === 0" class="no-comments">
          暂无评论，快来抢沙发吧~
        </div>
      </div>
    </section>
  </div>

  <!-- Loading State -->
  <div v-else-if="loading" class="loading-state">
    <div class="loading-spinner"></div>
    <p>加载中...</p>
  </div>

  <!-- Not Found State -->
  <div v-else class="not-found-state">
    <h2>文章不存在</h2>
    <router-link to="/" class="back-home">返回首页</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { useReadingStore } from '../stores/reading'
import { useActiveAnchor, useScrollObserver } from '../composables/useObserver'
import { articlesApi, commentsApi } from '../api/frontend'

const route = useRoute()
const readingStore = useReadingStore()

// Font size
const fontSize = computed(() => readingStore.currentFontSize)

// 加载状态
const loading = ref(true)
const notFound = ref(false)

// 文章数据
const article = ref({
  id: route.params.id,
  title: '',
  excerpt: '',
  date: '',
  category: '',
  categorySlug: '',
  tag: null,
  content: ''
})

// 从API加载文章
const loadArticle = async () => {
  try {
    loading.value = true
    notFound.value = false
    const id = route.params.id

    const res = await articlesApi.detail(id)
    const data = res.data

    article.value = {
      id: data.id,
      title: data.title,
      excerpt: data.summary || '',
      date: data.create_time,
      category: data.category?.name || '',
      categorySlug: data.category?.name || '',
      tag: data.tag || null,
      content: data.content
    }

    // 加载评论
    loadComments()
  } catch (error) {
    console.error('加载文章失败:', error)
    notFound.value = true
  } finally {
    loading.value = false
  }
}

// 评论数据
const comments = ref([])

// 加载评论
const loadComments = async () => {
  try {
    const res = await commentsApi.list(route.params.id)
    comments.value = res.data.map(c => ({
      id: c.id,
      nickname: c.nickname,
      content: c.content,
      date: c.create_time
    }))
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

// Table of Contents - 从Markdown解析
const toc = computed(() => {
  if (!article.value.content) return []
  const headings = []
  const lines = article.value.content.split('\n')
  let currentLevel = 0

  lines.forEach(line => {
    const match = line.match(/^(#{1,3})\s+(.+)$/)
    if (match) {
      const level = match[1].length
      const text = match[2]
      const id = text.toLowerCase().replace(/[^\u4e00-\u9fa5a-z0-9]+/g, '-')
      headings.push({ id, text, level })
    }
  })

  return headings
})

// 渲染Markdown内容
const renderedContent = computed(() => {
  if (!article.value.content) return ''
  return marked(article.value.content)
})

// Image lazy loading
const imageLoaded = ref(false)

// Active anchor tracking
const activeAnchor = ref('')

// Scroll to anchor
const scrollToAnchor = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80
    const top = element.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

// Format date
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 评论提交
const commentForm = ref({
  nickname: '',
  email: '',
  content: ''
})
const submitting = ref(false)
const commentError = ref('')

const submitComment = async () => {
  if (!commentForm.value.nickname || !commentForm.value.content) {
    commentError.value = '请填写昵称和评论内容'
    return
  }

  try {
    submitting.value = true
    commentError.value = ''
    await commentsApi.create({
      article_id: parseInt(route.params.id),
      ...commentForm.value
    })
    // 清空表单
    commentForm.value = { nickname: '', email: '', content: '' }
    // 重新加载评论
    loadComments()
  } catch (error) {
    console.error('提交评论失败:', error)
    commentError.value = '评论发表失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}

// Watch route changes
watch(() => route.params.id, () => {
  loadArticle()
})

onMounted(() => {
  loadArticle()
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

/* Comments Section */
.comments-section {
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
}

.comments-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
}

.comment-form {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.comment-input {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
  }
}

.comment-textarea {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  resize: vertical;
  transition: border-color var(--transition-base);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:focus {
    border-color: var(--color-accent);
  }
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-md);
}

.error-text {
  color: #ff3b30;
  font-size: var(--font-size-sm);
}

.submit-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover:not(:disabled) {
    background: var(--color-accent-hover);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.comment-item {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.comment-author {
  font-weight: 600;
  color: var(--color-text-primary);
}

.comment-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.comment-content {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

.no-comments {
  text-align: center;
  color: var(--color-text-tertiary);
  padding: var(--spacing-xl);
}

/* Loading & Not Found States */
.loading-state,
.not-found-state {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.not-found-state h2 {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.back-home {
  color: var(--color-accent);
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}
</style>
