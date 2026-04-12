/**
 * Scroll / visibility observers.
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'

export function useIntersectionObserver(options = {}, externalTargetRef = null) {
  const isVisible = ref(false)
  const targetRef = externalTargetRef || ref(null)
  let observer = null

  const defaultOptions = {
    threshold: 0,
    rootMargin: '0px 0px -10px 0px',
    ...options
  }

  const startObserver = () => {
    if (!targetRef.value || isVisible.value) return

    // Fallback for older mobile browsers and embedded webviews.
    if (typeof window === 'undefined' || typeof window.IntersectionObserver !== 'function') {
      isVisible.value = true
      return
    }

    observer = new window.IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true
          observer?.unobserve(entry.target)
        }
      })
    }, defaultOptions)

    observer.observe(targetRef.value)
  }

  watch(targetRef, (newVal) => {
    if (newVal && !isVisible.value) {
      startObserver()
    }
  })

  onMounted(() => {
    startObserver()
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return {
    targetRef,
    isVisible
  }
}

export function useScrollObserver(threshold = 300) {
  const scrollY = ref(0)
  const isScrolled = ref(false)
  let ticking = false

  const handleScroll = () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        scrollY.value = window.scrollY
        isScrolled.value = scrollY.value > threshold
        ticking = false
      })
      ticking = true
    }
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
    scrollY.value = window.scrollY
    isScrolled.value = window.scrollY > threshold
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return {
    scrollY,
    isScrolled
  }
}

export function useActiveAnchor(anchorIds = []) {
  const activeAnchor = ref('')
  let observer = null

  onMounted(() => {
    if (anchorIds.length === 0) return

    const callback = (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeAnchor.value = entry.target.id
          break
        }
      }
    }

    if (typeof window === 'undefined' || typeof window.IntersectionObserver !== 'function') {
      activeAnchor.value = anchorIds[0] || ''
      return
    }

    observer = new window.IntersectionObserver(callback, {
      rootMargin: '-80px 0px -60% 0px',
      threshold: 0
    })

    anchorIds.forEach((id) => {
      const el = document.getElementById(id)
      if (el) observer.observe(el)
    })
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return {
    activeAnchor
  }
}
