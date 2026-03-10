/**
 * Admin Store - 管理员状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminApi } from '@/api'
import router from '@/router'

export const useAdminStore = defineStore('admin', () => {
  // State
  const token = ref(localStorage.getItem('admin_token') || '')
  const adminInfo = ref(null)
  const sidebarCollapsed = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)

  // Actions
  const login = async (username, password) => {
    const res = await adminApi.login({ username, password })
    token.value = res.data.token
    adminInfo.value = res.data.admin
    localStorage.setItem('admin_token', res.data.token)
    return res.data
  }

  const getInfo = async () => {
    if (!token.value) return null
    try {
      const res = await adminApi.getInfo()
      adminInfo.value = res.data
      return res.data
    } catch (error) {
      logout()
      throw error
    }
  }

  const logout = () => {
    token.value = ''
    adminInfo.value = null
    localStorage.removeItem('admin_token')
    router.push('/admin/login')
  }

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return {
    token,
    adminInfo,
    sidebarCollapsed,
    isLoggedIn,
    login,
    getInfo,
    logout,
    toggleSidebar
  }
})
