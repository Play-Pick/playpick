import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authAPI from '@/api/auth'
import userAPI from '@/api/users'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value)
  const username = computed(() => user.value?.username)
  const nickname = computed(() => user.value?.nickname || user.value?.username)
  const displayName = computed(() => user.value?.nickname || user.value?.username || '회원')
  const userId = computed(() => user.value?.id)
  const isAdmin = computed(() => user.value?.is_staff || user.value?.is_superuser || false)

  // Actions
  const register = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      // 새 계정 시작 전에 온보딩/웰컴 관련 로컬 상태 초기화
      localStorage.removeItem('onboarding_skipped')
      const response = await authAPI.register(credentials)

      // 토큰 저장
      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)

      // 사용자 정보 저장
      user.value = response.data.user

      // 온보딩 스토어 초기화
      const { useOnboardingStore } = await import('@/stores/onboardingStore')
      useOnboardingStore().reset()

      return response.data
    } catch (err) {
      error.value = err.response?.data || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      // 계정 전환 시 글로벌 스킵 플래그 정리
      localStorage.removeItem('onboarding_skipped')

      // JWT 토큰 발급
      const response = await authAPI.login(credentials)

      // 토큰 저장
      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)

      // 사용자 정보 가져오기
      await fetchCurrentUser()

      // 온보딩 스토어 초기화
      const { useOnboardingStore } = await import('@/stores/onboardingStore')
      useOnboardingStore().reset()

      return response.data
    } catch (err) {
      error.value = err.response?.data || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true

    try {
      await authAPI.logout()

      // 상태 초기화
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('onboarding_skipped')

      // 온보딩 스토어 초기화
      const { useOnboardingStore } = await import('@/stores/onboardingStore')
      useOnboardingStore().reset()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    if (!accessToken.value) return

    try {
      const response = await userAPI.getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('사용자 정보 가져오기 실패:', err)
      // 토큰이 유효하지 않은 경우 로그아웃
      if (err.response?.status === 401) {
        await logout()
      }
    }
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('Refresh token이 없습니다')
    }

    try {
      const response = await authAPI.refreshToken(refreshToken.value)

      accessToken.value = response.data.access
      localStorage.setItem('access_token', response.data.access)

      // refresh token도 갱신된 경우 (ROTATE_REFRESH_TOKENS=True)
      if (response.data.refresh) {
        refreshToken.value = response.data.refresh
        localStorage.setItem('refresh_token', response.data.refresh)
      }

      return response.data.access
    } catch (err) {
      // 토큰 갱신 실패 시 로그아웃
      await logout()
      throw err
    }
  }

  // 초기화 - 앱 로드 시 토큰이 있으면 사용자 정보 가져오기
  const initialize = async () => {
    if (accessToken.value) {
      await fetchCurrentUser()
    }
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    // Getters
    isAuthenticated,
    username,
    nickname,
    displayName,
    userId,
    isAdmin,
    // Actions
    register,
    login,
    logout,
    fetchCurrentUser,
    refreshAccessToken,
    initialize,
  }
})
