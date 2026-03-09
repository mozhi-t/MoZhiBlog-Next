/**
 * Reading Store - 阅读辅助设置
 * 管理字号大小、目录锚点等阅读体验设置
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useReadingStore = defineStore('reading', () => {
  // 字号大小: 'small' | 'medium' | 'large'
  const fontSize = ref('medium')

  // 字号映射
  const fontSizeMap = {
    small: '15px',
    medium: '17px',
    large: '19px'
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

  // 目录锚点激活状态
  const activeAnchor = ref('')
  const setActiveAnchor = (id) => {
    activeAnchor.value = id
  }

  return {
    fontSize,
    currentFontSize,
    fontSizeMap,
    initFontSize,
    setFontSize,
    cycleFontSize,
    activeAnchor,
    setActiveAnchor
  }
})
