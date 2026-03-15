import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'

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

export const renderMarkdown = (content = '') => {
  if (!content) return ''
  return markdownRenderer.parse(content)
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
