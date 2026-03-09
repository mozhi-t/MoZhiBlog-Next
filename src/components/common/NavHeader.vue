<template>
  <header class="nav-header" :class="{ scrolled: isScrolled, 'menu-open': menuOpen }">
    <nav class="nav-container">
      <!-- Logo -->
      <router-link to="/" class="nav-logo" @click="closeMenu">
        <span class="logo-text">MoZhi</span>
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
            <span class="nav-link dropdown-trigger">
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
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '../../stores/theme'

const route = useRoute()
const themeStore = useThemeStore()

const theme = computed(() => themeStore.theme)
const toggleTheme = () => themeStore.toggleTheme()

// Navigation Items
const navItems = [
  { name: '首页', path: '/' },
  { name: '分类', path: '/category', children: [
    { name: '技术', path: '/category/tech' },
    { name: '生活', path: '/category/life' },
    { name: '随笔', path: '/category/essay' }
  ]},
  { name: '归档', path: '/archive' },
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
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Active route check
const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
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
  transition: all var(--transition-smooth);
}

/* Logo */
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
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-base);
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
    height: 1px;
    background: var(--color-accent);
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
  left: 50%;
  transform: translateX(-50%) translateY(-5px);
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
  }
}
</style>
