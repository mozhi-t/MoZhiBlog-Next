<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from './stores/theme'
import { useReadingStore } from './stores/reading'
import NavHeader from './components/common/NavHeader.vue'
import SiteFooter from './components/common/SiteFooter.vue'
import ReadingTools from './components/common/ReadingTools.vue'
import InitialLoader from './components/common/InitialLoader.vue'

const route = useRoute()
const themeStore = useThemeStore()
const readingStore = useReadingStore()
const homeLoaderDone = ref(false)
const homeLoaderMounted = ref(route.path === '/')
const homeLoaderActive = ref(route.path === '/')

const isAdminPage = computed(() => route.path.startsWith('/admin'))
const showInitialLoader = computed(() => homeLoaderMounted.value && !isAdminPage.value)

const handleHomePageReady = () => {
  if (route.path !== '/' || homeLoaderDone.value) return
  homeLoaderDone.value = true
  homeLoaderActive.value = false
}

const handleLoaderHidden = () => {
  homeLoaderMounted.value = false
}

onMounted(() => {
  themeStore.initTheme()
  readingStore.initAll()
})

watch(
  () => route.path,
  (path) => {
    if (path === '/' && !homeLoaderDone.value) {
      homeLoaderMounted.value = true
      homeLoaderActive.value = true
      return
    }

    if (path !== '/') {
      homeLoaderActive.value = false
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="app-wrapper">
    <InitialLoader
      v-if="showInitialLoader"
      :active="homeLoaderActive"
      @hidden="handleLoaderHidden"
    />

    <NavHeader v-if="!isAdminPage" />

    <main class="main-content" :class="{ 'no-header': isAdminPage }">
      <router-view v-slot="{ Component }">
        <Transition name="slide" mode="out-in">
          <component :is="Component" @page-ready="handleHomePageReady" />
        </Transition>
      </router-view>
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

  &.no-header {
    margin-top: 0;
  }
}

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

@media (max-width: 768px) {
  .slide-enter-from {
    transform: translateY(20px);
  }

  .slide-leave-to {
    transform: translateY(-20px);
  }
}
</style>
