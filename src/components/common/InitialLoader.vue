<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  active: {
    type: Boolean,
    default: true
  },
  loadKey: {
    type: String,
    default: ''
  },
  scrolled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['complete', 'hidden'])

const visible = ref(false)
const isOpen = ref(false)
const progress = ref(0)

let animationFrameId = null
let finishTimer = null
let openFrameId = null
let measureTimer = null
let completeTimer = null
let startedAt = 0
let loadRunId = 0
let totalResources = 0
let completedResources = 0
let resourceTimeoutTimer = null
const cleanupResourceListeners = []

const FINISH_HIDE_DELAY = 1700
const ENTER_DELAY = 180
const MIN_PROGRESS = 6
const CONTINUED_PROGRESS_CAP = 82
const MIN_VISIBLE_DURATION = 1200
const COMPLETE_HOLD_DURATION = 360
const RESOURCE_TIMEOUT = 4500
const RESOURCE_MEASURE_DELAY = 420

const progressPercent = computed(() => `${Math.round(progress.value)}%`)

const clearTimers = () => {
  if (finishTimer) {
    window.clearTimeout(finishTimer)
    finishTimer = null
  }

  if (openFrameId) {
    cancelAnimationFrame(openFrameId)
    openFrameId = null
  }

  if (measureTimer) {
    window.clearTimeout(measureTimer)
    measureTimer = null
  }

  if (completeTimer) {
    window.clearTimeout(completeTimer)
    completeTimer = null
  }

  if (resourceTimeoutTimer) {
    window.clearTimeout(resourceTimeoutTimer)
    resourceTimeoutTimer = null
  }
}

const stopProgressLoop = () => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }
}

const clearResourceListeners = () => {
  cleanupResourceListeners.splice(0).forEach((cleanup) => cleanup())
}

const markResourceDone = (runId) => {
  if (runId !== loadRunId) {
    return
  }

  completedResources += 1
  updateProgressFromResources(runId)
}

const addResourceListener = (element, runId) => {
  if (!element || element.dataset.loaderTracked === String(runId)) {
    return
  }

  element.dataset.loaderTracked = String(runId)
  totalResources += 1

  if (isElementLoaded(element)) {
    completedResources += 1
    return
  }

  let settled = false
  const settle = () => {
    if (settled) {
      return
    }

    settled = true
    markResourceDone(runId)
  }

  element.addEventListener('load', settle, { once: true })
  element.addEventListener('error', settle, { once: true })

  cleanupResourceListeners.push(() => {
    element.removeEventListener('load', settle)
    element.removeEventListener('error', settle)
  })
}

const isElementLoaded = (element) => {
  const tagName = element.tagName?.toLowerCase()

  if (tagName === 'img') {
    return element.complete
  }

  if (tagName === 'link') {
    try {
      return Boolean(element.sheet)
    } catch (error) {
      return true
    }
  }

  return true
}

const collectTrackableResources = (runId) => {
  clearResourceListeners()
  totalResources = 0
  completedResources = 0
  const currentPage = document.querySelector('.route-stage .route-page:last-child')
  const scope = currentPage || document

  scope.querySelectorAll('img').forEach((img) => {
    const isLazyPending = img.loading === 'lazy' && !img.complete

    if (!isLazyPending) {
      addResourceListener(img, runId)
    }
  })

  document.querySelectorAll('link[rel~="stylesheet"]').forEach((link) => {
    addResourceListener(link, runId)
  })

  document.querySelectorAll('script[src]').forEach((script) => {
    addResourceListener(script, runId)
  })

  if (document.fonts && document.fonts.status !== 'loaded') {
    totalResources += 1
    document.fonts.ready
      .then(() => markResourceDone(runId))
      .catch(() => markResourceDone(runId))
  }

  updateProgressFromResources(runId)
}

const updateProgressFromResources = (runId) => {
  if (runId !== loadRunId) {
    return
  }

  if (totalResources === 0) {
    progress.value = 100
    scheduleComplete(runId)
    return
  }

  progress.value = Math.max(
    MIN_PROGRESS,
    Math.min(100, (completedResources / totalResources) * 100)
  )

  if (completedResources >= totalResources) {
    scheduleComplete(runId)
  }
}

const scheduleComplete = (runId) => {
  if (runId !== loadRunId || completeTimer) {
    return
  }

  const elapsed = performance.now() - startedAt
  const delay = Math.max(0, MIN_VISIBLE_DURATION - elapsed) + COMPLETE_HOLD_DURATION

  completeTimer = window.setTimeout(() => {
    if (runId !== loadRunId) {
      return
    }

    progress.value = 100
    emit('complete')
  }, delay)
}

const scheduleResourceTimeout = (runId) => {
  resourceTimeoutTimer = window.setTimeout(() => {
    if (runId !== loadRunId) {
      return
    }

    completedResources = totalResources
    updateProgressFromResources(runId)
  }, RESOURCE_TIMEOUT)
}

const measurePageResources = (runId) => {
  nextTick(() => {
    requestAnimationFrame(() => {
      measureTimer = window.setTimeout(() => {
        measureTimer = null

        if (runId !== loadRunId) {
          return
        }

        collectTrackableResources(runId)
        scheduleResourceTimeout(runId)
      }, RESOURCE_MEASURE_DELAY)
    })
  })
}

const startLoading = () => {
  loadRunId += 1
  const runId = loadRunId
  const wasVisible = visible.value
  const continuedProgress = Math.min(
    Math.max(progress.value, MIN_PROGRESS),
    CONTINUED_PROGRESS_CAP
  )

  clearTimers()
  stopProgressLoop()
  clearResourceListeners()
  visible.value = true
  isOpen.value = wasVisible ? true : false
  progress.value = wasVisible ? continuedProgress : MIN_PROGRESS
  startedAt = performance.now()
  totalResources = 0
  completedResources = 0

  if (!wasVisible) {
    openFrameId = requestAnimationFrame(() => {
      openFrameId = requestAnimationFrame(() => {
        openFrameId = null
        isOpen.value = true
      })
    })
  }

  measurePageResources(runId)
}

const finishAndHide = () => {
  loadRunId += 1
  clearTimers()
  stopProgressLoop()
  clearResourceListeners()

  if (!visible.value) {
    emit('hidden')
    return
  }

  progress.value = 100
  isOpen.value = false

  finishTimer = window.setTimeout(() => {
    visible.value = false
    isOpen.value = false
    progress.value = 0
    emit('hidden')
  }, FINISH_HIDE_DELAY + ENTER_DELAY)
}

watch(
  () => [props.active, props.loadKey],
  ([isActive]) => {
    if (isActive) {
      startLoading()
      return
    }

    finishAndHide()
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  clearTimers()
  stopProgressLoop()
})
</script>

<template>
  <Transition name="initial-loader-pop" appear>
    <div
      v-if="visible"
      class="initial-loader"
      :class="{ 'is-open': isOpen, scrolled }"
      role="progressbar"
      aria-label="页面资源加载进度"
      aria-valuemin="0"
      aria-valuemax="100"
      :aria-valuenow="Math.round(progress)"
    >
      <div class="initial-loader__track">
        <div class="initial-loader__bar" :style="{ width: progressPercent }"></div>
      </div>
    </div>
  </Transition>
</template>

<style lang="scss" scoped>
.initial-loader {
  position: absolute;
  left: 50%;
  top: calc(100% + 10px);
  z-index: -1;
  width: clamp(104px, 12vw, 156px);
  height: 18px;
  padding: 3px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-nav);
  background: var(--glass-bg);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.38);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  pointer-events: none;
  transform-origin: 50% -18px;
  transform: translateX(-50%);
  overflow: hidden;
  will-change: transform, opacity, filter;
}

.initial-loader__track {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: inherit;
  background: rgba(255, 255, 255, 0.42);
}

.initial-loader__bar {
  width: 0;
  height: 100%;
  border-radius: inherit;
  background:
    linear-gradient(
      90deg,
      rgba(108, 108, 112, 0.7),
      rgba(150, 150, 156, 0.92)
    );
  box-shadow:
    0 0 14px rgba(82, 82, 88, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.36);
  transition: width 0.24s cubic-bezier(0.22, 1, 0.36, 1);
}

.initial-loader {
  transition:
    opacity 1.55s cubic-bezier(0.19, 1, 0.22, 1),
    transform 1.55s cubic-bezier(0.19, 1, 0.22, 1),
    filter 1.55s cubic-bezier(0.19, 1, 0.22, 1),
    box-shadow 1.55s cubic-bezier(0.19, 1, 0.22, 1),
    top 0.4s cubic-bezier(0.19, 1, 0.22, 1),
    width 0.4s cubic-bezier(0.19, 1, 0.22, 1),
    height 0.4s cubic-bezier(0.19, 1, 0.22, 1),
    padding 0.4s cubic-bezier(0.19, 1, 0.22, 1);
  opacity: 0;
  filter: blur(18px) saturate(0.92);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.28);
  transform: translate(-50%, -42px) scale(0.32, 0.42);
}

.initial-loader.scrolled {
  top: calc(100% + 8px);
  width: clamp(88px, 10vw, 132px);
  height: 15px;
  padding: 2.5px;
  transform-origin: 50% -14px;
}

.initial-loader.is-open {
  opacity: 1;
  filter: blur(0) saturate(1);
  box-shadow:
    0 10px 28px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.38);
  transform: translate(-50%, 0) scale(1);
}

[data-theme="dark"] .initial-loader {
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.42),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

[data-theme="dark"] .initial-loader__track {
  background: rgba(255, 255, 255, 0.08);
}

[data-theme="dark"] .initial-loader__bar {
  background:
    linear-gradient(
      90deg,
      rgba(150, 150, 156, 0.62),
      rgba(214, 214, 220, 0.88)
    );
  box-shadow:
    0 0 16px rgba(190, 190, 196, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .initial-loader {
    top: calc(100% + 8px);
    width: 118px;
    height: 16px;
  }

  .initial-loader.scrolled {
    top: calc(100% + 7px);
    width: 100px;
    height: 14px;
    padding: 2px;
  }
}
</style>
