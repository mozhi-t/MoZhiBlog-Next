const FALLBACK_SITE_URL = 'https://blog.mozhi.top'
const FALLBACK_API_BASE_URL = '/api'
const SITE_CONFIG_GLOBAL_KEY = '__MOZHI_SITE_CONFIG__'

const trimTrailingSlash = (value = '') => String(value || '').replace(/\/$/, '')
const isPlainObject = (value) => Object.prototype.toString.call(value) === '[object Object]'

const defaultSiteUrl = trimTrailingSlash(
  typeof import.meta !== 'undefined' && import.meta.env?.VITE_SITE_URL
    ? import.meta.env.VITE_SITE_URL
    : FALLBACK_SITE_URL
)

const defaultApiBaseUrl = trimTrailingSlash(
  typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL
    ? import.meta.env.VITE_API_BASE_URL
    : FALLBACK_API_BASE_URL
)

const DEFAULT_SITE_CONFIG = {
  name: '',
  title: '',
  shortName: '',
  url: defaultSiteUrl,
  description: '',
  locale: 'zh_CN',
  api: {
    baseUrl: defaultApiBaseUrl
  },
  author: {
    name: '',
    avatar: '/favicon.ico',
    bio: '',
    intro: '',
    aboutBio: '',
    email: '',
    socialLinks: {
      github: '',
      twitter: '',
      email: ''
    }
  },
  seo: {
    defaultImage: `${defaultSiteUrl}/favicon.ico`,
    keywords: []
  },
  twikoo: {
    envId: typeof import.meta !== 'undefined' && import.meta.env?.VITE_TWIKOO_ENV_ID
      ? import.meta.env.VITE_TWIKOO_ENV_ID
      : '',
    el: '#tcomment',
    lang: 'zh-CN',
    path: ''
  },
  article: {
    tipQrCode: ''
  },
  friendLink: {
    intro: '',
    siteName: '',
    siteUrl: defaultSiteUrl,
    avatar: '',
    description: ''
  },
  footer: {
    startDate: '',
    copyright: '',
    links: []
  },
  analytics: {
    sdkSnippets: []
  }
}

const deepMerge = (base, override) => {
  if (Array.isArray(base) || Array.isArray(override)) {
    return Array.isArray(override) ? [...override] : Array.isArray(base) ? [...base] : override
  }

  if (!isPlainObject(base) || !isPlainObject(override)) {
    return override === undefined ? base : override
  }

  const merged = { ...base }
  for (const key of Object.keys(override)) {
    merged[key] = deepMerge(base[key], override[key])
  }
  return merged
}

const runtimeConfig = typeof window !== 'undefined' ? window[SITE_CONFIG_GLOBAL_KEY] : null
const mergedConfig = deepMerge(DEFAULT_SITE_CONFIG, runtimeConfig || {})

mergedConfig.url = trimTrailingSlash(mergedConfig.url || DEFAULT_SITE_CONFIG.url)
mergedConfig.api = {
  ...DEFAULT_SITE_CONFIG.api,
  ...mergedConfig.api,
  baseUrl: trimTrailingSlash(mergedConfig.api?.baseUrl || DEFAULT_SITE_CONFIG.api.baseUrl)
}
mergedConfig.author = {
  ...DEFAULT_SITE_CONFIG.author,
  ...mergedConfig.author,
  socialLinks: {
    ...DEFAULT_SITE_CONFIG.author.socialLinks,
    ...mergedConfig.author?.socialLinks
  }
}
mergedConfig.seo = {
  ...DEFAULT_SITE_CONFIG.seo,
  ...mergedConfig.seo,
  defaultImage: mergedConfig.seo?.defaultImage || `${mergedConfig.url}/favicon.ico`,
  keywords: Array.isArray(mergedConfig.seo?.keywords) ? mergedConfig.seo.keywords : []
}
mergedConfig.twikoo = {
  ...DEFAULT_SITE_CONFIG.twikoo,
  ...mergedConfig.twikoo
}
mergedConfig.article = {
  ...DEFAULT_SITE_CONFIG.article,
  ...mergedConfig.article
}
mergedConfig.friendLink = {
  ...DEFAULT_SITE_CONFIG.friendLink,
  ...mergedConfig.friendLink,
  siteUrl: trimTrailingSlash(mergedConfig.friendLink?.siteUrl || mergedConfig.url)
}
mergedConfig.footer = {
  ...DEFAULT_SITE_CONFIG.footer,
  ...mergedConfig.footer,
  links: Array.isArray(mergedConfig.footer?.links) ? mergedConfig.footer.links : []
}
mergedConfig.analytics = {
  ...DEFAULT_SITE_CONFIG.analytics,
  ...mergedConfig.analytics,
  sdkSnippets: Array.isArray(mergedConfig.analytics?.sdkSnippets)
    ? mergedConfig.analytics.sdkSnippets.filter(item => typeof item === 'string' && item.trim())
    : []
}

export const SITE_CONFIG = mergedConfig

export const injectAnalyticsSdkScripts = () => {
  if (typeof document === 'undefined') return

  SITE_CONFIG.analytics.sdkSnippets.forEach((snippet, index) => {
    const marker = `site-analytics-sdk-${index}`
    if (document.head.querySelector(`[data-site-sdk="${marker}"]`)) {
      return
    }

    const normalizedSnippet = snippet.trim()
    if (!normalizedSnippet) {
      return
    }

    if (!/<script[\s>]/i.test(normalizedSnippet)) {
      const script = document.createElement('script')
      script.dataset.siteSdk = marker
      script.text = normalizedSnippet
      document.head.appendChild(script)
      return
    }

    const template = document.createElement('template')
    template.innerHTML = normalizedSnippet

    Array.from(template.content.childNodes).forEach((node, nodeIndex) => {
      if (node.nodeType === Node.TEXT_NODE && !node.textContent?.trim()) {
        return
      }

      if (node.nodeType === Node.ELEMENT_NODE && node.tagName.toLowerCase() === 'script') {
        const script = document.createElement('script')
        Array.from(node.attributes).forEach((attr) => {
          script.setAttribute(attr.name, attr.value)
        })
        script.dataset.siteSdk = `${marker}-${nodeIndex}`
        script.text = node.textContent || ''
        document.head.appendChild(script)
        return
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const clonedNode = node.cloneNode(true)
        clonedNode.dataset.siteSdk = `${marker}-${nodeIndex}`
        document.head.appendChild(clonedNode)
      }
    })
  })
}

export const SITE_NAME = SITE_CONFIG.name
export const SITE_TITLE = SITE_CONFIG.title
export const SITE_URL = SITE_CONFIG.url
export const SITE_DESCRIPTION = SITE_CONFIG.description
export const SITE_AUTHOR = SITE_CONFIG.author.name
export const SITE_LOCALE = SITE_CONFIG.locale
export const SITE_DEFAULT_IMAGE = SITE_CONFIG.seo.defaultImage
export const SITE_KEYWORDS = SITE_CONFIG.seo.keywords
export const SITE_API_BASE_URL = SITE_CONFIG.api.baseUrl
