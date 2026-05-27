<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from './stores/theme'
import { useReadingStore } from './stores/reading'
import NavHeader from './components/common/NavHeader.vue'
import SiteFooter from './components/common/SiteFooter.vue'
import ReadingTools from './components/common/ReadingTools.vue'
import InitialLoader from './components/common/InitialLoader.vue'

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const readingStore = useReadingStore()

const isAdminPage = computed(() => route.path.startsWith('/admin'))
const shouldUsePageLoader = (targetRoute) => {
  return (
    targetRoute.name === 'Home' ||
    targetRoute.name === 'Article' ||
    targetRoute.path === '/' ||
    targetRoute.path.startsWith('/article/')
  )
}

const isPageLoading = ref(!isAdminPage.value && shouldUsePageLoader(route))
const shouldShowLoader = computed(() => !isAdminPage.value && isPageLoading.value)

let removeBeforeGuard = null
let removeAfterGuard = null

const finishPageLoading = () => {
  isPageLoading.value = false
}

onMounted(() => {
  themeStore.initTheme()
  readingStore.initAll()

  router.isReady().then(() => {
    isPageLoading.value = !route.path.startsWith('/admin') && shouldUsePageLoader(route)
  })

  removeBeforeGuard = router.beforeEach((to, from, next) => {
    if (!to.path.startsWith('/admin') && from.matched.length > 0 && shouldUsePageLoader(to)) {
      isPageLoading.value = true
    } else if (!shouldUsePageLoader(to)) {
      isPageLoading.value = false
    }

    next()
  })

  removeAfterGuard = router.afterEach((to, from) => {
    if (to.path.startsWith('/admin') || !shouldUsePageLoader(to)) {
      isPageLoading.value = false
      return
    }

    if (from.matched.length === 0) {
      return
    }

    isPageLoading.value = true
  })
})

onUnmounted(() => {
  removeBeforeGuard?.()
  removeAfterGuard?.()
})
</script>

<template>
  <div class="app-wrapper">
    <NavHeader v-if="!isAdminPage">
      <template #below-nav="{ isScrolled }">
        <InitialLoader
          :active="shouldShowLoader"
          :load-key="route.fullPath"
          :scrolled="isScrolled"
          @complete="finishPageLoading"
        />
      </template>
    </NavHeader>

    <main class="main-content" :class="{ 'no-header': isAdminPage }">
      <div class="route-stage">
        <router-view v-slot="{ Component }">
          <Transition :name="isAdminPage ? '' : 'page-fade'" appear>
            <component :is="Component" :key="isAdminPage ? undefined : route.fullPath" class="route-page" />
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
