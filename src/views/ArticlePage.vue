<template>
  <div class="article-page-shell">
  <div class="article-page" :class="{ 'article-page-entered': articleIntroVisible }" v-if="!loading && !notFound">
    <!-- Article Header -->
    <header class="article-header">
      <div class="header-meta-row">
        <div class="header-meta-left">
          <button type="button" class="back-button" @click="goBack">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 18l-6-6 6-6"></path>
            </svg>
            <span>返回</span>
          </button>
        </div>
        <div class="header-meta">
          <router-link v-if="article.category" :to="`/category/${article.categorySlug}`" class="category-tag">
            {{ article.category }}
          </router-link>
          <div class="header-badges" v-if="article.isTop || article.needPassword">
            <span v-if="article.isTop" class="header-badge top">置顶</span>
            <span v-if="article.needPassword" class="header-badge password">密码保护</span>
          </div>
        </div>
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

    <section v-if="article.needPassword" class="password-panel">
      <div class="password-card">
        <h3>这是一篇受保护的文章</h3>
        <p>输入正确密码后才能查看正文内容。</p>
        <input
          v-model="passwordInput"
          type="password"
          class="password-input"
          placeholder="请输入访问密码"
          @keyup.enter="verifyPasswordAndReload"
        />
        <button class="unlock-btn" @click="verifyPasswordAndReload" :disabled="verifyingPassword">
          {{ verifyingPassword ? '验证中...' : '解锁文章' }}
        </button>
        <p v-if="passwordError" class="password-error">{{ passwordError }}</p>
      </div>
    </section>

    <!-- Article Content -->
    <article v-else class="article-content" :style="{ '--reading-font-size': fontSize }">
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
            :data-id="item.id"
          >
            <a :href="`#${item.id}`" @click.prevent="scrollToAnchor(item.id)">
              {{ item.text }}
            </a>
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <div class="content-body markdown-content" ref="contentRef" @click="handleContentClick">
        <!-- 渲染Markdown内容 -->
        <div v-html="renderedContent"></div>
        <section class="article-license-card">
          <div class="license-main">
            <span class="category-tag license-category">{{ article.category || '未分类' }}</span>
            <p class="license-title">{{ article.title }}</p>
            <div class="license-meta">
              <span>作者：MoZhi</span>
              <span>发布于 {{ formatDate(article.date, true) }}</span>
              <span>更新于 {{ formatDate(article.updateTime || article.date, true) }}</span>
              <a
                class="license-link"
                :href="CC_LICENSE_URL"
                target="_blank"
                rel="noopener noreferrer"
              >
                许可协议 CC-BY-NC-SA 4.0 国际标准
              </a>
            </div>
            <div class="license-summary">署名 — 非商业性使用 — 相同方式共享 4.0 国际版</div>
          </div>
          <div class="license-mark" aria-hidden="true">©</div>
        </section>
        <div
          v-if="ARTICLE_TIP_QR_CODE"
          ref="tipActionRef"
          class="article-tip-action"
          :class="{ active: isTipPopoverOpen }"
        >
          <div class="tip-popover">
            <img class="tip-qr-image" :src="ARTICLE_TIP_QR_CODE" alt="赞赏收款码" />
          </div>
          <button
            type="button"
            class="tip-button"
            :aria-expanded="isTipPopoverOpen"
            @mousedown="handleTipMouseDown"
            @click="toggleTipPopover"
          >
            <span>投币</span>
          </button>
        </div>
      </div>
    </article>

    <!-- Comments Section -->
    <section v-if="!article.needPassword" class="comments-section">
      <h3 class="comments-title">评论</h3>
      <div id="twikoo-container">
        <div id="tcomment"></div>
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
  <div
    v-if="imagePreview.visible"
    class="image-preview-overlay"
    :class="{ dragging: isDraggingPreview }"
    role="dialog"
    aria-modal="true"
    aria-label="图片预览"
    @pointerdown="startImageDrag"
    @click.self="closeImagePreview"
    @wheel.prevent="handlePreviewWheel"
    @dragstart.prevent
  >
    <button
      type="button"
      class="image-preview-close"
      aria-label="关闭图片预览"
      @click="closeImagePreview"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
        <path d="M6 6l12 12"></path>
        <path d="M18 6l-12 12"></path>
      </svg>
    </button>
    <div
      ref="imagePreviewStageRef"
      class="image-preview-stage"
    >
      <img
        class="image-preview-img"
        :src="imagePreview.src"
        :alt="imagePreview.alt"
        draggable="false"
        :style="{ transform: `translate(${imagePreview.offsetX}px, ${imagePreview.offsetY}px) scale(${imagePreview.scale})` }"
      />
    </div>
    <div class="image-preview-toolbar">
      <button
        type="button"
        class="image-preview-control"
        aria-label="缩小图片"
        :disabled="!canZoomOut"
        @click="zoomOutImage"
      >
        -
      </button>
      <span class="image-preview-ratio">{{ imagePreviewScaleText }}</span>
      <button
        type="button"
        class="image-preview-control"
        aria-label="放大图片"
        :disabled="!canZoomIn"
        @click="zoomInImage"
      >
        +
      </button>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReadingStore } from '../stores/reading'
import { articlesApi } from '../api/frontend'
import { SITE_CONFIG } from '../config/site'
import { TWIKOO_ENV_ID, TWIKOO_CONFIG } from '../config/twikoo'
import { enhanceCodeBlocks, hydrateArticleReferences, renderMarkdown } from '../utils/markdown'
import { updateSeo, stripHtml, truncate } from '../utils/seo'

const route = useRoute()
const router = useRouter()
const readingStore = useReadingStore()
const CC_LICENSE_URL = 'https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans'
const ARTICLE_TIP_QR_CODE = SITE_CONFIG.article?.tipQrCode || ''

const goBack = () => {
  const hasRouterBack = typeof window !== 'undefined' && window.history.state?.back
  let hasSameOriginReferrer = false

  if (typeof document !== 'undefined' && document.referrer) {
    try {
      hasSameOriginReferrer = new URL(document.referrer).origin === window.location.origin
    } catch {
      hasSameOriginReferrer = false
    }
  }

  if (hasRouterBack || hasSameOriginReferrer) {
    router.back()
    return
  }

  router.push('/')
}

const toggleTipPopover = () => {
  if (typeof window !== 'undefined' && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    return
  }
  isTipPopoverOpen.value = !isTipPopoverOpen.value
}

const handleTipMouseDown = (event) => {
  if (typeof window !== 'undefined' && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    event.preventDefault()
  }
}

const handleGlobalPointerDown = (event) => {
  if (!tipActionRef.value?.contains(event.target)) {
    isTipPopoverOpen.value = false
  }
}

// Font size
const fontSize = computed(() => readingStore.currentFontSize)

const loading = ref(true)
const notFound = ref(false)
const passwordInput = ref('')
const passwordError = ref('')
const verifyingPassword = ref(false)
const contentRef = ref(null)
const imagePreviewStageRef = ref(null)
const tipActionRef = ref(null)
const isTipPopoverOpen = ref(false)
const articleIntroVisible = ref(false)
const IMAGE_PREVIEW_MIN_SCALE = 0.5
const IMAGE_PREVIEW_MAX_SCALE = 3
const IMAGE_PREVIEW_STEP = 0.25
const IMAGE_PREVIEW_WHEEL_STEP = 0.05
const imagePreview = ref({
  visible: false,
  src: '',
  alt: '',
  scale: 1,
  offsetX: 0,
  offsetY: 0
})
const isDraggingPreview = ref(false)
let isPageActive = true
let codeBlockTimer = null
let headingObserverTimer = null
let twikooScriptLoading = false
const previewDragState = {
  pointerId: null,
  startX: 0,
  startY: 0,
  originX: 0,
  originY: 0
}

// 文章数据
const article = ref({
  id: route.params.id,
  title: '',
  summary: '',
  date: '',
  updateTime: '',
  category: '',
  categorySlug: '',
  tagList: [],
  content: '',
  readCount: 0,
  isTop: false,
  needPassword: false
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

const scheduleCodeBlockEnhancement = () => {
  if (codeBlockTimer) {
    clearTimeout(codeBlockTimer)
  }

  codeBlockTimer = window.setTimeout(() => {
    codeBlockTimer = null
    if (!isPageActive) return
    addCodeBlockHeader()
  }, 100)
}

const playArticleIntro = () => {
  articleIntroVisible.value = false

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      if (!isPageActive) return
      articleIntroVisible.value = true
    })
  })
}

// 从API加载文章
const loadArticle = async () => {
  try {
    loading.value = true
    notFound.value = false
    passwordError.value = ''
    articleIntroVisible.value = false
    const id = route.params.id

    const res = await articlesApi.detail(id)
    const data = res.data

    article.value = {
      id: data.id,
      title: data.title,
      summary: data.summary || '',
      date: data.create_time,
      updateTime: data.update_time,
      category: data.category?.name || '',
      categorySlug: data.category?.name || '',
      tagList: data.tag_list || [],
      content: data.content || '',
      readCount: data.read_count || 0,
      isTop: !!data.is_top,
      needPassword: !!data.need_password
    }

    if (!data.need_password) {
      setupHeadingObserver()
      activeAnchor.value = ''
      scheduleCodeBlockEnhancement()
      initTwikoo()
    }

    nextTick(() => {
      playArticleIntro()
    })
  } catch (error) {
    console.error('加载文章失败:', error)
    notFound.value = true
  } finally {
    loading.value = false
  }
}

const verifyPasswordAndReload = async () => {
  if (!passwordInput.value.trim()) {
    passwordError.value = '请输入访问密码'
    return
  }

  try {
    verifyingPassword.value = true
    passwordError.value = ''
    const res = await articlesApi.verifyPassword(route.params.id, passwordInput.value.trim())
    if (!res.data?.passed) {
      passwordError.value = '密码错误，请重新输入'
      return
    }

    if (res.data?.access_token) {
      sessionStorage.setItem(`article_access_${route.params.id}`, res.data.access_token)
    }

    passwordInput.value = ''
    await loadArticle()
  } catch (error) {
    passwordError.value = error.response?.data?.detail || error.message || '密码验证失败'
  } finally {
    verifyingPassword.value = false
  }
}

// 初始化 Twikoo 评论
const initTwikoo = () => {
  // 确保 DOM 已渲染
  nextTick(() => {
    if (!isPageActive || !document.querySelector(TWIKOO_CONFIG.el)) {
      return
    }

    // 如果 Twikoo 已经加载，直接初始化
    if (window.twikoo) {
      initTwikooInstance()
      return
    }

    // 动态加载 Twikoo 脚本
    if (twikooScriptLoading || document.querySelector('script[src="/twikoo.min.js"]')) {
      return
    }

    const script = document.createElement('script')
    script.src = '/twikoo.min.js'
    twikooScriptLoading = true
    script.onload = () => {
      twikooScriptLoading = false
      if (!isPageActive) {
        return
      }
      initTwikooInstance()
    }
    script.onerror = () => {
      twikooScriptLoading = false
      console.error('Twikoo 脚本加载失败')
    }
    document.head.appendChild(script)
  })
}

// 初始化 Twikoo 实例
const initTwikooInstance = () => {
  if (!isPageActive || !window.twikoo) {
    console.error('Twikoo 未正确加载')
    return
  }

  if (!document.querySelector(TWIKOO_CONFIG.el)) {
    return
  }

  window.twikoo.init({
    envId: TWIKOO_ENV_ID,
    el: TWIKOO_CONFIG.el,
    path: `/article/${route.params.id}`,  // 用于区分不同文章的自定义路径，确保每篇文章评论独立
    lang: TWIKOO_CONFIG.lang
  })
}

// Table of Contents - 从Markdown解析
const toc = computed(() => {
  if (!article.value.content) return []
  const headings = []
  const lines = article.value.content.split('\n')

  lines.forEach(line => {
    const match = line.match(/^(#{1,6})\s+(.+)$/)
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
  return renderMarkdown(article.value.content)
})

// Image lazy loading
const imageLoaded = ref(false)
const canZoomOut = computed(() => imagePreview.value.scale > IMAGE_PREVIEW_MIN_SCALE)
const canZoomIn = computed(() => imagePreview.value.scale < IMAGE_PREVIEW_MAX_SCALE)
const imagePreviewScaleText = computed(() => `${Math.round(imagePreview.value.scale * 100)}%`)

// Active anchor tracking
const activeAnchor = ref('')
let isScrollingToAnchor = false

// 自动滚动目录
watch(activeAnchor, (newId) => {
  if (newId) {
    nextTick(() => {
      const activeItem = document.querySelector(`.toc-item[data-id="${newId}"]`)
      if (activeItem) {
        activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      }
    })
  }
})

// 阅读进度
const readingProgress = ref(0)

// 计算阅读进度
const calculateProgress = () => {
  const scrollTop = window.scrollY
  const contentBody = document.querySelector('.content-body')
  if (!contentBody) return

  const contentTop = contentBody.offsetTop
  const contentHeight = contentBody.offsetHeight
  const scrollableHeight = contentHeight - window.innerHeight

  const relativeScrollTop = scrollTop - contentTop

  if (scrollableHeight > 0) {
    const progress = Math.round((relativeScrollTop / scrollableHeight) * 100)
    readingProgress.value = Math.max(0, Math.min(100, progress))
  }
}

// Scroll to anchor
const scrollToAnchor = (id) => {
  const element = document.getElementById(id)
  if (element) {
    activeAnchor.value = id
    isScrollingToAnchor = true
    const offset = 80
    const top = element.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })

    const onScrollEnd = () => {
      isScrollingToAnchor = false
      window.removeEventListener('scrollend', onScrollEnd)
    }
    window.addEventListener('scrollend', onScrollEnd, { once: true })

    setTimeout(() => {
      isScrollingToAnchor = false
    }, 1500)
  }
}

const setImagePreviewScale = (nextScale) => {
  imagePreview.value.scale = Math.min(
    IMAGE_PREVIEW_MAX_SCALE,
    Math.max(IMAGE_PREVIEW_MIN_SCALE, Number(nextScale.toFixed(2)))
  )

  if (imagePreview.value.scale <= 1) {
    imagePreview.value.offsetX = 0
    imagePreview.value.offsetY = 0
  }
}

const openImagePreview = (src, alt = '') => {
  if (!src) return
  imagePreview.value = {
    visible: true,
    src,
    alt,
    scale: 1,
    offsetX: 0,
    offsetY: 0
  }
  document.body.style.overflow = 'hidden'
}

const closeImagePreview = () => {
  stopImageDrag()
  imagePreview.value.visible = false
  document.body.style.overflow = ''
}

const zoomInImage = () => {
  setImagePreviewScale(imagePreview.value.scale + IMAGE_PREVIEW_STEP)
}

const zoomOutImage = () => {
  setImagePreviewScale(imagePreview.value.scale - IMAGE_PREVIEW_STEP)
}

const handlePreviewWheel = (event) => {
  if (event.target.closest('.image-preview-close, .image-preview-toolbar')) return

  const direction = Math.sign(event.deltaY)
  if (direction === 0) return

  setImagePreviewScale(
    imagePreview.value.scale + (direction < 0 ? IMAGE_PREVIEW_WHEEL_STEP : -IMAGE_PREVIEW_WHEEL_STEP)
  )
}

const startImageDrag = (event) => {
  if (event.button !== 0) return
  if (event.target.closest('.image-preview-close, .image-preview-toolbar')) return

  event.preventDefault()
  previewDragState.pointerId = event.pointerId
  previewDragState.startX = event.clientX
  previewDragState.startY = event.clientY
  previewDragState.originX = imagePreview.value.offsetX
  previewDragState.originY = imagePreview.value.offsetY
  isDraggingPreview.value = true
  imagePreviewStageRef.value?.setPointerCapture?.(event.pointerId)
}

const handleImageDrag = (event) => {
  if (!isDraggingPreview.value || event.pointerId !== previewDragState.pointerId) return

  imagePreview.value.offsetX = previewDragState.originX + (event.clientX - previewDragState.startX)
  imagePreview.value.offsetY = previewDragState.originY + (event.clientY - previewDragState.startY)
}

const stopImageDrag = (event) => {
  if (event && previewDragState.pointerId !== null && event.pointerId !== previewDragState.pointerId) return

  if (previewDragState.pointerId !== null) {
    imagePreviewStageRef.value?.releasePointerCapture?.(previewDragState.pointerId)
  }

  previewDragState.pointerId = null
  isDraggingPreview.value = false
}

const handlePreviewKeydown = (event) => {
  if (event.key === 'Escape' && imagePreview.value.visible) {
    closeImagePreview()
  }
}

const handleContentClick = (event) => {
  const image = event.target.closest('img')
  if (!image || !contentRef.value?.contains(image)) return
  openImagePreview(image.currentSrc || image.src, image.alt || '')
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

watch(
  () => [
    route.params.id,
    loading.value,
    notFound.value,
    article.value.title,
    article.value.summary,
    article.value.content,
    article.value.category,
    article.value.needPassword,
    article.value.date,
    article.value.updateTime,
    article.value.tagList
  ],
  () => {
    if (loading.value) return

    if (notFound.value) {
      updateSeo({
        title: '文章不存在',
        description: '当前访问的文章不存在、已被删除，或暂时无法查看。',
        path: `/article/${route.params.id}`,
        noindex: true
      })
      return
    }

    const descriptionSource = article.value.summary || stripHtml(article.value.content)
    const description = article.value.needPassword
      ? `《${article.value.title}》为受保护文章，输入访问密码后才可查看完整内容。`
      : truncate(descriptionSource || `${article.value.title} - ${SITE_CONFIG.name}`, 160)

    const schema = article.value.needPassword
      ? null
      : {
          '@context': 'https://schema.org',
          '@type': 'BlogPosting',
          headline: article.value.title,
          description,
          author: {
            '@type': 'Person',
            name: SITE_CONFIG.author.name
          },
          datePublished: article.value.date || undefined,
          dateModified: article.value.updateTime || article.value.date || undefined,
          mainEntityOfPage: `${SITE_CONFIG.url}/article/${route.params.id}`,
          articleSection: article.value.category || undefined,
          keywords: article.value.tagList.map(tag => tag.name).join(', ') || undefined
        }

    updateSeo({
      title: article.value.title || '文章详情',
      description,
      path: `/article/${route.params.id}`,
      type: 'article',
      keywords: [
        '文章',
        article.value.category,
        ...article.value.tagList.map(tag => tag.name)
      ].filter(Boolean),
      noindex: article.value.needPassword,
      publishedTime: article.value.date,
      modifiedTime: article.value.updateTime || article.value.date,
      section: article.value.category,
      tags: article.value.tagList.map(tag => tag.name),
      schema
    })
  },
  { deep: true, immediate: true }
)

// Watch route changes
watch(() => route.params.id, () => {
  loadArticle()
})

// 监听文章内容变化，重新添加代码块头部
watch(article, (newArticle) => {
  if (newArticle?.content) {
    scheduleCodeBlockEnhancement()
  }
}, { deep: true })

// 监听标题滚动位置
let headingObserver = null

const setupHeadingObserver = () => {
  if (headingObserver) {
    headingObserver.disconnect()
  }

  // 等待 DOM 更新
  headingObserverTimer = window.setTimeout(() => {
    headingObserverTimer = null
    if (!isPageActive) return
    const headings = document.querySelectorAll('.content-body h1, .content-body h2, .content-body h3, .content-body h4, .content-body h5, .content-body h6')
    if (headings.length === 0) return

    const observerOptions = {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0
    }

    headingObserver = new IntersectionObserver((entries) => {
      // 点击目录滚动时跳过 Observer 更新，避免高亮错乱
      if (isScrollingToAnchor) return

      // 找到所有相交的标题，根据它们在页面中的实际位置排序，选择最上面的
      const intersectingEntries = entries.filter(entry => entry.isIntersecting)
      if (intersectingEntries.length > 0) {
        // 按照页面中的实际位置排序，找到最上面的标题
        intersectingEntries.sort((a, b) => {
          return a.target.getBoundingClientRect().top - b.target.getBoundingClientRect().top
        })
        activeAnchor.value = intersectingEntries[0].target.id
      }
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
  window.addEventListener('keydown', handlePreviewKeydown)
  window.addEventListener('pointermove', handleImageDrag)
  window.addEventListener('pointerup', stopImageDrag)
  window.addEventListener('pointercancel', stopImageDrag)
  document.addEventListener('pointerdown', handleGlobalPointerDown)
  // 渲染完成后添加代码块的语言标签和复制按钮
  scheduleCodeBlockEnhancement()
})

const addCodeBlockHeader = () => {
  const contentRoot = contentRef.value
  if (!contentRoot) return

  enhanceCodeBlocks(contentRoot)

  hydrateArticleReferences(contentRoot, async (id) => {
    const res = await articlesApi.reference(id)
    return res.data
  })
}

onUnmounted(() => {
  isPageActive = false
  if (headingObserver) {
    headingObserver.disconnect()
  }
  if (headingObserverTimer) {
    clearTimeout(headingObserverTimer)
    headingObserverTimer = null
  }
  if (codeBlockTimer) {
    clearTimeout(codeBlockTimer)
    codeBlockTimer = null
  }
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('keydown', handlePreviewKeydown)
  window.removeEventListener('pointermove', handleImageDrag)
  window.removeEventListener('pointerup', stopImageDrag)
  window.removeEventListener('pointercancel', stopImageDrag)
  document.removeEventListener('pointerdown', handleGlobalPointerDown)
  document.body.style.overflow = ''
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

.article-header,
.password-panel,
.article-content,
.comments-section {
  opacity: 0;
  transform: translateY(18px) scale(0.992);
  filter: blur(10px);
  transition:
    opacity 0.42s ease,
    transform 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    filter 0.42s ease;
  will-change: opacity, transform, filter;
}

.article-page-entered .article-header,
.article-page-entered .password-panel,
.article-page-entered .article-content,
.article-page-entered .comments-section {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0);
}

.article-page-entered .article-header {
  transition-delay: 0.04s;
}

.article-page-entered .password-panel,
.article-page-entered .article-content {
  transition-delay: 0.1s;
}

.article-page-entered .comments-section {
  transition-delay: 0.18s;
}

/* Article Header */
.article-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--color-divider);
}

.header-meta-row {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: var(--spacing-md);
  min-height: 40px;
}

.header-meta-left {
  position: absolute;
  left: 96px;
  top: 50%;
  transform: translateY(-50%);
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
  line-height: 1;
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 16px;
    height: 16px;
    transition: transform var(--transition-base);
  }

  &:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
    background: var(--color-accent-light);

    svg {
      transform: translateX(-2px);
    }
  }
}

.header-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.header-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: var(--font-size-xs);
  font-weight: 600;

  &.top {
    color: #b85c00;
    background: rgba(255, 183, 77, 0.22);
  }

  &.password {
    color: #8a3ffc;
    background: rgba(138, 63, 252, 0.12);
  }
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

@media (max-width: 768px) {
  .header-meta-row {
    flex-direction: column;
    gap: var(--spacing-sm);
    min-height: auto;
  }

  .header-meta-left {
    position: static;
    transform: none;
    align-self: flex-start;
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

.password-panel {
  max-width: 640px;
  margin: 0 auto;
}

.password-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding: var(--spacing-2xl);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  text-align: center;

  h3 {
    margin: 0;
    color: var(--color-text-primary);
  }

  p {
    margin: 0;
    color: var(--color-text-secondary);
  }
}

[data-theme="dark"] .password-card {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

.password-input {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  outline: none;

  &:focus {
    border-color: var(--color-accent);
  }
}

.unlock-btn {
  align-self: center;
  min-width: 140px;
  padding: var(--spacing-sm) var(--spacing-xl);
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-accent);
  color: #fff;
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

.password-error {
  color: #d92d20 !important;
  font-size: var(--font-size-sm);
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
  max-height: calc(100vh - 140px);
  overflow-y: auto;

  @media (max-width: 1024px) {
    display: none;
  }
}

[data-theme="dark"] .toc {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
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
    color: var(--color-text-primary);
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

  &[style*="--level: 4"] a {
    padding-left: 56px;
    font-size: 14px;
    color: var(--color-text-tertiary);
  }

  &[style*="--level: 5"] a {
    padding-left: 68px;
    font-size: 14px;
    color: var(--color-text-tertiary);
  }

  &[style*="--level: 6"] a {
    padding-left: 80px;
    font-size: 14px;
    color: var(--color-text-tertiary);
  }

  &[style*="--level: 4"]::before,
  &[style*="--level: 5"]::before,
  &[style*="--level: 6"]::before {
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
}

.content-body :deep(img) {
  cursor: zoom-in;
}

.image-preview-overlay {
  position: fixed;
  inset: 0;
  z-index: 1200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 24px 112px;
  background: rgba(15, 23, 42, 0.86);
  backdrop-filter: blur(10px);
  cursor: grab;

  &.dragging {
    cursor: grabbing;
  }
}

.image-preview-close {
  position: absolute;
  top: 24px;
  right: 24px;
  z-index: 2;
  width: 48px;
  height: 48px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition:
    background 0.2s ease,
    transform 0.2s ease,
    border-color 0.2s ease;

  svg {
    width: 20px;
    height: 20px;
  }

  &:hover {
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.04);
  }
}

.image-preview-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  touch-action: none;
}

.image-preview-img {
  max-width: min(100%, 1100px);
  max-height: calc(100vh - 220px);
  object-fit: contain;
  transform-origin: center center;
  user-select: none;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
  border-radius: 16px;
  pointer-events: none;
  will-change: transform;
}

.image-preview-toolbar {
  position: absolute;
  left: 50%;
  bottom: 28px;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 10px 14px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.62);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.26);
}

.image-preview-control {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  transition:
    background 0.2s ease,
    opacity 0.2s ease,
    transform 0.2s ease;

  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.22);
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
}

.image-preview-ratio {
  min-width: 72px;
  text-align: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.article-license-card {
  position: relative;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: var(--spacing-lg);
  padding: 28px 32px;
  margin-top: var(--spacing-2xl);
  border: 1.5px solid #d1d5db;
  border-radius: 28px;
  background: var(--color-bg-secondary);
  box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
  overflow: hidden;
}

[data-theme="dark"] .article-license-card {
  border-color: rgba(255, 255, 255, 0.1);
  background-color: var(--color-bg-secondary);
}

.license-main {
  position: relative;
  z-index: 1;
  flex: 1;
  min-width: 0;
}

.license-category {
  display: inline-flex;
  margin: 0 0 2px;
}

.license-title {
  margin: 0;
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 700;
  line-height: 1.3;
  color: var(--color-text-primary);
}

.license-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  margin-top: 18px;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;

  span,
  a {
    position: relative;
  }

  span:not(:first-child)::before,
  a::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 4px;
    margin-right: 16px;
    vertical-align: middle;
    border-radius: 50%;
    background: color-mix(in srgb, var(--color-accent) 55%, var(--color-text-tertiary));
  }
}

.license-link {
  color: var(--color-accent);
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.license-summary {
  margin: 20px 0 0;
  color: var(--color-text-primary);
  font-size: 17px !important;
  font-weight: 400;
  line-height: 1.35 !important;
}

.license-mark {
  position: absolute;
  right: 6px;
  bottom: -22px;
  z-index: 0;
  font-size: clamp(132px, 20vw, 220px);
  line-height: 1;
  font-weight: 700;
  color: color-mix(in srgb, var(--color-accent) 14%, transparent);
  font-family: Georgia, 'Times New Roman', serif;
  user-select: none;
  pointer-events: none;
}

.article-tip-action {
  position: relative;
  display: flex;
  width: fit-content;
  margin-top: 18px;
  margin-left: auto;
  margin-right: auto;
}

.tip-button {
  position: relative;
  min-width: 104px;
  padding: 10px 24px;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 600;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
  overflow: hidden;
  transition:
    transform 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: color-mix(in srgb, var(--color-accent) 78%, white);
    transform: translateY(102%);
    transition: transform 0.22s ease;
    z-index: 0;
  }

  span {
    position: relative;
    z-index: 1;
  }

  &:hover,
  .article-tip-action:focus-within & {
    transform: translateY(-1px);
    border-color: var(--color-accent);
    color: #fff;
    box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
  }

  &:hover::before,
  .article-tip-action:focus-within &::before {
    transform: translateY(0);
  }
}

.tip-popover {
  position: absolute;
  left: 50%;
  bottom: calc(100% + 14px);
  z-index: 4;
  width: 204px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: var(--color-bg-secondary);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.14);
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, 8px);
  transition:
    opacity 0.2s ease,
    transform 0.2s ease,
    visibility 0.2s ease;
  pointer-events: none;
}

.article-tip-action:hover .tip-popover,
.article-tip-action.active .tip-popover,
.article-tip-action:focus-within .tip-popover {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, 0);
}

@media (hover: hover) and (pointer: fine) {
  .article-tip-action:focus-within .tip-popover,
  .article-tip-action.active .tip-popover {
    opacity: 0;
    visibility: hidden;
    transform: translate(-50%, 8px);
  }
}

.tip-qr-image {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 12px;
  background: #f3f4f6;
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

  .image-preview-overlay {
    padding: 24px 12px 96px;
  }

  .image-preview-close {
    top: 16px;
    right: 16px;
    width: 42px;
    height: 42px;
  }

  .image-preview-img {
    max-width: 100%;
    max-height: calc(100vh - 180px);
    border-radius: 12px;
  }

  .image-preview-toolbar {
    gap: 12px;
    bottom: 20px;
    padding: 8px 12px;
  }

  .image-preview-control {
    width: 36px;
    height: 36px;
    font-size: 22px;
  }

  .article-license-card {
    padding: 22px 20px 28px;
    border-radius: 22px;
  }

  .license-meta {
    gap: 8px 0;

    span,
    a {
      width: 100%;
    }

    span::before,
    a::before {
      display: none !important;
    }
  }

  .license-summary {
    padding-right: 72px;
  }

  .license-mark {
    right: -2px;
    bottom: -8px;
    font-size: 112px;
  }

  .tip-popover {
    width: 184px;
    padding: 10px;
    border-radius: 18px;
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

#twikoo-container {
  min-height: 200px;
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
