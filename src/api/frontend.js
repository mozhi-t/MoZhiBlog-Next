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
  detail: (id) => frontendApi.get(`/articles/${id}`),
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

// 评论
export const commentsApi = {
  list: (articleId) => frontendApi.get(`/comments/${articleId}`),
  create: (data) => frontendApi.post('/comments', data)
}

// 留言板
export const messageBoardApi = {
  list: () => frontendApi.get('/messages'),
  create: (data) => frontendApi.post('/messages', data)
}
