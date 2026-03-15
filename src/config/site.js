const siteUrl = (import.meta.env.VITE_SITE_URL || 'https://blog.mozhi.top').replace(/\/$/, '')
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')

export const SITE_CONFIG = {
  name: 'MoZhi Blog',
  title: 'MoZhi 的个人博客',
  shortName: 'MoZhi',
  url: siteUrl,
  description: '专注于前端开发、编程实践、学习记录与生活思考的个人博客。',
  locale: 'zh_CN',
  api: {
    baseUrl: apiBaseUrl
  },
  author: {
    name: 'MoZhi',
    avatar: '/favicon.ico',
    bio: '远方很远，步履不停，未来可期',
    intro: 'Hi~欢迎光临 MoZhi 的个人博客，这里存放有技术分析、学习笔记、生活感悟等内容，还有一些好玩的效果，希望你可以在这里找到对你有用的知识和感悟。',
    aboutBio: '前端开发者 / 设计爱好者 / 终身学习者',
    email: 'mozhi.it@qq.com',
    socialLinks: {
      github: 'https://github.com/mozhi-it',
      twitter: 'https://twitter.com',
      email: 'mailto:mozhi.it@qq.com'
    }
  },
  seo: {
    defaultImage: `${siteUrl}/favicon.ico`,
    keywords: [
      'MoZhi Blog',
      'MoZhi',
      '个人博客',
      '前端开发',
      'Vue',
      'JavaScript',
      '编程',
      '技术博客'
    ]
  },
  twikoo: {
    envId: import.meta.env.VITE_TWIKOO_ENV_ID || 'https://twikoo-api.mozhix.top/',
    el: '#tcomment',
    lang: 'zh-CN',
    path: ''
  },
  friendLink: {
    intro: '如果你想交换友链，可以在下方评论发出你的友链信息或用邮箱联系我，我看到之后会第一时间添加。',
    siteName: 'MoZhi Blog',
    siteUrl,
    avatar: 'https://mozhi.s3.bitiful.net/cropped-tou.jpg',
    description: '远方很远，步履不停，未来可期'
  },
  footer: {
    startDate: '2024-10-08',
    copyright: 'All rights reserved.',
    links: [
      { label: 'GitHub', href: 'https://github.com/mozhi-it', external: true },
      { label: 'RSS', href: '/rss.xml', external: false },
      { label: '林槐夏', href: 'https://www.lyvps.net', external: true }
    ]
  }
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
