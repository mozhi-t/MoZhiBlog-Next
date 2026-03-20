/**
 * Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'
import adminRouter from './admin'
import { useAdminStore } from '@/stores/admin'
import { updateSeo } from '@/utils/seo'

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
    path: '/space',
    name: 'Space',
    component: () => import('../views/SpacePage.vue'),
    meta: { title: '空间' }
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
    path: '/search',
    name: 'Search',
    component: () => import('../views/SearchPage.vue'),
    meta: { title: '搜索' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundPage.vue'),
    meta: { title: '404' }
  }
]

const allRoutes = [...routes, ...adminRouter.options.routes]

const router = createRouter({
  history: createWebHistory(),
  routes: allRoutes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 80
      }
    }

    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach(async (to, from, next) => {
  const adminStore = useAdminStore()

  updateSeo({
    title: to.meta.title || '首页',
    path: to.fullPath,
    noindex: to.path.startsWith('/admin')
  })

  if (to.meta.public) {
    if (to.path === '/admin/login' && adminStore.token) {
      return next('/admin/dashboard')
    }
    return next()
  }

  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    if (!adminStore.token) {
      return next('/admin/login')
    }

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
