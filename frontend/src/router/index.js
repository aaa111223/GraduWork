import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainLayout from '@/components/Layout/MainLayout.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ??????
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/test-login',
      name: 'test-login',
      component: () => import('../components/TestLogin.vue')
    },

    // ???????��??��????
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: '/my-employment',
          name: 'my-employment',
          component: () => import('../views/MyEmploymentView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/job-market',
          name: 'job-market',
          component: () => import('../views/JobMarketView.vue'),
        },
        {
          path: '/applications',
          name: 'applications',
          component: () => import('../views/ApplicationsView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/system-management',
          name: 'system-management',
          component: () => import('../views/SystemManagementView.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
          path: '/profile',
          name: 'profile',
          component: () => import('../views/ProfileView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/feedback',
          name: 'feedback',
          component: () => import('../views/FeedbackView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/test',
          name: 'test',
          component: () => import('@/views/TestView.vue')
        }
      ]
    }
  ],
})

// ��??????
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // ????????????
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // ?????????????????
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next({ name: 'home' })
    return
  }

  // ?????????????????????????????????????��
  if (to.meta.requiresGuest && userStore.isLoggedIn) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
