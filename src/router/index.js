/**
 * Vue Router Configuration
 * 路由配置 - 包含页面切换动效
 */
import { createRouter, createWebHistory } from 'vue-router'

// 导入后台路由
import adminRouter from './admin'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/article/:id',
    name: 'Article',
    component: () => import('../views/ArticlePage.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/category',
    name: 'Category',
    component: () => import('../views/CategoryPage.vue'),
    meta: { title: '分类' }
  },
  {
    path: '/tag',
    name: 'Tag',
    component: () => import('../views/TagPage.vue'),
    meta: { title: '标签' }
  },
  {
    path: '/archive',
    name: 'Archive',
    component: () => import('../views/ArchivePage.vue'),
    meta: { title: '归档' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutPage.vue'),
    meta: { title: '关于' }
  },
  {
    path: '/links',
    name: 'Links',
    component: () => import('../views/LinksPage.vue'),
    meta: { title: '友链' }
  },
  {
    path: '/message',
    name: 'Message',
    component: () => import('../views/MessagePage.vue'),
    meta: { title: '留言板' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundPage.vue'),
    meta: { title: '404' }
  }
]

// 合并路由
const allRoutes = [...routes, ...adminRouter.options.routes]

const router = createRouter({
  history: createWebHistory(),
  routes: allRoutes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      // 平滑滚动到锚点
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 80 // 留出导航栏空间
      }
    } else {
      // 路由切换时回到顶部
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '首页'} | MoZhi Blog`
  next()
})

export default router
