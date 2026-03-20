<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  active: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['hidden'])

const dots = Array.from({ length: 7 }, (_, index) => index)
const visible = ref(true)
const isFinishing = ref(false)
let finishTimer = null
const FINISH_HIDE_DELAY = 680

const clearTimers = () => {
  if (finishTimer) {
    clearTimeout(finishTimer)
    finishTimer = null
  }
}

const finishAndHide = () => {
  clearTimers()
  isFinishing.value = true

  finishTimer = setTimeout(() => {
    visible.value = false
    isFinishing.value = false
    emit('hidden')
  }, FINISH_HIDE_DELAY)
}

watch(
  () => props.active,
  (isActive) => {
    if (isActive) {
      visible.value = true
      isFinishing.value = false
      return
    }

    finishAndHide()
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  clearTimers()
})
</script>

<template>
  <Transition name="initial-loader-fade">
    <div
      v-if="visible"
      class="initial-loader"
      :class="{ 'is-finishing': isFinishing }"
      aria-live="polite"
      aria-label="Loading"
    >
      <div class="initial-loader__inner">
        <div class="initial-loader__label" aria-hidden="true">loading</div>

        <div class="initial-loader__text" role="status">
          <span
            v-for="index in dots"
            :key="index"
            class="initial-loader__dot"
            :style="{ animationDelay: `${index * 0.09}s` }"
          />
        </div>

      </div>
    </div>
  </Transition>
</template>

<style lang="scss" scoped>
.initial-loader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background:
    radial-gradient(circle at 50% 16%, rgba(255, 255, 255, 0.72), rgba(245, 245, 247, 0.96) 42%, #eef0f3 100%);
  backdrop-filter: blur(10px) saturate(110%);
  transition:
    opacity 0.58s cubic-bezier(0.22, 1, 0.36, 1),
    background 0.68s cubic-bezier(0.22, 1, 0.36, 1),
    backdrop-filter 0.68s cubic-bezier(0.22, 1, 0.36, 1);
}

[data-theme="dark"] .initial-loader {
  background:
    radial-gradient(circle at 50% 16%, rgba(78, 78, 82, 0.26), rgba(22, 22, 24, 0.96) 42%, #070707 100%);
}

.initial-loader__inner {
  width: min(300px, 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  transition:
    opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1),
    filter 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.initial-loader__label {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", "PingFang SC", sans-serif;
  font-size: clamp(18px, 3.2vw, 22px);
  font-weight: 400;
  letter-spacing: 0.11em;
  text-transform: lowercase;
  color: rgba(29, 29, 31, 0.72);
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.38);
}

[data-theme="dark"] .initial-loader__label {
  color: rgba(255, 255, 255, 0.76);
  text-shadow: none;
}

.initial-loader__text {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 16px;
}

.initial-loader__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(29, 29, 31, 0.38);
  box-shadow:
    0 0 0 0.5px rgba(255, 255, 255, 0.44),
    0 1px 2px rgba(0, 0, 0, 0.08);
  animation: loaderBounce 1.45s cubic-bezier(0.33, 0.72, 0.12, 1) infinite;
}

[data-theme="dark"] .initial-loader__dot {
  background: rgba(255, 255, 255, 0.52);
  box-shadow:
    0 0 0 0.5px rgba(255, 255, 255, 0.08),
    0 1px 2px rgba(0, 0, 0, 0.22);
}

.initial-loader.is-finishing .initial-loader__inner {
  opacity: 0;
  filter: blur(14px);
  transform: scale(1.045);
}

.initial-loader.is-finishing .initial-loader__dot {
  animation-play-state: paused;
}

.initial-loader.is-finishing {
  pointer-events: none;
  opacity: 0;
  background:
    radial-gradient(circle at 50% 16%, rgba(255, 255, 255, 0), rgba(245, 245, 247, 0.1) 42%, rgba(238, 240, 243, 0) 100%);
  backdrop-filter: blur(0px) saturate(100%);
}

[data-theme="dark"] .initial-loader.is-finishing {
  background:
    radial-gradient(circle at 50% 16%, rgba(78, 78, 82, 0), rgba(22, 22, 24, 0.08) 42%, rgba(7, 7, 7, 0) 100%);
}

.initial-loader-fade-enter-active,
.initial-loader-fade-leave-active {
  transition:
    opacity 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    visibility 0.42s cubic-bezier(0.22, 1, 0.36, 1);
}

.initial-loader-fade-enter-from,
.initial-loader-fade-leave-to {
  opacity: 0;
}

@keyframes loaderBounce {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.42;
  }
  15% {
    transform: translateY(-3px) scale(1.12);
    opacity: 0.9;
  }
  30% {
    transform: translateY(0) scale(1);
    opacity: 0.55;
  }
}

@media (max-width: 640px) {
  .initial-loader__inner {
    gap: 16px;
  }

  .initial-loader__label {
    font-size: 18px;
  }

  .initial-loader__text {
    gap: 8px;
  }

  .initial-loader__dot {
    width: 5px;
    height: 5px;
  }

}
</style>
