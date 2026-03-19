<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from './stores/theme'
import { useReadingStore } from './stores/reading'
import NavHeader from './components/common/NavHeader.vue'
import SiteFooter from './components/common/SiteFooter.vue'
import ReadingTools from './components/common/ReadingTools.vue'

const route = useRoute()
const themeStore = useThemeStore()
const readingStore = useReadingStore()

const isAdminPage = computed(() => route.path.startsWith('/admin'))

onMounted(() => {
  themeStore.initTheme()
  readingStore.initAll()
})
</script>

<template>
  <div class="app-wrapper">
    <NavHeader v-if="!isAdminPage" />

    <main class="main-content" :class="{ 'no-header': isAdminPage }">
      <div class="route-stage">
        <router-view v-slot="{ Component }">
          <Transition name="page-fade" appear>
            <component :is="Component" :key="route.fullPath" class="route-page" />
          </Transition>
        </router-view>
      </div>
    </main>

    <SiteFooter v-if="!isAdminPage" />
    <ReadingTools v-if="!isAdminPage" />
  </div>
</template>

<style lang="scss">
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
  overflow-x: clip;

  &.no-header {
    margin-top: 0;
  }
}

.route-stage {
  position: relative;
  width: 100%;
}

.route-page {
  width: 100%;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease, filter 0.3s ease;
  will-change: transform, opacity, filter;
}

.page-fade-leave-active {
  position: absolute;
  inset: 0;
  pointer-events: none;
 }

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateX(28px);
  filter: blur(6px);
}

.page-fade-enter-to,
.page-fade-leave-from {
  opacity: 1;
  transform: translateX(0);
  filter: blur(0);
}

@media (max-width: 768px) {
  .page-fade-enter-from,
  .page-fade-leave-to {
    transform: translateY(20px);
  }
}

</style>
