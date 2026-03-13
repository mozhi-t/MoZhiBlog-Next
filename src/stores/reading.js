/**
 * Reading Store - 阅读辅助和个性化设置
 * 管理字号大小、阴影强度、圆角大小等阅读体验设置
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useReadingStore = defineStore('reading', () => {
  // ==================== 字号大小 ====================
  const fontSize = ref('medium')

  // 字号映射 (14px - 20px)
  const fontSizeMap = {
    small: '14px',
    medium: '17px',
    large: '20px'
  }

  // 当前字号CSS值
  const currentFontSize = computed(() => fontSizeMap[fontSize.value])

  // 初始化字号
  const initFontSize = () => {
    const savedSize = localStorage.getItem('blog-font-size')
    if (savedSize && fontSizeMap[savedSize]) {
      fontSize.value = savedSize
    }
    applyFontSize()
  }

  // 应用字号
  const applyFontSize = () => {
    document.documentElement.style.setProperty('--reading-font-size', currentFontSize.value)
    // 同时更新基础字号变量
    document.documentElement.style.setProperty('--font-size-base', currentFontSize.value)
  }

  // 设置字号
  const setFontSize = (size) => {
    if (fontSizeMap[size]) {
      fontSize.value = size
      localStorage.setItem('blog-font-size', size)
      applyFontSize()
    }
  }

  // 字号循环切换
  const cycleFontSize = () => {
    const sizes = ['small', 'medium', 'large']
    const currentIndex = sizes.indexOf(fontSize.value)
    const nextIndex = (currentIndex + 1) % sizes.length
    setFontSize(sizes[nextIndex])
  }

  // ==================== 阴影强度 ====================
  const shadowIntensity = ref('medium')

  const shadowMap = {
    none: { sm: 'none', md: 'none', lg: 'none' },
    light: { sm: '0 1px 4px rgba(0, 0, 0, 0.02)', md: '0 2px 8px rgba(0, 0, 0, 0.03)', lg: '0 4px 16px rgba(0, 0, 0, 0.04)' },
    medium: { sm: '0 2px 8px rgba(0, 0, 0, 0.04)', md: '0 4px 16px rgba(0, 0, 0, 0.06)', lg: '0 8px 32px rgba(0, 0, 0, 0.08)' },
    strong: { sm: '0 4px 16px rgba(0, 0, 0, 0.08)', md: '0 8px 32px rgba(0, 0, 0, 0.12)', lg: '0 16px 48px rgba(0, 0, 0, 0.16)' }
  }

  const currentShadow = computed(() => shadowMap[shadowIntensity.value])

  const initShadow = () => {
    const savedShadow = localStorage.getItem('blog-shadow')
    if (savedShadow && shadowMap[savedShadow]) {
      shadowIntensity.value = savedShadow
    }
    applyShadow()
  }

  const applyShadow = () => {
    const shadow = currentShadow.value
    document.documentElement.style.setProperty('--shadow-sm', shadow.sm)
    document.documentElement.style.setProperty('--shadow-md', shadow.md)
    document.documentElement.style.setProperty('--shadow-lg', shadow.lg)
  }

  const setShadow = (intensity) => {
    if (shadowMap[intensity]) {
      shadowIntensity.value = intensity
      localStorage.setItem('blog-shadow', intensity)
      applyShadow()
    }
  }

  // ==================== 圆角大小 ====================
  const borderRadius = ref('medium')

  const radiusMap = {
    none: { sm: '0', md: '0', lg: '0', xl: '0' },
    small: { sm: '4px', md: '6px', lg: '8px', xl: '12px' },
    medium: { sm: '8px', md: '12px', lg: '16px', xl: '24px' },
    large: { sm: '12px', md: '16px', lg: '20px', xl: '28px' },
    full: { sm: '16px', md: '24px', lg: '32px', xl: '40px' }
  }

  const currentRadius = computed(() => radiusMap[borderRadius.value])

  const initRadius = () => {
    const savedRadius = localStorage.getItem('blog-radius')
    if (savedRadius && radiusMap[savedRadius]) {
      borderRadius.value = savedRadius
    }
    applyRadius()
  }

  const applyRadius = () => {
    const radius = currentRadius.value
    document.documentElement.style.setProperty('--radius-sm', radius.sm)
    document.documentElement.style.setProperty('--radius-md', radius.md)
    document.documentElement.style.setProperty('--radius-lg', radius.lg)
    document.documentElement.style.setProperty('--radius-xl', radius.xl)
  }

  const setRadius = (size) => {
    if (radiusMap[size]) {
      borderRadius.value = size
      localStorage.setItem('blog-radius', size)
      applyRadius()
    }
  }

  // ==================== 初始化所有设置 ====================
  const initAll = () => {
    initFontSize()
    initShadow()
    initRadius()
  }

  // 目录锚点激活状态
  const activeAnchor = ref('')
  const setActiveAnchor = (id) => {
    activeAnchor.value = id
  }

  return {
    // 字号
    fontSize,
    currentFontSize,
    fontSizeMap,
    initFontSize,
    setFontSize,
    cycleFontSize,
    // 阴影
    shadowIntensity,
    currentShadow,
    shadowMap,
    initShadow,
    setShadow,
    // 圆角
    borderRadius,
    currentRadius,
    radiusMap,
    initRadius,
    setRadius,
    // 初始化
    initAll,
    // 锚点
    activeAnchor,
    setActiveAnchor
  }
})
