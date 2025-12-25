import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import performanceAPI from '@/api/performances'
import { useAuthStore } from './authStore'

export const usePerformanceStore = defineStore('performance', () => {
  // State
  const performances = ref([])
  const currentPerformance = ref(null)
  const genres = ref([])
  const boxOfficeRankings = ref([])
  const loading = ref(false)
  const error = ref(null)
  const likeLoading = ref(false)

  // Getters
  const performanceCount = computed(() => performances.value.length)

  // Actions
  const fetchPerformances = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getPerformances(params)
      performances.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchPerformance = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getPerformance(id)
      currentPerformance.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchGenres = async () => {
    try {
      const response = await performanceAPI.getGenres()
      genres.value = response.data.genres
      return response.data.genres
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const fetchBoxOffice = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getBoxOffice(params)
      boxOfficeRankings.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchLatestBoxOfficeByGenre = async (genreCode) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getLatestBoxOfficeByGenre(genreCode)
      boxOfficeRankings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 좋아요 토글 (전역 상태 관리)
   * @param {string} performanceId - 공연 ID
   * @returns {Promise<{is_liked: boolean, like_count: number}>}
   */
  const toggleLike = async (performanceId) => {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      throw new Error('로그인이 필요합니다.')
    }

    likeLoading.value = true
    error.value = null

    try {
      const response = await performanceAPI.toggleLike(performanceId)
      const { is_liked, like_count } = response.data

      // 모든 공연 목록에서 해당 공연의 좋아요 상태 업데이트
      updateLikeStatus(performanceId, is_liked, like_count)

      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      likeLoading.value = false
    }
  }

  /**
   * 공연 ID로 모든 목록의 좋아요 상태 업데이트
   * @private
   */
  const updateLikeStatus = (performanceId, isLiked, likeCount) => {
    // 헬퍼 함수: 배열의 공연 데이터 업데이트
    const updateArray = (arr) => {
      const index = arr.findIndex(item => {
        // 직접 mt20id를 가진 경우
        if (item.mt20id === performanceId) return true
        // performance 객체 안에 있는 경우
        if (item.performance?.mt20id === performanceId) return true
        return false
      })

      if (index !== -1) {
        const item = arr[index]
        if (item.performance) {
          item.performance.is_liked = isLiked
          item.performance.like_count = likeCount
        } else {
          item.is_liked = isLiked
          item.like_count = likeCount
        }
        return true
      }
      return false
    }

    // 1. performances 배열 업데이트
    updateArray(performances.value)

    // 2. boxOfficeRankings 배열 업데이트
    updateArray(boxOfficeRankings.value)

    // 3. currentPerformance 업데이트
    if (currentPerformance.value?.mt20id === performanceId) {
      currentPerformance.value.is_liked = isLiked
      currentPerformance.value.like_count = likeCount
    }

    // 4. useAllRanking composable의 allRankings 업데이트
    // 동적으로 import하여 상태 업데이트
    import('@/composables/useAllRanking').then(module => {
      const { allRankings, highlightPerformances } = module.useAllRanking()
      updateArray(allRankings.value)
      updateArray(highlightPerformances.value)
    })

    // 5. useBoxOffice composable의 allPerformances 업데이트
    import('@/composables/useBoxOffice').then(module => {
      const { allPerformances } = module.useBoxOffice()
      updateArray(allPerformances.value)
    })

    // 6. aiSearchStore의 searchResults 업데이트
    import('@/stores/aiSearchStore').then(module => {
      const aiSearchStore = module.useAISearchStore()
      updateArray(aiSearchStore.searchResults)
    })

    // 7. wishlistStore의 items 업데이트
    import('@/stores/wishlistStore').then(module => {
      const wishlistStore = module.useWishlistStore()
      updateArray(wishlistStore.items)
    })

    // 8. watchedStore의 items 업데이트
    import('@/stores/watchedStore').then(module => {
      const watchedStore = module.useWatchedStore()
      updateArray(watchedStore.items)
    })
  }

  return {
    // State
    performances,
    currentPerformance,
    genres,
    boxOfficeRankings,
    loading,
    error,
    likeLoading,
    // Getters
    performanceCount,
    // Actions
    fetchPerformances,
    fetchPerformance,
    fetchGenres,
    fetchBoxOffice,
    fetchLatestBoxOfficeByGenre,
    toggleLike
  }
})
