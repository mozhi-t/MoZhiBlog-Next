/**
 * useIntersectionObserver - 滚动可视区域检测
 * 使用Intersection Observer API实现元素进入可视区域时的动效
 */
import { ref, onMounted, onUnmounted } from 'vue'

export function useIntersectionObserver(options = {}) {
  const isVisible = ref(false)
  const targetRef = ref(null)
  let observer = null

  const defaultOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px',
    ...options
  }

  onMounted(() => {
    if (!targetRef.value) return

    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true
          // 只触发一次
          observer?.unobserve(entry.target)
        }
      })
    }, defaultOptions)

    observer.observe(targetRef.value)
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return {
    targetRef,
    isVisible
  }
}

/**
 * useScrollObserver - 监听滚动位置
 * 用于返回顶部按钮显示/隐藏等
 */
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
    // 初始化
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

/**
 * useActiveAnchor - 目录锚点跟随滚动
 */
export function useActiveAnchor(anchorIds = []) {
  const activeAnchor = ref('')
  let observer = null

  onMounted(() => {
    if (anchorIds.length === 0) return

    const callback = (entries) => {
      // 找到第一个在视口顶部的标题
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeAnchor.value = entry.target.id
          break
        }
      }
    }

    observer = new IntersectionObserver(callback, {
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
