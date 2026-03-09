/**
 * Theme Store - 主题模式管理
 * 使用Pinia管理暗黑/浅色模式状态
 */
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 主题模式: 'light' | 'dark'
  const theme = ref('light')

  // 初始化主题
  const initTheme = () => {
    // 优先读取localStorage
    const savedTheme = localStorage.getItem('blog-theme')
    if (savedTheme) {
      theme.value = savedTheme
    } else {
      // 检测系统偏好
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      theme.value = prefersDark ? 'dark' : 'light'
    }
    applyTheme()
  }

  // 应用主题到DOM
  const applyTheme = () => {
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  // 切换主题
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('blog-theme', theme.value)
    applyTheme()
  }

  // 监听主题变化
  watch(theme, () => {
    applyTheme()
  })

  return {
    theme,
    initTheme,
    toggleTheme
  }
})
