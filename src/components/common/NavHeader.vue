<template>
  <!-- FPS Display -->
  <div
    class="fps-display"
    :class="{ scrolled: isScrolled, hovered: isHovered }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    title="当前帧率"
  >
    <span class="fps-value">{{ fps }}</span>
    <span class="fps-text">当前FPS：</span>
  </div>

  <!-- Search Box -->
  <div
    class="search-box"
    :class="{ scrolled: isScrolled, 'search-hovered': searchHovered }"
    @mouseenter="searchHovered = true"
    @mouseleave="searchHovered = false"
    title="搜索文章"
  >
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <circle cx="11" cy="11" r="8" stroke-width="2"/>
      <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
    </svg>
    <input
      type="text"
      class="search-input"
      placeholder="搜索文章..."
      v-model="searchQuery"
      @keyup.enter="handleSearch"
    />
  </div>

  <header class="nav-header" :class="{ scrolled: isScrolled, 'menu-open': menuOpen }">
    <nav class="nav-container" :class="navPromptClasses">
      <div class="nav-prompt-overlay" aria-hidden="true">
        <div class="nav-radiance-core"></div>
      </div>

      <!-- Logo -->
      <router-link to="/" class="nav-logo" @click="closeMenu">
        <span class="logo-text">{{ SITE_CONFIG.shortName }}</span>
      </router-link>

      <!-- Desktop Navigation -->
      <ul class="nav-links desktop-nav">
        <li v-for="item in navItems" :key="item.path" class="nav-item">
          <router-link
            v-if="!item.children"
            :to="item.path"
            class="nav-link"
            :class="{ active: isActive(item.path) }"
          >
            {{ item.name }}
          </router-link>

          <!-- Dropdown Menu -->
          <div v-else class="nav-dropdown">
            <span class="nav-link dropdown-trigger" :title="item.tooltip">
              {{ item.name }}
              <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M6 9l6 6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <ul class="dropdown-menu">
              <li v-for="child in item.children" :key="child.path">
                <router-link :to="child.path" class="dropdown-link">
                  {{ child.name }}
                </router-link>
              </li>
            </ul>
          </div>
        </li>
      </ul>

      <!-- Right Actions -->
      <div class="nav-actions">
        <!-- Theme Toggle -->
        <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'">
          <svg v-if="theme === 'light'" class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="5" stroke-width="2"/>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <svg v-else class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <!-- Mobile Menu Button -->
        <button class="menu-toggle" @click="toggleMenu" :class="{ active: menuOpen }">
          <span class="menu-line"></span>
          <span class="menu-line"></span>
          <span class="menu-line"></span>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <Transition name="slide-down">
        <ul v-if="menuOpen" class="nav-links mobile-nav">
          <li v-for="item in navItems" :key="item.path" class="nav-item">
            <router-link
              v-if="!item.children"
              :to="item.path"
              class="nav-link"
              @click="closeMenu"
            >
              {{ item.name }}
            </router-link>
            <div v-else class="nav-dropdown-mobile">
              <span class="nav-link dropdown-trigger">{{ item.name }}</span>
              <ul class="dropdown-menu-mobile">
                <li v-for="child in item.children" :key="child.path">
                  <router-link :to="child.path" class="dropdown-link" @click="closeMenu">
                    {{ child.name }}
                  </router-link>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </Transition>
      <div
        class="nav-prompt-overlay"
        :class="{ visible: isPromptTextVisible }"
      >
        <div
        class="nav-prompt"
        :class="[
          promptType ? `is-${promptType}` : '',
          { visible: isPromptTextVisible }
        ]"
        aria-live="polite"
      >
        {{ promptMessage }}
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '../../stores/theme'
import { SITE_CONFIG } from '../../config/site'

const route = useRoute()
const themeStore = useThemeStore()

// FPS Calculation
const fps = ref(60)
let frameCount = 0
let lastTime = performance.now()
let animationFrameId = null

const calculateFPS = () => {
  frameCount++
  const currentTime = performance.now()
  const elapsed = currentTime - lastTime

  if (elapsed >= 1000) {
    fps.value = Math.round((frameCount * 1000) / elapsed)
    frameCount = 0
    lastTime = currentTime
  }

  animationFrameId = requestAnimationFrame(calculateFPS)
}

const theme = computed(() => themeStore.theme)
const toggleTheme = () => themeStore.toggleTheme()

// Navigation Items
const navItems = [
  { name: '首页', path: '/' },
  {
    name: '文章',
    path: '/article',
    tooltip: '分类、标签、归档',
    children: [
      { name: '分类', path: '/category' },
      { name: '标签', path: '/tag' }
    ]
  },
  { name: '空间', path: '/space' },
  { name: '归档', path: '/archive' },
  { name: '友链', path: '/links' },
  { name: '留言', path: '/message' },
  { name: '关于', path: '/about' }
]

// Menu state
const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
const closeMenu = () => {
  menuOpen.value = false
}

// Scroll state
const isScrolled = ref(false)
const isHovered = ref(false)
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Search functionality
const searchHovered = ref(false)
const searchQuery = ref('')
const router = useRouter()

const NAV_PROMPT_TYPES = {
  copy: 'copy',
  devtools: 'devtools'
}

const promptType = ref('')
const isPromptBlurred = ref(false)
const isPromptTextVisible = ref(false)
const isPromptGradientVisible = ref(false)
const isPromptGradientReversing = ref(false)
const devtoolsOpened = ref(false)

const promptTimers = new Set()
let promptFrameId = null
let devtoolsCheckTimer = null

const BLUR_ENTER_DURATION = 300
const GRADIENT_ENTER_DURATION = 400
const HOLD_DURATION = 2000
const EXIT_DURATION = 650
const EXIT_STAGGER_DURATION = 200
const DEVTOOLS_THRESHOLD = 160

const promptMessage = computed(() => {
  if (promptType.value === NAV_PROMPT_TYPES.copy) {
    return '复制成功'
  }

  if (promptType.value === NAV_PROMPT_TYPES.devtools) {
    return '您已打开开发者工具，请注意遵守开源协议'
  }

  return ''
})

const navPromptClasses = computed(() => ({
  'is-prompt-active': Boolean(promptType.value),
  'is-prompt-blurred': isPromptBlurred.value,
  'is-prompt-gradient-visible': isPromptGradientVisible.value,
  'is-prompt-gradient-reversing': isPromptGradientReversing.value,
  'is-copy-prompt': promptType.value === NAV_PROMPT_TYPES.copy,
  'is-devtools-prompt': promptType.value === NAV_PROMPT_TYPES.devtools
}))

const registerTimer = (callback, delay) => {
  const timer = window.setTimeout(() => {
    promptTimers.delete(timer)
    callback()
  }, delay)

  promptTimers.add(timer)
}

const clearPromptTimers = () => {
  promptTimers.forEach((timer) => window.clearTimeout(timer))
  promptTimers.clear()
}

const resetPromptState = () => {
  if (promptFrameId) {
    cancelAnimationFrame(promptFrameId)
    promptFrameId = null
  }

  clearPromptTimers()
  isPromptBlurred.value = false
  isPromptTextVisible.value = false
  isPromptGradientVisible.value = false
  isPromptGradientReversing.value = false
  promptType.value = ''
}

const startPromptExit = () => {
  isPromptGradientVisible.value = false
  isPromptGradientReversing.value = true

  registerTimer(() => {
    isPromptTextVisible.value = false
    isPromptBlurred.value = false
  }, EXIT_STAGGER_DURATION)

  registerTimer(() => {
    isPromptGradientReversing.value = false
    promptType.value = ''
  }, EXIT_DURATION + EXIT_STAGGER_DURATION)
}

const triggerNavPrompt = (type) => {
  resetPromptState()
  promptType.value = type

  promptFrameId = requestAnimationFrame(() => {
    promptFrameId = null
    isPromptBlurred.value = true

    registerTimer(() => {
      isPromptTextVisible.value = true
      isPromptGradientVisible.value = true
    }, BLUR_ENTER_DURATION)

    registerTimer(() => {
      startPromptExit()
    }, BLUR_ENTER_DURATION + GRADIENT_ENTER_DURATION + HOLD_DURATION)
  })
}

const handleCopy = () => {
  const selectedText = window.getSelection?.()?.toString().trim()

  if (!selectedText) {
    return
  }

  triggerNavPrompt(NAV_PROMPT_TYPES.copy)
}

const detectDevtoolsOpen = () => {
  const widthGap = window.outerWidth - window.innerWidth
  const heightGap = window.outerHeight - window.innerHeight
  const opened = widthGap > DEVTOOLS_THRESHOLD || heightGap > DEVTOOLS_THRESHOLD

  if (opened && !devtoolsOpened.value) {
    triggerNavPrompt(NAV_PROMPT_TYPES.devtools)
  }

  devtoolsOpened.value = opened
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } })
  }
}

// Active route check
const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('copy', handleCopy)
  handleScroll()
  calculateFPS()
  detectDevtoolsOpen()
  devtoolsCheckTimer = window.setInterval(detectDevtoolsOpen, 1000)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('copy', handleCopy)
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
  if (devtoolsCheckTimer) {
    clearInterval(devtoolsCheckTimer)
  }
  resetPromptState()
})
</script>

<style lang="scss" scoped>
/* ============================================
   Navigation Header - 玻璃椭圆导航栏
   ============================================ */
.nav-header {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: var(--nav-width);
  max-width: 1200px;
  height: var(--nav-height);
  z-index: 1000;
  transition: all var(--transition-smooth);

  &.scrolled {
    top: 10px;
    height: var(--nav-height-scrolled);
  }
}

.nav-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 var(--spacing-lg);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-nav);
  box-shadow: var(--shadow-nav);
  overflow: visible;
  isolation: isolate;
  transition:
    background 0.4s ease-in-out,
    border-color 0.4s ease-in-out,
    box-shadow 0.4s ease-in-out,
    backdrop-filter 0.3s ease-in-out,
    -webkit-backdrop-filter 0.3s ease-in-out;

  > * {
    position: relative;
    z-index: 1;
    transition:
      filter 0.3s ease-in-out,
      opacity 0.3s ease-in-out,
      transform 0.3s ease-in-out;
  }

  .nav-prompt-overlay {
    position: absolute;
    inset: 0;
    z-index: 3;
    overflow: hidden;
    border-radius: inherit;
    pointer-events: none;
  }

  .nav-radiance-core {
    position: absolute;
    left: 50%;
    bottom: -18%;
    z-index: 2;
    width: 34%;
    height: 68%;
    border-radius: 999px;
    opacity: 0;
    transform: translateX(-50%) scale(0.12, 0.08);
    transform-origin: 50% 100%;
    transition:
      transform 0.24s cubic-bezier(0.18, 0.88, 0.28, 1),
      opacity 0.18s ease-out,
      filter 0.24s ease-out;
    filter: blur(14px) saturate(1.08) brightness(1.02);
    pointer-events: none;
  }

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 2;
    border-radius: inherit;
    opacity: 0;
    clip-path: circle(0% at 50% 100%);
    transition:
      clip-path 0.4s cubic-bezier(0.22, 0.84, 0.24, 1),
      opacity 0.4s ease-in-out,
      filter 0.4s ease-in-out;
    transition-delay: 0.18s;
    filter: saturate(1.05);
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 2;
    border-radius: inherit;
    background:
      linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.42) 0%,
        rgba(255, 255, 255, 0.3) 100%
      );
    backdrop-filter: blur(18px) saturate(145%);
    -webkit-backdrop-filter: blur(18px) saturate(145%);
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    pointer-events: none;
  }

  &.is-prompt-blurred {
    > :not(.nav-prompt-overlay) {
      filter: blur(6px);
      contain: paint;
      opacity: 0.34;
      transform: scale(0.985);
    }

    &::after {
      opacity: 0.95;
    }
  }

  &.is-prompt-gradient-visible::before {
    opacity: 1;
    clip-path: circle(150% at 50% 100%);
    filter: saturate(1.2);
  }

  &.is-prompt-gradient-visible.is-copy-prompt {
    background: rgba(214, 252, 227, 0.46);
    box-shadow:
      0 10px 22px rgba(22, 163, 74, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.24);
  }

  &.is-prompt-gradient-visible.is-devtools-prompt {
    background: rgba(254, 226, 226, 0.46);
    box-shadow:
      0 10px 22px rgba(220, 38, 38, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.24);
  }

  &.is-prompt-gradient-visible .nav-radiance-core {
    opacity: 1;
    transform: translateX(-50%) scale(1.9, 1.28);
    filter: blur(18px) saturate(1.18) brightness(1.12);
  }

  &.is-prompt-gradient-reversing::before {
    opacity: 0;
    clip-path: circle(0% at 50% 100%);
    transition-duration: 0.65s;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-delay: 0s;
  }

  &.is-prompt-gradient-reversing .nav-radiance-core {
    opacity: 0;
    transform: translateX(-50%) scale(0.12, 0.08);
    transition-duration: 0.65s;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  }

  &.is-copy-prompt::before {
    background: rgba(34, 197, 94, 0.9);
  }

  &.is-copy-prompt .nav-radiance-core {
    background:
      radial-gradient(
        ellipse at 50% 100%,
        rgba(220, 252, 231, 0.98) 0%,
        rgba(134, 239, 172, 0.92) 28%,
        rgba(74, 222, 128, 0.64) 52%,
        rgba(34, 197, 94, 0) 78%
      );
  }

  &.is-devtools-prompt::before {
    background: rgba(239, 68, 68, 0.9);
  }

  &.is-devtools-prompt .nav-radiance-core {
    background:
      radial-gradient(
        ellipse at 50% 100%,
        rgba(254, 226, 226, 0.98) 0%,
        rgba(252, 165, 165, 0.92) 28%,
        rgba(248, 113, 113, 0.64) 52%,
        rgba(239, 68, 68, 0) 78%
      );
  }
}

.nav-prompt {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  min-width: 260px;
  max-width: calc(100% - 48px);
  padding: 0 24px;
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.02em;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0;
  pointer-events: none;
  text-shadow: 0 1px 12px rgba(255, 255, 255, 0.28);
  transform: translate(-50%, 120%);
  transition:
    transform 0.3s ease-in-out,
    opacity 0.3s ease-in-out,
    color 0.4s ease-in-out;

  &.visible {
    opacity: 1;
    transform: translate(-50%, -50%);
  }

  &.is-copy {
    color: #166534;
  }

  &.is-devtools {
    color: #b91c1c;
  }
}

/* FPS Display */
.fps-display {
  position: fixed;
  left: 20px;
  top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--nav-height);
  height: var(--nav-height);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: 50%;
  box-shadow: var(--shadow-nav);
  flex-shrink: 0;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 1001;
  overflow: hidden;

  .fps-value {
    font-size: 18px;
    font-weight: 600;
    color: var(--color-text-secondary);
    line-height: 1;
    transition: all 0.3s ease;
  }

  .fps-text {
    position: absolute;
    left: -10px;
    opacity: 0;
    font-size: 14px;
    font-weight: 500;
    color: var(--color-text-secondary);
    white-space: nowrap;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    filter: blur(4px);
    transform: translateX(-10px);
  }

  &.hovered {
    width: 160px;
    border-radius: 30px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);

    .fps-value {
      transform: translateX(30px);
    }

    .fps-text {
      opacity: 1;
      left: 16px;
      filter: blur(0);
      transform: translateX(0);
    }
  }

  &.scrolled {
    width: var(--nav-height-scrolled);
    height: var(--nav-height-scrolled);
    top: 10px;

    &.hovered {
      width: 160px;
    }
  }
}

/* Search Box */
.search-box {
  position: fixed;
  right: 20px;
  top: 20px;
  display: flex;
  align-items: center;
  width: var(--nav-height);
  height: var(--nav-height);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: 50%;
  box-shadow: var(--shadow-nav);
  flex-shrink: 0;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 1001;
  overflow: hidden;

  .search-icon {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 20px;
    height: 20px;
    color: var(--color-text-secondary);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    flex-shrink: 0;
  }

  .search-input {
    position: absolute;
    left: -10px;
    width: 122px;
    height: 100%;
    padding: 0 16px 0 36px;
    background: transparent;
    border: none;
    outline: none;
    font-size: 14px;
    color: var(--color-text-primary);
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    filter: blur(4px);
    transform: translateX(-10px);

    &::placeholder {
      color: var(--color-text-tertiary);
    }
  }

  &.search-hovered {
    width: 170px;
    border-radius: 30px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);

    .search-icon {
      left: 16px;
      transform: translateX(0);
    }

    .search-input {
      opacity: 1;
      left: 12px;
      filter: blur(0);
      transform: translateX(0);
    }
  }

  &.scrolled {
    width: var(--nav-height-scrolled);
    height: var(--nav-height-scrolled);
    top: 10px;

    &.search-hovered {
      width: 170px;
    }
  }
}

@media (max-width: 768px) {
  .fps-display,
  .search-box {
    display: none;
  }
}

.nav-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;

  .logo-text {
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--color-text-primary);
    letter-spacing: -0.5px;
    transition: color var(--transition-base);
  }

  &:hover .logo-text {
    color: var(--color-accent);
  }
}

/* Desktop Navigation */
.nav-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  list-style: none;

  &.desktop-nav {
    @media (max-width: 768px) {
      display: none;
    }
  }
}

.nav-item {
  position: relative;
}

.nav-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 17px;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: color var(--transition-base);
  cursor: pointer;

  &:hover,
  &.active {
    color: var(--color-accent);
  }

  // Hover underline effect
  &::after {
    content: '';
    position: absolute;
    bottom: 4px;
    left: 50%;
    width: 0;
    height: 3px;
    background: var(--color-accent);
    border-radius: 999px;
    pointer-events: none;
    transition: all var(--transition-base);
    transform: translateX(-50%);
  }

  &:hover::after {
    width: 60%;
  }
}

/* Dropdown Menu */
.nav-dropdown {
  position: relative;
  padding-bottom: 8px;
  margin-bottom: -8px;

  &:hover .dropdown-menu {
    opacity: 1;
    transform: translateY(0);
    visibility: visible;
  }
}

.dropdown-arrow {
  width: 14px;
  height: 14px;
  transition: transform var(--transition-base);
}

.dropdown-trigger:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  z-index: 20;
  transform: translateY(-5px);
  min-width: 140px;
  padding: var(--spacing-sm);
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition-smooth);
  list-style: none;

  li {
    margin: var(--spacing-xs) 0;
  }

  .dropdown-link {
    display: block;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
    border-radius: var(--radius-sm);
    transition: all var(--transition-base);

    &:hover {
      color: var(--color-accent);
      background: var(--color-accent-light);
    }
  }
}

/* Right Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

/* Theme Toggle */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 20px;
    height: 20px;
    color: var(--color-text-secondary);
    transition: all var(--transition-base);
  }

  &:hover {
    background: var(--color-accent-light);

    svg {
      color: var(--color-accent);
      transform: rotate(15deg);
    }
  }
}

/* Mobile Menu Toggle */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;

  @media (max-width: 768px) {
    display: flex;
  }

  .menu-line {
    width: 22px;
    height: 1.5px;
    background: var(--color-text-secondary);
    border-radius: 2px;
    transition: all var(--transition-base);
  }

  &:hover .menu-line {
    background: var(--color-accent);
  }

  &.active {
    .menu-line:nth-child(1) {
      transform: translateY(6.5px) rotate(45deg);
    }
    .menu-line:nth-child(2) {
      opacity: 0;
    }
    .menu-line:nth-child(3) {
      transform: translateY(-6.5px) rotate(-45deg);
    }
  }
}

/* Mobile Navigation */
.mobile-nav {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  flex-direction: column;
  padding: var(--spacing-md);
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  list-style: none;

  .nav-link {
    display: block;
    padding: var(--spacing-md);
    font-size: var(--font-size-lg);
  }
}

.dropdown-menu-mobile {
  padding-left: var(--spacing-lg);
  list-style: none;

  .dropdown-link {
    display: block;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
  }
}

/* Slide Down Animation for Mobile Menu */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all var(--transition-smooth);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Dark Mode Adjustments */
[data-theme="dark"] {
  .nav-container {
    background: var(--glass-bg);
    border-color: rgba(255, 255, 255, 0.1);
    box-shadow: var(--shadow-nav);
  }

  .nav-container.is-prompt-gradient-visible.is-copy-prompt {
    background: rgba(20, 83, 45, 0.46);
    box-shadow:
      0 10px 22px rgba(22, 163, 74, 0.1),
      inset 0 1px 0 rgba(220, 252, 231, 0.08);
  }

  .nav-container.is-prompt-gradient-visible.is-devtools-prompt {
    background: rgba(127, 29, 29, 0.46);
    box-shadow:
      0 10px 22px rgba(220, 38, 38, 0.1),
      inset 0 1px 0 rgba(254, 226, 226, 0.08);
  }

  .nav-prompt {
    color: #f3f4f6;
    text-shadow: 0 1px 12px rgba(0, 0, 0, 0.35);

    &.is-copy {
      color: #dcfce7;
    }

    &.is-devtools {
      color: #fee2e2;
    }
  }
}
</style>
