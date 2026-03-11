/**
 * Admin Router - 后台管理路由
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useAdminStore } from '@/stores/admin'

const routes = [
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue'),
    meta: { title: '管理员登录', public: true }
  },
  {
    path: '/admin',
    component: () => import('../views/admin/Layout.vue'),
    redirect: '/admin/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/admin/Dashboard.vue'),
        meta: { title: '仪表盘', requiresAuth: true }
      },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('../views/admin/Articles.vue'),
        meta: { title: '文章管理', requiresAuth: true }
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('../views/admin/Categories.vue'),
        meta: { title: '分类管理', requiresAuth: true }
      },
      {
        path: 'comments',
        name: 'Comments',
        component: () => import('../views/admin/Comments.vue'),
        meta: { title: '评论管理', requiresAuth: true }
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('../views/admin/Tags.vue'),
        meta: { title: '标签管理', requiresAuth: true }
      },
      {
        path: 'friend-links',
        name: 'FriendLinks',
        component: () => import('../views/admin/FriendLinks.vue'),
        meta: { title: '友链管理', requiresAuth: true }
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('../views/admin/Messages.vue'),
        meta: { title: '留言管理', requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const adminStore = useAdminStore()

  // 设置页面标题
  document.title = `${to.meta.title || '后台管理'} | MoZhi Blog`

  // 公开页面直接通过（登录页）
  if (to.meta.public) {
    // 如果已登录且访问登录页，重定向到后台首页
    if (to.path === '/admin/login' && adminStore.token) {
      return next('/admin/dashboard')
    }
    return next()
  }

  // 需要登录的页面（所有 /admin 下的页面，除了登录页）
  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    if (!adminStore.token) {
      return next('/admin/login')
    }

    // 如果没有管理员信息，先获取
    if (!adminStore.adminInfo) {
      try {
        await adminStore.getInfo()
      } catch (error) {
        return next('/admin/login')
      }
    }
  }

  next()
})

export default router
