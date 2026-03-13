/**
 * Admin Router - 后台管理路由
 */
import { createRouter, createWebHistory } from 'vue-router'

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
        path: 'articles/new',
        name: 'ArticleNew',
        component: () => import('../views/admin/ArticleEditor.vue'),
        meta: { title: '新增文章', requiresAuth: true }
      },
      {
        path: 'articles/:id/edit',
        name: 'ArticleEdit',
        component: () => import('../views/admin/ArticleEditor.vue'),
        meta: { title: '编辑文章', requiresAuth: true }
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
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/admin/Settings.vue'),
        meta: { title: '设置', requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
