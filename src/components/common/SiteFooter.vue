<template>
  <footer class="site-footer" :class="{ visible: isVisible }">
    <div class="footer-content">
      <p class="site-time">
        本站已经运行 {{ runDays }} 天 {{ runHours }} 小时 {{ runMinutes }} 分钟 {{ runSeconds }} 秒
      </p>
      <p class="copyright">
        &copy; {{ currentYear }} {{ SITE_CONFIG.author.name }}. {{ SITE_CONFIG.footer.copyright }}
      </p>
      <div class="footer-links">
        <template v-for="(link, index) in SITE_CONFIG.footer.links" :key="link.href">
          <a
            :href="link.href"
            :target="link.external ? '_blank' : undefined"
            :rel="link.external ? 'noopener' : undefined"
          >
            {{ link.label }}
          </a>
          <span v-if="index < SITE_CONFIG.footer.links.length - 1" class="divider">路</span>
        </template>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { SITE_CONFIG } from '../../config/site'

const isVisible = ref(false)
const currentYear = computed(() => new Date().getFullYear())

const startDate = new Date(SITE_CONFIG.footer.startDate).getTime()
const runTime = ref(Date.now() - startDate)
let timer = null

const runDays = computed(() => Math.floor(runTime.value / (1000 * 60 * 60 * 24)))
const runHours = computed(() => Math.floor((runTime.value % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)))
const runMinutes = computed(() => Math.floor((runTime.value % (1000 * 60 * 60)) / (1000 * 60)))
const runSeconds = computed(() => Math.floor((runTime.value % (1000 * 60)) / 1000))

const checkScrollPosition = () => {
  const scrollHeight = document.documentElement.scrollHeight
  const clientHeight = window.innerHeight
  const scrollTop = window.scrollY
  isVisible.value = scrollTop + clientHeight >= scrollHeight - 100
}

onMounted(() => {
  window.addEventListener('scroll', checkScrollPosition, { passive: true })
  checkScrollPosition()
  timer = setInterval(() => {
    runTime.value = Date.now() - startDate
  }, 1000)
})

onUnmounted(() => {
  window.removeEventListener('scroll', checkScrollPosition)
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
.site-footer {
  padding: var(--spacing-3xl) var(--spacing-lg);
  margin-top: var(--spacing-3xl);
  background: var(--color-bg-tertiary);
  opacity: 0;
  transform: translateY(20px);
  transition: all var(--transition-smooth);

  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
}

.footer-content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  text-align: center;
}

.copyright,
.site-time {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-bottom: var(--spacing-sm);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);

  a {
    color: var(--color-text-tertiary);
    text-decoration: none;
    transition: color var(--transition-base);

    &:hover {
      color: var(--color-accent);
    }
  }

  .divider {
    color: var(--color-text-tertiary);
  }
}
</style>
