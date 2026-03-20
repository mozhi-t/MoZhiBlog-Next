<template>
  <div class="about-page">
    <header class="page-header">
      <h1 class="page-title">关于</h1>
      <p class="page-description" :class="{ visible: isVisible }">半生寥寥，尽在此间</p>
    </header>

    <section
      ref="targetRef"
      class="profile-block"
      :class="{ visible: isVisible }"
    >
      <div class="avatar">
        <img :src="authorAvatar" :alt="SITE_CONFIG.author.name" />
      </div>
      <h2 class="name">{{ SITE_CONFIG.author.name }}</h2>
      <p class="bio">{{ SITE_CONFIG.author.aboutBio }}</p>
      <div class="social-links">
        <a :href="SITE_CONFIG.author.socialLinks.github" target="_blank" rel="noopener" class="social-link">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
          </svg>
        </a>
        <a :href="SITE_CONFIG.author.socialLinks.twitter" target="_blank" rel="noopener" class="social-link">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
          </svg>
        </a>
        <a :href="SITE_CONFIG.author.socialLinks.email" class="social-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <polyline points="22,6 12,13 2,6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </a>
      </div>
    </section>

    <div class="about-content">
      <div
        v-for="(section, index) in sections"
        :key="section.title"
        class="content-section"
        :class="{ visible: isVisible }"
        :style="{ '--section-delay': `${0.12 + index * 0.12}s` }"
      >
        <h2 class="section-title">{{ section.title }}</h2>
        <div class="section-body markdown-content" v-html="section.html"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import authorAvatar from '@/assets/tx.jpg'
import { SITE_CONFIG } from '../config/site'
import { useIntersectionObserver } from '../composables/useObserver'
import { renderMarkdown } from '../utils/markdown'
import { updateSeo } from '../utils/seo'

const { targetRef, isVisible } = useIntersectionObserver({ threshold: 0.2 })

updateSeo({
  title: '关于',
  description: `了解 ${SITE_CONFIG.author.name} 的个人背景、博客定位、技术栈与联系方式。`,
  path: '/about',
  keywords: ['关于', '作者介绍', '博客简介']
})

const aboutContent = `# 关于我

- 昵称：MoZhi（沫栀.）
- 性别：Man
- 身份：09高中生
- 邮箱：2195829535@qq.com | mozhi.it@hotmail.com （常用QQ邮箱，微软不经常看）
- 昵称由来：初中取的，当时觉得比较蕴含文艺气息，就一直沿用到现在了
- 对全栈开发，游戏开发（UE4），虚拟制片，摄影，无人机，DIY，物联网等等领域都有涉及
- 本人文笔不好，文章有时会很凌乱，还会说一些废话
- 不喜欢'应试教育'，学的东西都是为了‘学习’而学习，而且每天感觉在学校里很无聊，有这时间我还不如自学呢
- 自认为涉及的领域~~非常广~~

# 关于本站

本博客搭建与24年10月8号，其实之前在初中的时候就想建一个网站了，可惜当时没有太多能力和时间，导致一直在搁置，现在也算是圆了小时候一个梦想。博客之前一直使用的是WordPress，但因为访问比较卡等一些原因，使我在25年年尾时开始自学vue等一些框架并开发属于自己的博客系统（当然也有AI的帮助），现在的博客的设计风格我很满意，启动速度也不错，但是可能还是有一些安全性的问题我没有检查出来（其实写的是一坨屎罢了），这是开源链接：[mozhiblog-next](https://github.com/mozhi-it/mozhiblog-next)

本站域名其实一开始想用mozhi这个前缀的，但是被注册了，然后其他后缀的域名续费又太贵了，于是我就在mozhi后面加了个x，~~感觉增加了一点高级感~~（bushi）

# 技术栈

- 前端
  - Vue 3
  - Vite
  - Pinia
  - Vue Router
  - Axios
  - Marked
  - Highlight.js
  - Sass
  - Twikoo
- 后端
  - Python
  - FastAPI
  - MySQL
  - Pyjwt
  - SQLAlchemy
  - Pydantic
  - Python-Dotenv
  - Passlib / Bcrypt
  - Uvicorn

- 其他
  - 云服务：[林柚云](https://youvps.cn/)
  - 图床：[敖武的图床](https://playground.z.wiki/img-cloud/index.html)（准备换为自建）
  - 对象存储：[缤纷云](https://console.bitiful.com/)
  - SEO：[百度](http://ziyuan.baidu.com/)+[bing](https://www.bing.com/webmasters/about?setlang=zh-cn)
  - 流量监控：[51la](https://v6.51.la/)+[umami](https://github.com/umami-software/umami)+[Uptime Kuma](https://github.com/louislam/uptime-kuma)
  - 版权协议：使用[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)`

const parseSections = (content) => {
  const normalized = content.replace(/\r\n/g, '\n').trim()
  const blocks = normalized.split(/\n(?=# )/).filter(Boolean)

  return blocks.map((block) => {
    const lines = block.split('\n')
    const title = lines[0].replace(/^#\s+/, '').trim()
    const body = lines.slice(1).join('\n').trim()

    return {
      title,
      html: renderMarkdown(body)
    }
  })
}

const sections = computed(() => parseSections(aboutContent))
</script>

<style lang="scss" scoped>
.about-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(var(--nav-height) + 40px) var(--spacing-lg) var(--spacing-3xl);
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.page-title {
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.page-description {
  font-size: var(--font-size-lg);
  color: var(--color-text-tertiary);
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 0.32s ease, transform 0.32s ease;
}

.page-description.visible {
  opacity: 1;
  transform: translateY(0);
}

.profile-block {
  width: min(100%, 620px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-inline: auto;
  margin-bottom: var(--spacing-3xl);
  text-align: center;
  opacity: 1;

  &.visible {
    opacity: 1;
  }
}

.avatar img {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.name {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.bio {
  max-width: 560px;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.social-links {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xs);
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  color: var(--color-text-secondary);
  background: transparent;
  transition: color var(--transition-base), transform var(--transition-base);

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    color: var(--color-accent);
    transform: translateY(-2px);
  }
}

.about-content {
  max-width: 760px;
  margin: 0 auto;
}

.content-section {
  --section-delay: 0.12s;
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  opacity: 0;
  transform: translateY(6px);
}

.section-body {
  color: var(--color-text-secondary);
  opacity: 0;
  transform: translateY(8px);
}

.content-section.visible .section-title {
  animation: sectionTitleIn 0.36s ease both;
  animation-delay: var(--section-delay);
}

.content-section.visible .section-body {
  animation: sectionBodyIn 0.42s ease both;
  animation-delay: calc(var(--section-delay) + 0.08s);
}

.section-body :deep(p),
.section-body :deep(li),
.section-body :deep(a) {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
}

.section-body :deep(p),
.section-body :deep(ul),
.section-body :deep(ol) {
  margin-top: 0;
}

.section-body :deep(li) {
  color: var(--color-text-primary);
}

@keyframes sectionTitleIn {
  0% {
    opacity: 0;
    transform: translateY(6px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes sectionBodyIn {
  0% {
    opacity: 0;
    transform: translateY(8px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .avatar img {
    width: 104px;
    height: 104px;
  }
}
</style>
