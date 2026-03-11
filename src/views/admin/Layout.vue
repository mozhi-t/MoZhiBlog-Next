<template>
  <div class="admin-layout" :class="{ collapsed: adminStore.sidebarCollapsed }">
    <!-- 顶部导航 -->
    <header class="admin-header">
      <div class="header-left">
        <button class="menu-toggle" @click="adminStore.toggleSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        <span class="header-title">后台管理</span>
      </div>
      <div class="header-right">
        <span class="admin-name">{{ adminStore.adminInfo?.username }}</span>
        <button class="logout-btn" @click="handleLogout">退出</button>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="admin-sidebar">
      <nav class="sidebar-nav">
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
    </aside>

    <!-- 主内容区 -->
    <main class="admin-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/stores/admin'

const adminStore = useAdminStore()

const menuItems = [
  {
    name: '仪表盘',
    path: 'dashboard',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>'
  },
  {
    name: '文章管理',
    path: 'articles',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
  },
  {
    name: '分类管理',
    path: 'categories',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>'
  },
  {
    name: '标签管理',
    path: 'tags',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>'
  },
  {
    name: '评论管理',
    path: 'comments',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
  },
  {
    name: '友链管理',
    path: 'friend-links',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
  },
  {
    name: '留言管理',
    path: 'messages',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
  }
]

const handleLogout = () => {
  adminStore.logout()
}
</script>

<style lang="scss" scoped>
.admin-layout {
  min-height: 100vh;
  background: var(--color-bg-primary);
  transition: all var(--transition-smooth);
}

.admin-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.menu-toggle {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-text-primary);
  transition: background var(--transition-base);

  svg {
    width: 20px;
    height: 20px;
  }

  &:hover {
    background: var(--color-bg-tertiary);
  }
}

.header-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.admin-name {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.logout-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  background: var(--color-accent-light);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-accent);
    color: #fff;
  }
}

.admin-sidebar {
  position: fixed;
  top: 56px;
  left: 0;
  bottom: 0;
  width: 240px;
  background: var(--glass-bg-solid);
  backdrop-filter: var(--glass-blur);
  border-right: 1px solid var(--color-border);
  padding: var(--spacing-lg);
  transition: all var(--transition-smooth);
  z-index: 90;
  overflow-y: auto;
}

.collapsed .admin-sidebar {
  width: 80px;
  padding: var(--spacing-lg) var(--spacing-sm);

  .nav-text {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: var(--spacing-md);
  }
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);

  &:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-text-primary);
  }

  &.active {
    background: var(--color-accent-light);
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

.admin-main {
  margin-left: 240px;
  margin-top: 56px;
  padding: var(--spacing-xl);
  min-height: calc(100vh - 56px);
  transition: margin-left var(--transition-smooth);
}

.collapsed .admin-main {
  margin-left: 80px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-main {
    margin-left: 0;
  }
}
</style>
