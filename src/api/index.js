/**
 * API Service - Axios 封装
 */
import axios from 'axios'
import { useAdminStore } from '@/stores/admin'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 登录请求不需要携带 token
    if (config.url === '/admin/login') {
      return config
    }

    const adminStore = useAdminStore()
    if (adminStore.token) {
      config.headers.Authorization = `Bearer ${adminStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      return Promise.reject(new Error(res.msg || '请求失败'))
    }
    return res
  },
  error => {
    // 处理401/403错误
    if (error.response?.status === 401 || error.response?.status === 403) {
      const adminStore = useAdminStore()
      adminStore.logout()
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export default api

// ==================== API 方法 ====================

// 管理员
export const adminApi = {
  login: (data) => api.post('/admin/login', data),
  getInfo: () => api.get('/admin/me'),
  logout: () => api.post('/admin/logout'),
  updateSettings: (data) => api.put('/admin/settings', data)
}

// 文章
export const articleApi = {
  // 公开
  list: (params) => api.get('/articles', { params }),
  detail: (id) => api.get(`/articles/${id}`),
  hot: (limit = 10) => api.get('/articles/hot', { params: { limit } }),

  // 管理
  create: (data) => api.post('/articles', data),
  update: (id, data) => api.put(`/articles/${id}`, data),
  delete: (id) => api.delete(`/articles/${id}`)
}

// 分类
export const categoryApi = {
  list: () => api.get('/categories'),
  create: (data) => api.post('/categories', data),
  update: (id, data) => api.put(`/categories/${id}`, data),
  delete: (id) => api.delete(`/categories/${id}`)
}

// 评论
export const commentApi = {
  list: (articleId) => api.get(`/comments/${articleId}`),
  create: (data) => api.post('/comments', data),

  // 管理
  all: (params) => api.get('/comments/all', { params }),
  delete: (id) => api.delete(`/comments/${id}`),
  approve: (id, isApproved) => api.put(`/comments/${id}/approve`, null, { params: { is_approved: isApproved } })
}

// 友链
export const friendLinkApi = {
  list: () => api.get('/friend_links'),
  create: (data) => api.post('/friend_links', data),

  // 管理
  all: (params) => api.get('/friend_links/all', { params }),
  update: (id, data) => api.put(`/friend_links/${id}`, data),
  delete: (id) => api.delete(`/friend_links/${id}`)
}

// 标签
export const tagApi = {
  list: () => api.get('/tags'),

  // 管理
  all: (params) => api.get('/tags/all', { params }),
  create: (data) => api.post('/tags', data),
  update: (id, data) => api.put(`/tags/${id}`, data),
  delete: (id) => api.delete(`/tags/${id}`)
}

// 统计
export const statsApi = {
  dashboard: () => api.get('/stats/dashboard')
}

// 留言板
export const messageApi = {
  list: () => api.get('/messages'),
  create: (data) => api.post('/messages', data),

  // 管理
  all: (params) => api.get('/messages/all', { params }),
  update: (id, data) => api.put(`/messages/${id}`, data),
  delete: (id) => api.delete(`/messages/${id}`)
}
