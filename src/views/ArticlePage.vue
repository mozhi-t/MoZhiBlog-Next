<template>
  <div class="article-page" v-if="!loading && !notFound">
    <!-- Article Header -->
    <header class="article-header">
      <div class="header-meta">
        <router-link :to="`/category/${article.categorySlug}`" class="category-tag">
          {{ article.category }}
        </router-link>
      </div>
      <h1 class="article-title">{{ article.title }}</h1>

      <!-- Article Tags -->
      <div class="article-tags" v-if="article.tagList && article.tagList.length > 0">
        <router-link
          v-for="tag in article.tagList"
          :key="tag.id"
          :to="`/tag?id=${tag.id}`"
          class="tag"
        >
          #{{ tag.name }}
        </router-link>
      </div>

      <!-- Article Stats -->
      <div class="article-stats">
        <span class="stat-item">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          发布于 {{ formatDate(article.date, true) }}
        </span>
        <span class="stat-item" v-if="article.updateTime && article.updateTime !== article.date">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          更新于 {{ formatDate(article.updateTime, true) }}
        </span>
        <span class="stat-item">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          {{ article.readCount || 0 }} 阅读
        </span>
        <span class="stat-item">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          {{ wordCount }} 字
        </span>
        <span class="stat-item">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          阅读需 {{ readingTime }} 分钟
        </span>
      </div>
    </header>

    <!-- Article Content -->
    <article class="article-content" :style="{ '--reading-font-size': fontSize }">
      <!-- Table of Contents -->
      <aside class="toc" v-if="toc.length > 0">
        <div class="toc-header">
          <h4 class="toc-title">目录</h4>
          <span class="toc-progress">{{ readingProgress }}%</span>
        </div>
        <ul class="toc-list">
          <li
            v-for="item in toc"
            :key="item.id"
            class="toc-item"
            :class="{ active: activeAnchor === item.id }"
            :style="{ '--level': item.level }"
          >
            <a :href="`#${item.id}`" @click.prevent="scrollToAnchor(item.id)">
              {{ item.text }}
            </a>
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <div class="content-body" ref="contentRef">
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
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import { useReadingStore } from '../stores/reading'
import { useActiveAnchor, useScrollObserver } from '../composables/useObserver'
import { articlesApi, commentsApi } from '../api/frontend'

// 配置 marked 使用 highlight.js
const marked = new Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext'
      return hljs.highlight(code, { language }).value
    }
  }),
  {
    gfm: true,
    breaks: true
  }
)

// 自定义渲染器
const renderer = {
  heading({ tokens, depth }) {
    const text = this.parser.parseInline(tokens)
    const id = text.toLowerCase().replace(/[^\u4e00-\u9fa5a-z0-9]+/g, '-').replace(/^-|-$/g, '')
    return `<h${depth} id="${id}">${text}</h${depth}>`
  }
}

marked.use({ renderer })

const route = useRoute()
const readingStore = useReadingStore()

// Font size
const fontSize = computed(() => readingStore.currentFontSize)

const loading = ref(true)
const notFound = ref(false)

// 文章数据
const article = ref({
  id: route.params.id,
  title: '',
  date: '',
  updateTime: '',
  category: '',
  categorySlug: '',
  tagList: [],
  content: '',
  readCount: 0
})

// 计算字数
const wordCount = computed(() => {
  if (!article.value.content) return 0
  // 计算纯文本字数
  const text = article.value.content
    .replace(/```[\s\S]*?```/g, '') // 移除代码块
    .replace(/`[^`]+`/g, '') // 移除行内代码
    .replace(/!\[.*?\]\(.*?\)/g, '') // 移除图片
    .replace(/\[.*?\]\(.*?\)/g, '') // 移除链接
    .replace(/[#*_~>`\-]/g, '') // 移除 Markdown 符号
    .replace(/\n+/g, '') // 移除换行
  return text.length
})

// 计算阅读时间（每分钟300字）
const readingTime = computed(() => {
  if (wordCount.value === 0) return 0
  return Math.ceil(wordCount.value / 300)
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
      date: data.create_time,
      updateTime: data.update_time,
      category: data.category?.name || '',
      categorySlug: data.category?.name || '',
      tagList: data.tag_list || [],
      content: data.content,
      readCount: data.read_count || 0
    }

    // 设置标题滚动监听
    setupHeadingObserver()
    activeAnchor.value = ''

    // 加载评论
    loadComments()

    // 添加代码块头部
    setTimeout(addCodeBlockHeader, 100)
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

  lines.forEach(line => {
    const match = line.match(/^(#{1,3})\s+(.+)$/)
    if (match) {
      const level = match[1].length
      const text = match[2]
      const id = text.toLowerCase().replace(/[^\u4e00-\u9fa5a-z0-9]+/g, '-').replace(/^-|-$/g, '')
      headings.push({ id, text, level })
    }
  })

  return headings
})

// 渲染Markdown内容
const renderedContent = computed(() => {
  if (!article.value.content) return ''
  return marked.parse(article.value.content)
})

// Image lazy loading
const imageLoaded = ref(false)

// Active anchor tracking
const activeAnchor = ref('')

// 阅读进度
const readingProgress = ref(0)

// 计算阅读进度
const calculateProgress = () => {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  if (docHeight > 0) {
    readingProgress.value = Math.min(100, Math.round((scrollTop / docHeight) * 100))
  }
}

// Scroll to anchor
const scrollToAnchor = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80
    const top = element.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

// Format date (with time for article metadata)
const formatDate = (date, includeTime = false) => {
  if (!date) return ''
  if (includeTime) {
    return new Date(date).toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
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

// 监听文章内容变化，重新添加代码块头部
watch(article, (newArticle) => {
  if (newArticle?.content) {
    setTimeout(addCodeBlockHeader, 100)
  }
}, { deep: true })

// 监听标题滚动位置
let headingObserver = null

const setupHeadingObserver = () => {
  if (headingObserver) {
    headingObserver.disconnect()
  }

  // 等待 DOM 更新
  setTimeout(() => {
    const headings = document.querySelectorAll('.content-body h1, .content-body h2, .content-body h3')
    if (headings.length === 0) return

    const observerOptions = {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0
    }

    headingObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeAnchor.value = entry.target.id
        }
      })
    }, observerOptions)

    headings.forEach((heading) => {
      headingObserver.observe(heading)
    })
  }, 100)
}

onMounted(() => {
  loadArticle()
  calculateProgress()
  window.addEventListener('scroll', handleScroll, { passive: true })
  // 渲染完成后添加代码块的语言标签和复制按钮
  setTimeout(addCodeBlockHeader, 100)
})

// 动态添加代码块的语言标签和复制按钮
const addCodeBlockHeader = () => {
  const codeBlocks = document.querySelectorAll('.content-body pre')
  codeBlocks.forEach(pre => {
    if (pre.parentNode?.classList.contains('code-block-wrapper')) return // 已处理过

    const codeEl = pre.querySelector('code')
    if (!codeEl) return // 没有 code 元素

    const code = codeEl?.textContent || ''
    // 获取语言
    const langEl = codeEl.classList.value.match(/language-(\S+)/)
    const lang = langEl ? langEl[1] : 'text'

    // 创建包装元素
    const wrapper = document.createElement('div')
    wrapper.className = 'code-block-wrapper'

    // 创建头部
    const header = document.createElement('div')
    header.className = 'code-header'
    header.innerHTML = `
      <span class="code-lang">${lang}</span>
      <button class="copy-btn" data-code="${encodeURIComponent(code)}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span>复制</span>
      </button>
    `

    // 将 pre 包装到 wrapper 中
    pre.parentNode?.insertBefore(wrapper, pre)
    wrapper.appendChild(header)
    wrapper.appendChild(pre)
  })

  // 绑定复制按钮事件
  document.querySelectorAll('.content-body .copy-btn').forEach(btn => {
    btn.onclick = async () => {
      const code = decodeURIComponent(btn.dataset.code || '')
      try {
        await navigator.clipboard.writeText(code)
        const span = btn.querySelector('span')
        span.textContent = '已复制'
        btn.classList.add('copied')
        setTimeout(() => {
          span.textContent = '复制'
          btn.classList.remove('copied')
        }, 2000)
      } catch (err) {
        console.error('复制失败:', err)
      }
    }
  })
}

onUnmounted(() => {
  if (headingObserver) {
    headingObserver.disconnect()
  }
  window.removeEventListener('scroll', handleScroll)
})

// 滚动处理函数
const handleScroll = () => {
  calculateProgress()
}
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
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);

  .tag {
    padding: 4px 12px;
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    font-size: var(--font-size-xs);
    border-radius: var(--radius-full);
    text-decoration: none;
    transition: all var(--transition-base);

    &:hover {
      background: var(--color-accent-light);
      color: var(--color-accent);
    }
  }
}

.article-stats {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-md);

  .stat-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: var(--font-size-sm);
    color: var(--color-text-tertiary);

    .icon {
      width: 14px;
      height: 14px;
      opacity: 0.7;
    }
  }
}

/* Article Content Layout */
.article-content {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: var(--spacing-2xl);
  align-items: start;
  max-width: 1200px;
  margin: 0 auto;

  @media (max-width: 1200px) {
    grid-template-columns: 240px 1fr;
    max-width: 1000px;
  }

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
  padding-left: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);

  @media (max-width: 1024px) {
    display: none;
  }
}

.toc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--color-divider);
}

.toc-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.toc-progress {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-accent);
  background: var(--color-accent-light);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.toc-list {
  list-style: none;
  max-height: 60vh;
  overflow-y: auto;
  margin-left: -4px;

  /* 隐藏滚动条但保持滚动功能 */
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: var(--color-border);
    border-radius: 2px;
  }
}

.toc-item {
  margin-bottom: 4px;
  position: relative;

  a {
    display: block;
    padding: 10px 16px;
    padding-left: 20px;
    font-size: 16px;
    color: var(--color-text-secondary);
    text-decoration: none;
    border-radius: var(--radius-sm);
    transition: all 0.25s ease;
    line-height: 1.4;
    overflow: visible;
    white-space: normal;
    word-break: break-word;

    &:hover {
      color: var(--color-accent);
      background: var(--color-accent-light);
    }
  }

  /* 左侧圆角矩形条 */
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 0;
    background: var(--color-accent);
    border-radius: 2px;
    transition: all 0.25s ease;
    opacity: 0;
  }

  &:hover::before {
    height: 60%;
    opacity: 0.5;
  }

  /* 根据标题级别调整缩进 */
  &[style*="--level: 1"] a {
    padding-left: 20px;
    font-weight: 500;
  }

  &[style*="--level: 2"] a {
    padding-left: 32px;
    font-size: 15px;
  }

  &[style*="--level: 3"] a {
    padding-left: 44px;
    font-size: 15px;
    color: var(--color-text-tertiary);
  }

  &[style*="--level: 2"]::before,
  &[style*="--level: 3"]::before {
    left: 12px;
  }

  &.active {
    a {
      color: var(--color-accent);
      background: var(--color-accent-light);
      font-weight: 500;
    }

    &::before {
      height: 70%;
      opacity: 1;
    }
  }
}

/* Content Body */
.content-body {
  font-size: var(--reading-font-size, var(--font-size-base));
  line-height: var(--line-height-relaxed);
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;

  /* ============================================
     Markdown 内容样式 - 苹果风格
     ============================================ */

  /* 标题样式 */
  :deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
    position: relative;
    transition: all 0.3s ease;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%) scale(0.8);
      font-size: 12px;
      font-weight: 600;
      color: var(--color-accent);
      padding: 1px 4px;
      border-radius: 3px;
      opacity: 0;
      filter: blur(4px);
      transition: all 0.3s ease;
    }

    &:hover {
      padding-left: 20px;

      &::before {
        opacity: 1;
        filter: blur(0);
        transform: translateY(-50%) scale(1);
      }
    }
  }

  :deep(h1) {
    font-size: 31px;
    font-weight: 500;
    color: var(--color-text-primary);
    line-height: 1.4;
    margin-top: 24px;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--color-divider);

    &::before {
      content: 'H1';
    }

    @media (max-width: 768px) {
      font-size: 27px;
    }
  }

  :deep(h2) {
    font-size: 27px;
    font-weight: 500;
    color: var(--color-text-primary);
    line-height: 1.4;
    margin-top: 24px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--color-accent);

    &::before {
      content: 'H2';
    }

    @media (max-width: 768px) {
      font-size: 23px;
    }
  }

  :deep(h3) {
    font-size: 23px;
    font-weight: 500;
    color: var(--color-text-primary);
    line-height: 1.4;
    margin-top: 24px;
    margin-bottom: 16px;

    &::before {
      content: 'H3';
    }

    @media (max-width: 768px) {
      font-size: 21px;
    }
  }

  :deep(h4), :deep(h5), :deep(h6) {
    font-size: 19px;
    font-weight: 500;
    color: var(--color-text-primary);
    line-height: 1.4;
    margin-top: 24px;
    margin-bottom: 16px;

    &::before {
      content: 'H4';
      color: var(--color-text-tertiary);
    }
  }

  /* 段落样式 */
  :deep(p) {
    font-size: 19px;
    color: var(--color-text-primary);
    line-height: 1.8;
    margin: 16px 0;
    text-indent: 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;

    @media (max-width: 768px) {
      font-size: 18px;
    }
  }

  /* 链接样式 */
  :deep(a) {
    color: var(--color-accent);
    text-decoration: none;
    transition: all 0.2s;

    &:hover {
      text-decoration: underline;
    }
  }

  /* 强调样式 */
  :deep(em) {
    font-style: italic;
    color: var(--color-text-primary);
  }

  :deep(strong) {
    font-weight: 700;
    color: var(--color-text-primary);
  }

  /* 列表样式 */
  :deep(ul), :deep(ol) {
    margin: 16px 0;
    padding-left: 0;
    list-style: none;
  }

  :deep(li) {
    margin: 12px 0;
    color: var(--color-text-primary);
    line-height: 1.8;
    position: relative;
    padding-left: 20px;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 10px;
      width: 6px;
      height: 6px;
      background: var(--color-accent);
      border-radius: 50%;
    }
  }

  :deep(ol li) {
    padding-left: 30px;
    counter-increment: item;

    &::before {
      content: counter(item);
      background: none;
      width: auto;
      height: auto;
      color: var(--color-text-tertiary);
      font-size: 14px;
      top: 12px;
      left: 0;
    }
  }

  /* 引用样式 */
  :deep(blockquote) {
    margin: 20px 0;
    padding: 16px;
    background: var(--color-bg-tertiary);
    border-left: 4px solid var(--color-accent);
    border-radius: 8px;

    p {
      margin: 0;
      font-size: 15px;
      color: var(--color-text-tertiary);
      line-height: 1.7;
    }
  }

  /* 代码块样式 */
  :deep(.code-block-wrapper) {
    margin: 20px 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.06),
      0 4px 16px rgba(0, 0, 0, 0.08);
  }

  :deep(.code-block-wrapper pre) {
    white-space: pre-wrap;
    word-break: break-all;
  }

  :deep(.code-block-wrapper code) {
    white-space: pre-wrap;
    word-break: break-all;
  }

  :deep(.code-block-wrapper pre code) {
    white-space: pre-wrap;
    word-break: break-all;
  }

  :deep(.code-header) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    background: var(--color-bg-secondary);
    border-bottom: 1px solid var(--color-border);
    border-radius: 12px 12px 0 0;
  }

  :deep(.code-block-wrapper pre) {
    border-radius: 0 0 12px 12px;
  }

  :deep(.code-lang) {
    font-size: 12px;
    font-weight: 500;
    color: var(--color-accent);
    text-transform: lowercase;
  }

  :deep(.copy-btn) {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    background: transparent;
    border: 1px solid var(--color-border);
    border-radius: 4px;
    font-size: 12px;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;

    svg {
      width: 14px;
      height: 14px;
    }

    &:hover {
      background: var(--color-accent-light);
      border-color: var(--color-accent);
      color: var(--color-accent);
    }

    &.copied {
      background: var(--color-accent);
      border-color: var(--color-accent);
      color: white;
    }
  }

  :deep(pre) {
    background: var(--color-bg-tertiary);
    backdrop-filter: blur(4px);
    padding: 20px;
    margin: 0;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: pre-wrap;
    word-break: break-all;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  :deep(code) {
    background: #e8e8e8;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 14px;
    color: #4a4a4a;
    font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
    white-space: pre-wrap;
    word-break: break-all;
    border: 1px solid #d4d4d4;
  }

  :deep(pre code) {
    background: transparent;
    padding: 0;
    font-size: 14px;
    line-height: 1.6;
    color: var(--color-text-primary);
    white-space: pre-wrap;
    word-break: break-all;
    border: none;
  }

  /* 图片样式 */
  :deep(img) {
    max-width: 100%;
    border-radius: 12px;
    margin: 20px 0;
    display: block;
    margin-left: auto;
    margin-right: auto;
    transition: all 0.3s;

    &:hover {
      transform: scale(1.01);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
  }

  /* 表格样式 */
  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    border-radius: 8px;
    overflow: hidden;
  }

  :deep(th), :deep(td) {
    padding: 12px;
    text-align: left;
  }

  :deep(th) {
    background: var(--color-bg-tertiary);
    font-weight: 600;
    color: var(--color-text-primary);
    border-bottom: 1px solid var(--color-divider);
  }

  :deep(td) {
    color: var(--color-text-primary);
    border-bottom: 1px solid var(--color-divider);
  }

  :deep(tr:hover td) {
    background: var(--color-accent-light);
  }

  /* 分割线 */
  :deep(hr) {
    border: none;
    border-top: 1px solid var(--color-divider);
    margin: 24px 0;
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
