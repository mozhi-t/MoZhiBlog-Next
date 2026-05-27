<template>
  <aside class="admin-sidebar">
    <div class="sidebar-header">
      <span class="sidebar-title">后台管理</span>
    </div>
    <nav class="sidebar-nav" ref="navRef">
      <div class="nav-indicator" ref="indicatorRef"></div>
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="'/admin/' + item.path"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon" v-html="item.icon"></span>
        <span class="nav-text">{{ item.name }}</span>
      </router-link>
    </nav>
    <div class="sidebar-footer">
      <button class="logout-btn" @click="handleLogout">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span>退出登录</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useAdminStore } from '@/stores/admin'

const props = defineProps({
  currentPath: {
    type: String,
    required: true
  }
})

const adminStore = useAdminStore()
const navRef = ref(null)
const indicatorRef = ref(null)

const menuItems = [
  { name: '仪表盘', path: 'dashboard', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>' },
  { name: '文章管理', path: 'articles', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>' },
  { name: '说说管理', path: 'moments', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8"/><path d="M8 13h5"/></svg>' },
  { name: '分类管理', path: 'categories', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>' },
  { name: '标签管理', path: 'tags', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>' },
  { name: '友链管理', path: 'friend-links', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>' },
  { name: '设置', path: 'settings', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>' }
]

const updateIndicator = (animate = false) => {
  const nav = navRef.value
  const indicator = indicatorRef.value
  if (!nav || !indicator) return

  const activeItem = nav.querySelector('.nav-item.active')
  if (!activeItem) return

  const navRect = nav.getBoundingClientRect()
  const itemRect = activeItem.getBoundingClientRect()
  const top = itemRect.top - navRect.top
  const height = itemRect.height

  if (animate) {
    indicator.style.transition = 'top 0.35s cubic-bezier(0.4, 0, 0.2, 1), height 0.35s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease'
  } else {
    indicator.style.transition = 'none'
  }

  indicator.style.top = `${top}px`
  indicator.style.height = `${height}px`
  indicator.style.opacity = '1'
}

watch(
  () => props.currentPath,
  (newPath, oldPath) => {
    console.log('Route changed from', oldPath, 'to', newPath)
    if (newPath !== oldPath) {
      nextTick(() => {
        console.log('Updating indicator with animation')
        updateIndicator(true)
      })
    }
  },
  { immediate: false }
)

onMounted(() => {
  console.log('AdminSidebar mounted')
  nextTick(() => {
    console.log('Initializing indicator')
    updateIndicator(false)
  })
})

const handleLogout = () => {
  adminStore.logout()
}
</script>

<style lang="scss" scoped>
.admin-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 240px;
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: 90;
}

.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
}

.sidebar-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-lg);
  overflow-y: auto;
  position: relative;
}

.nav-indicator {
  position: absolute;
  left: var(--spacing-lg);
  right: var(--spacing-lg);
  background: var(--color-accent-light);
  border-radius: var(--radius-lg);
  z-index: 0;
  pointer-events: none;
  opacity: 0;
}

.sidebar-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-lg);
  position: relative;
  z-index: 1;
  transition: color var(--transition-base);

  &:hover {
    color: var(--color-text-primary);
  }

  &.active {
    color: var(--color-accent);
  }
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;

  svg {
    width: 20px;
    height: 20px;
  }
}

.nav-text {
  font-size: var(--font-size-sm);
  font-weight: 500;
  white-space: nowrap;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-accent);
    border-color: var(--color-accent);
  }
}
</style>
