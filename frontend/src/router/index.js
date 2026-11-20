import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  { path: '/books', name: 'BookList', component: () => import('../views/BookList.vue') },
  { path: '/books/:id', name: 'BookDetail', component: () => import('../views/BookDetail.vue') },
  { path: '/publish', name: 'PublishBook', component: () => import('../views/PublishBook.vue'), meta: { requireAuth: true } },
  { path: '/user', name: 'UserCenter', component: () => import('../views/UserCenter.vue'), meta: { requireAuth: true } },
  { path: '/messages', name: 'Messages', component: () => import('../views/Messages.vue'), meta: { requireAuth: true } },
  { path: '/wantbuy', name: 'WantBuy', component: () => import('../views/WantBuy.vue') },
  { path: '/admin', name: 'Admin', component: () => import('../views/Admin.vue'), meta: { requireAuth: true, requireAdmin: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  }
})

// 路由守卫 - 登录验证
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requireAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.requireAdmin && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
