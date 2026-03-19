<template>
  <div class="about-page">
    <header class="page-header">
      <h1 class="page-title">关于</h1>
    </header>

    <div
      class="profile-card"
      ref="targetRef"
      :class="{ visible: isVisible }"
    >
      <div class="avatar">
        <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200" :alt="SITE_CONFIG.author.name" />
      </div>
      <div class="profile-info">
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
      </div>
    </div>

    <div class="about-content">
      <section
        v-for="(section, index) in sections"
        :key="index"
        class="content-section"
      >
        <h2 class="section-title">{{ section.title }}</h2>
        <p class="section-text">{{ section.content }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { SITE_CONFIG } from '../config/site'
import { useIntersectionObserver } from '../composables/useObserver'
import { updateSeo } from '../utils/seo'

const { targetRef, isVisible } = useIntersectionObserver({ threshold: 0.2 })

updateSeo({
  title: '关于',
  description: `了解 ${SITE_CONFIG.author.name} 的个人背景、博客定位、技术栈与联系方式。`,
  path: '/about',
  keywords: ['关于', '作者介绍', '博客简介']
})

const sections = ref([
  {
    title: '关于这个博客',
    content: '这是一个专注于前端技术、编程实践与设计审美的个人博客，用来记录学习、沉淀经验，也整理一些值得反复回看的内容。'
  },
  {
    title: '技术栈',
    content: '目前主要围绕 Vue 3、JavaScript、TypeScript 与前端工程化展开，也会持续关注性能优化、交互设计和内容体验。'
  },
  {
    title: '联系我',
    content: `如果你想交流技术、讨论设计，或者交换友链，都可以通过邮件 ${SITE_CONFIG.author.email} 联系我。`
  }
])
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
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.profile-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--spacing-2xl);
  opacity: 0;
  transform: translateY(20px);
  transition: all var(--transition-smooth);

  &.visible {
    opacity: 1;
    transform: translateY(0);
  }

  &:hover {
    transform: rotateX(2deg) translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
}

[data-theme="dark"] .profile-card {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

.avatar {
  flex-shrink: 0;

  img {
    width: 120px;
    height: 120px;
    border-radius: var(--radius-full);
    object-fit: cover;
    box-shadow: var(--shadow-md);
  }
}

.profile-info {
  flex: 1;
}

.name {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.bio {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
}

.social-links {
  display: flex;
  gap: var(--spacing-md);

  @media (max-width: 768px) {
    justify-content: center;
  }
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: var(--color-text-secondary);
  border-radius: var(--radius-full);
  background: var(--color-bg-tertiary);
  transition: all var(--transition-base);

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    color: var(--color-accent);
    background: var(--color-accent-light);
    transform: translateY(-2px);
  }
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.content-section {
  position: relative;
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  opacity: 0;
  transform: translateY(10px);
  animation: sectionFadeIn 0.4s ease forwards;

  &:nth-child(1) { animation-delay: 0.1s; }
  &:nth-child(2) { animation-delay: 0.2s; }
  &:nth-child(3) { animation-delay: 0.3s; }
}

[data-theme="dark"] .content-section {
  border-color: rgba(255, 255, 255, 0.08);
  background-color: var(--color-bg-secondary);
}

@keyframes sectionFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  position: relative;
  padding-left: var(--spacing-md);

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 70%;
    background: var(--color-accent);
    border-radius: 2px;
  }
}

.section-text {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--color-text-secondary);
  padding-left: var(--spacing-md);
}
</style>
