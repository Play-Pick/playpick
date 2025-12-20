import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingView,
    },
    {
      path: '/performances',
      name: 'performances',
      component: () => import('@/views/PerformanceListView.vue'),
    },
    {
      path: '/performances/:id',
      name: 'performance-detail',
      component: () => import('@/views/PerformanceDetailView.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/CommunityView.vue'),
    },
    {
      path: '/community/write',
      name: 'community-write',
      component: () => import('@/views/CommunityWriteView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/community/:id',
      name: 'article-detail',
      component: () => import('@/views/ArticleDetailView.vue'),
    },
    {
      path: '/test-api',
      name: 'test-api',
      component: () => import('@/views/TestAPIView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('@/views/MyPageView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/AdminDashboardView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/rankings',
      name: 'rankings',
      component: () => import('@/views/RankingsView.vue'),
    },
    {
      path: '/rankings/all',
      name: 'ranking-all',
      component: () => import('@/views/RankingAllView.vue'),
    },
    {
      path: '/rankings/genre',
      name: 'ranking-genre',
      component: () => import('@/views/RankingGenreView.vue'),
    },
    {
      path: '/recommands',
      name: 'recommands',
      component: () => import('@/views/RecommandsView.vue'),
    },
  ],
})

// 인증이 필요한 라우트 보호
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
