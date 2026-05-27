<template>
  <div class="admin-layout" :class="{ collapsed: adminStore.sidebarCollapsed }">
    <AdminSidebar :current-path="route.path" />

    <main class="admin-main">
      <router-view v-slot="{ Component, route: currentRoute }">
        <Transition :name="transitionName" mode="out-in">
          <div :key="currentRoute.fullPath" class="page-container">
            <component :is="Component" />
          </div>
        </Transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import AdminSidebar from './AdminSidebar.vue'

const adminStore = useAdminStore()
const route = useRoute()

const menuItems = [
  { path: 'dashboard' },
  { path: 'articles' },
  { path: 'moments' },
  { path: 'categories' },
  { path: 'tags' },
  { path: 'friend-links' },
  { path: 'settings' }
]

const transitionName = ref('slide-down')

const getActiveIndex = () => {
  const currentPath = route.path.replace('/admin/', '')
  return menuItems.findIndex(item => item.path === currentPath)
}

watch(
  () => route.path,
  (newPath, oldPath) => {
    const newIndex = getActiveIndex()
    const oldPathClean = oldPath?.replace('/admin/', '')
    const oldIndex = menuItems.findIndex(item => item.path === oldPathClean)

    if (newIndex !== -1 && oldIndex !== -1 && newIndex !== oldIndex) {
      transitionName.value = newIndex > oldIndex ? 'slide-down' : 'slide-up'
    }
  }
)
</script>

<style lang="scss" scoped>
.admin-layout {
  min-height: 100vh;
  background: var(--color-bg-primary);
  transition: all var(--transition-smooth);
}

.admin-main {
  margin-left: 240px;
  padding: var(--spacing-xl);
  min-height: 100vh;
  transition: margin-left var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.page-container {
  width: 100%;
}

.collapsed .admin-main {
  margin-left: 80px;
}

/* 过渡动画 */
.slide-down-enter-active,
.slide-down-leave-active,
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease, filter 0.2s ease;
  will-change: transform, opacity, filter;
}

.slide-down-leave-active,
.slide-up-leave-active {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(20px);
  filter: blur(6px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
  filter: blur(6px);
}

.slide-down-enter-to,
.slide-down-leave-from {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(-20px);
  filter: blur(6px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
  filter: blur(6px);
}

.slide-up-enter-to,
.slide-up-leave-from {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}

@media (max-width: 768px) {
  .admin-main {
    margin-left: 0;
  }
}
</style>
