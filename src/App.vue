<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useThemeStore } from './stores/theme'
import { useReadingStore } from './stores/reading'
import NavHeader from './components/common/NavHeader.vue'
import SiteFooter from './components/common/SiteFooter.vue'
import ReadingTools from './components/common/ReadingTools.vue'

const route = useRoute()
const themeStore = useThemeStore()
const readingStore = useReadingStore()

// 判断是否在后台管理界面
const isAdminPage = computed(() => route.path.startsWith('/admin'))

// Initialize stores on mount
onMounted(() => {
  themeStore.initTheme()
  readingStore.initAll()
})
</script>

<template>
  <div class="app-wrapper">
    <!-- Navigation -->
    <NavHeader v-if="!isAdminPage" />

    <!-- Main Content -->
    <main class="main-content" :class="{ 'no-header': isAdminPage }">
      <router-view v-slot="{ Component }">
        <Transition name="slide" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>

    <!-- Footer -->
    <SiteFooter v-if="!isAdminPage" />

    <!-- Reading Tools -->
    <ReadingTools v-if="!isAdminPage" />
  </div>
</template>

<style lang="scss">
/* ============================================
   App Wrapper
   ============================================ */
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;

  &.no-header {
    margin-top: 0;
  }
}

/* Page Transition Animation */
/* PC端左右滑动 */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from {
  transform: translateX(30px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}

/* 移动端上下滑动 */
@media (max-width: 768px) {
  .slide-enter-from {
    transform: translateY(20px);
  }

  .slide-leave-to {
    transform: translateY(-20px);
  }
}
</style>
