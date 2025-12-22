import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    // savedPosition이 있으면 (브라우저 뒤로가기) 해당 위치로
    if (savedPosition) {
      return savedPosition
    }
    // 앵커가 있으면 해당 앵커로
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    // 기본적으로 최상단으로
    return { top: 0, behavior: 'smooth' }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingView,
    },
    {
      path: '/performances',
      name: 'performances',
      component: () => import('@/views/Performance/PerformanceListView.vue'),
    },
    {
      path: '/performances/:id',
      name: 'performance-detail',
      component: () => import('@/views/Performance/PerformanceDetailView.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/Community/CommunityView.vue'),
    },
    {
      path: '/community/best',
      name: 'community-best',
      component: () => import('@/views/Community/CommunityBestView.vue'),
    },
    {
      path: '/community/write',
      name: 'community-write',
      component: () => import('@/views/Community/CommunityWriteView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/community/:id',
      name: 'article-detail',
      component: () => import('@/views/Community/ArticleDetailView.vue'),
    },
    {
      path: '/community/:id/edit',
      name: 'article-edit',
      component: () => import('@/views/Community/EditArticleView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/test-api',
      name: 'test-api',
      component: () => import('@/views/TestAPIView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Auth/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Auth/RegisterView.vue'),
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: () => import('@/views/Auth/OnboardingView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('@/views/User/MyPageView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/edit-account',
      name: 'edit-account',
      component: () => import('@/views/User/EditAccountView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/Admin/AdminDashboardView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/rankings',
      name: 'rankings',
      component: () => import('@/views/Ranking/RankingsView.vue'),
    },
    {
      path: '/rankings/all',
      name: 'ranking-all',
      component: () => import('@/views/Ranking/RankingAllView.vue'),
    },
    {
      path: '/rankings/genre',
      name: 'ranking-genre',
      component: () => import('@/views/Ranking/RankingGenreView.vue'),
    },
    {
      path: '/recommands',
      name: 'recommands',
      component: () => import('@/views/RecommandsView.vue'),
    },
  ],
})

// 인증이 필요한 라우트 보호
router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/authStore')
  const authStore = useAuthStore()

  // Initialize auth if needed
  if (!authStore.isInitialized) {
    await authStore.initialize()
  }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = authStore.isAuthenticated
  // Skip flag is user-scoped to avoid leaking between accounts
  const skipKey = authStore.userId ? `onboarding_skipped_${authStore.userId}` : null
  const skippedOnboarding = skipKey ? localStorage.getItem(skipKey) === '1' : false

  if (requiresAuth && !isAuthenticated) {
    // Not logged in, redirect to login
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (isAuthenticated && !authStore.user?.has_onboarded && !skippedOnboarding && to.name !== 'onboarding') {
    // Logged in but not onboarded, force onboarding
    next({ name: 'onboarding' })
  } else if (to.name === 'onboarding' && (authStore.user?.has_onboarded || skippedOnboarding)) {
    // Already onboarded, redirect to home
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
