import hljs from 'highlight.js'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'

export const markdownRenderer = new Marked(
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

markdownRenderer.use({
  renderer: {
    heading({ tokens, depth }) {
      const text = this.parser.parseInline(tokens)
      const id = text
        .toLowerCase()
        .replace(/[^\u4e00-\u9fa5a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
      return `<h${depth} id="${id}">${text}</h${depth}>`
    }
  }
})

const articleReferenceCache = new Map()

const parseAttrs = (rawAttrs = '') => {
  const attrs = {}
  const attrRegex = /(\w+)="([^"]*)"/g
  let match = attrRegex.exec(rawAttrs)

  while (match) {
    attrs[match[1]] = match[2]
    match = attrRegex.exec(rawAttrs)
  }

  return attrs
}

const renderArticleReference = (attrs) => {
  const id = attrs.id?.trim()
  if (!id) return ''

  return `<a class="custom-article-ref" href="/article/${id}" data-article-ref-id="${id}">
<span class="custom-article-ref__label">未分类</span>
<span class="custom-article-ref__title">加载中...</span>
<span class="custom-article-ref__meta">文章 #${id}</span>
</a>`
}

const renderTimeline = (inner = '') => {
  const eventRegex = /\[timeline-event([^\]]*)\]([\s\S]*?)\[\/timeline-event\]/g
  const items = []
  let match = eventRegex.exec(inner)

  while (match) {
    const attrs = parseAttrs(match[1] || '')
    const body = preprocessCustomMarkdown((match[2] || '').trim())
    items.push(`<div class="custom-timeline__item">
<div class="custom-timeline__dot"></div>
<div class="custom-timeline__card">
<div class="custom-timeline__meta">
<span class="custom-timeline__date">${attrs.date || ''}</span>
<div class="custom-timeline__title">${attrs.title || ''}</div>
</div>
<div class="custom-timeline__body">${markdownRenderer.parse(body)}</div>
</div>
</div>`)
    match = eventRegex.exec(inner)
  }

  if (!items.length) return ''

  return `<section class="custom-timeline">
${items.join('\n')}
</section>`
}

const renderFoldedContent = (attrs, inner = '') => {
  const title = attrs.title?.trim() || '展开查看'
  const body = preprocessCustomMarkdown((inner || '').trim())

  return `<details class="custom-folded-content">
<summary class="custom-folded-content__summary">${title}</summary>
<div class="custom-folded-content__body">${markdownRenderer.parse(body)}</div>
</details>`
}

export const preprocessCustomMarkdown = (content = '') => {
  if (!content) return ''

  let processed = content

  processed = processed.replace(/\[timeline\]([\s\S]*?)\[\/timeline\]/g, (_, inner) => {
    return renderTimeline(inner)
  })

  processed = processed.replace(/\[folded_content([^\]]*)\]([\s\S]*?)\[\/folded(?:_|\s+)content\]/g, (_, rawAttrs, inner) => {
    return renderFoldedContent(parseAttrs(rawAttrs), inner)
  })

  processed = processed.replace(/\[article([^\]]*)\]/g, (_, rawAttrs) => {
    return renderArticleReference(parseAttrs(rawAttrs))
  })

  return processed
}

export const renderMarkdown = (content = '') => {
  if (!content) return ''
  return markdownRenderer.parse(preprocessCustomMarkdown(content))
}

export const enhanceCodeBlocks = (root) => {
  if (!root) return

  const codeBlocks = root.querySelectorAll('pre')
  codeBlocks.forEach((pre) => {
    if (pre.parentNode?.classList.contains('code-block-wrapper')) return

    const codeEl = pre.querySelector('code')
    if (!codeEl) return

    const code = codeEl.textContent || ''
    const langEl = codeEl.classList.value.match(/language-(\S+)/)
    const lang = langEl ? langEl[1] : 'text'

    const wrapper = document.createElement('div')
    wrapper.className = 'code-block-wrapper'

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

    pre.parentNode?.insertBefore(wrapper, pre)
    wrapper.appendChild(header)
    wrapper.appendChild(pre)
  })

  root.querySelectorAll('.copy-btn').forEach((btn) => {
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
      } catch (error) {
        console.error('复制失败:', error)
      }
    }
  })
}

export const hydrateArticleReferences = async (root, fetchArticleReference) => {
  if (!root || typeof fetchArticleReference !== 'function') return

  const refs = root.querySelectorAll('[data-article-ref-id]')
  await Promise.all(Array.from(refs).map(async (node) => {
    if (node.dataset.articleRefLoaded === 'true') return

    const articleId = node.dataset.articleRefId
    if (!articleId) return

    try {
      if (!articleReferenceCache.has(articleId)) {
        articleReferenceCache.set(
          articleId,
          Promise.resolve(fetchArticleReference(articleId)).catch((error) => {
            articleReferenceCache.delete(articleId)
            throw error
          })
        )
      }

      const article = await articleReferenceCache.get(articleId)
      const titleNode = node.querySelector('.custom-article-ref__title')
      const metaNode = node.querySelector('.custom-article-ref__meta')
      const badgeNode = node.querySelector('.custom-article-ref__label')

      if (titleNode) {
        titleNode.textContent = article.title || `文章 #${articleId}`
      }

      if (metaNode) {
        const metaParts = []
        if (article.category?.name) metaParts.push(article.category.name)
        if (article.need_password) metaParts.push('密码保护')
        if (article.summary) {
          metaParts.push(article.summary.length > 48 ? `${article.summary.slice(0, 48)}...` : article.summary)
        }
        metaNode.textContent = metaParts.join(' · ') || `文章 #${articleId}`
      }

      if (badgeNode && article.type === 1) {
        badgeNode.textContent = article.category?.name || '置顶文章'
      } else if (badgeNode) {
        badgeNode.textContent = article.category?.name || '未分类'
      }

      node.dataset.articleRefLoaded = 'true'
    } catch (error) {
      const titleNode = node.querySelector('.custom-article-ref__title')
      const metaNode = node.querySelector('.custom-article-ref__meta')
      if (titleNode) titleNode.textContent = `文章 #${articleId}`
      if (metaNode) metaNode.textContent = '引用信息加载失败'
      console.error('加载文章引用失败:', error)
    }
  }))
}
