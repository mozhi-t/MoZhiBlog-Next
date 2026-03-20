import {
  SITE_AUTHOR,
  SITE_DEFAULT_IMAGE,
  SITE_DESCRIPTION,
  SITE_KEYWORDS,
  SITE_LOCALE,
  SITE_NAME,
  SITE_TITLE,
  SITE_URL
} from '../config/site'

const EXTRA_META_SELECTOR = 'meta[data-seo-extra="true"]'
const SCHEMA_ID = 'seo-json-ld'

const upsertMeta = (selector, attributes) => {
  let element = document.head.querySelector(selector)
  if (!element) {
    element = document.createElement('meta')
    document.head.appendChild(element)
  }

  Object.entries(attributes).forEach(([key, value]) => {
    if (value === null || value === undefined || value === '') {
      element.removeAttribute(key)
    } else {
      element.setAttribute(key, value)
    }
  })
}

const upsertLink = (selector, attributes) => {
  let element = document.head.querySelector(selector)
  if (!element) {
    element = document.createElement('link')
    document.head.appendChild(element)
  }

  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, value)
  })
}

const removeManagedExtras = () => {
  document.head.querySelectorAll(EXTRA_META_SELECTOR).forEach((element) => element.remove())
}

const addExtraMeta = (attributes) => {
  const element = document.createElement('meta')
  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, value)
  })
  element.setAttribute('data-seo-extra', 'true')
  document.head.appendChild(element)
}

const setSchema = (schema) => {
  let element = document.head.querySelector(`#${SCHEMA_ID}`)

  if (!schema) {
    element?.remove()
    return
  }

  if (!element) {
    element = document.createElement('script')
    element.type = 'application/ld+json'
    element.id = SCHEMA_ID
    document.head.appendChild(element)
  }

  element.textContent = JSON.stringify(schema)
}

export const stripHtml = (value = '') =>
  value
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`[^`]*`/g, ' ')
    .replace(/!\[[^\]]*]\([^)]*\)/g, ' ')
    .replace(/\[[^\]]*]\([^)]*\)/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/[#>*_~\-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

export const truncate = (value = '', maxLength = 160) => {
  if (!value || value.length <= maxLength) {
    return value
  }
  return `${value.slice(0, Math.max(0, maxLength - 1)).trim()}…`
}

export const buildCanonicalUrl = (path = '/') => {
  if (/^https?:\/\//.test(path)) {
    return path
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return new URL(normalizedPath, `${SITE_URL}/`).toString()
}

export const updateSeo = ({
  title,
  description = SITE_DESCRIPTION,
  path = '/',
  image = SITE_DEFAULT_IMAGE,
  type = 'website',
  keywords = [],
  noindex = false,
  publishedTime,
  modifiedTime,
  section,
  tags = [],
  author = SITE_AUTHOR,
  schema
} = {}) => {
  const fullTitle = title ? `${title} | ${SITE_NAME}` : SITE_TITLE
  const canonicalUrl = buildCanonicalUrl(path)
  const normalizedDescription = truncate(description || SITE_DESCRIPTION, 160)
  const normalizedKeywords = [...new Set([...SITE_KEYWORDS, ...keywords].filter(Boolean))].join(', ')
  const robots = noindex ? 'noindex, nofollow' : 'index, follow, max-image-preview:large'

  document.documentElement.lang = 'zh-CN'
  document.title = fullTitle

  upsertMeta('meta[name="description"]', { name: 'description', content: normalizedDescription })
  upsertMeta('meta[name="keywords"]', { name: 'keywords', content: normalizedKeywords })
  upsertMeta('meta[name="robots"]', { name: 'robots', content: robots })
  upsertMeta('meta[name="author"]', { name: 'author', content: author })

  upsertMeta('meta[property="og:title"]', { property: 'og:title', content: fullTitle })
  upsertMeta('meta[property="og:description"]', { property: 'og:description', content: normalizedDescription })
  upsertMeta('meta[property="og:type"]', { property: 'og:type', content: type })
  upsertMeta('meta[property="og:url"]', { property: 'og:url', content: canonicalUrl })
  upsertMeta('meta[property="og:site_name"]', { property: 'og:site_name', content: SITE_NAME })
  upsertMeta('meta[property="og:locale"]', { property: 'og:locale', content: SITE_LOCALE })
  upsertMeta('meta[property="og:image"]', { property: 'og:image', content: image })

  upsertMeta('meta[name="twitter:card"]', { name: 'twitter:card', content: 'summary_large_image' })
  upsertMeta('meta[name="twitter:title"]', { name: 'twitter:title', content: fullTitle })
  upsertMeta('meta[name="twitter:description"]', { name: 'twitter:description', content: normalizedDescription })
  upsertMeta('meta[name="twitter:image"]', { name: 'twitter:image', content: image })

  upsertLink('link[rel="canonical"]', { rel: 'canonical', href: canonicalUrl })
  upsertLink('link[rel="alternate"][type="application/rss+xml"]', {
    rel: 'alternate',
    type: 'application/rss+xml',
    title: `${SITE_NAME} RSS`,
    href: buildCanonicalUrl('/rss.xml')
  })

  removeManagedExtras()

  if (type === 'article') {
    if (publishedTime) {
      addExtraMeta({ property: 'article:published_time', content: publishedTime })
    }
    if (modifiedTime) {
      addExtraMeta({ property: 'article:modified_time', content: modifiedTime })
    }
    if (section) {
      addExtraMeta({ property: 'article:section', content: section })
    }
    tags.forEach((tag) => addExtraMeta({ property: 'article:tag', content: tag }))
  }

  setSchema(schema)
}
