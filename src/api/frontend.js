/**
 * Frontend API Service - 主页前端API
 * 不需要管理员Token
 */
import axios from 'axios'

const frontendApi = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

const getArticleAccessToken = (articleId) => {
  if (!articleId) return ''
  return sessionStorage.getItem(`article_access_${articleId}`) || ''
}

// 响应处理
frontendApi.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ==================== 公开接口 ====================

// 文章
export const articlesApi = {
  // 获取文章列表
  list: (params) => frontendApi.get('/articles', { params }),
  // 获取文章详情
  detail: (id) => frontendApi.get(`/articles/${id}`, {
    headers: {
      'X-Article-Access-Token': getArticleAccessToken(id)
    }
  }),
  // 获取文章引用信息
  reference: (id) => frontendApi.get(`/articles/${id}/reference`),
  // 校验文章访问密码
  verifyPassword: (id, password) => frontendApi.post(`/articles/${id}/verify-password`, { password }),
  // 获取热门文章
  hot: (limit = 10) => frontendApi.get('/articles/hot', { params: { limit } })
}

// 分类
export const categoriesApi = {
  list: () => frontendApi.get('/categories')
}

// 标签
export const tagsApi = {
  list: () => frontendApi.get('/tags')
}

// 友链
export const friendLinksApi = {
  list: () => frontendApi.get('/friend_links')
}
