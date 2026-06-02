import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/DirectLogin.vue'
import Dashboard from '../views/Dashboard.vue'
import FileManagement from '../views/FileManagement.vue'
import AIAnalysis from '../views/AIAnalysis.vue'
import UserManagement from '../views/UserManagement.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/files',
    name: 'FileManagement',
    component: FileManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/ai-analysis',
    name: 'AIAnalysis',
    component: AIAnalysis,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
    
    if (to.meta.requiresAdmin) {
      const role = localStorage.getItem('role')
      if (role !== 'admin') {
        next('/')
        return
      }
    }
  }
  next()
})

export default router
