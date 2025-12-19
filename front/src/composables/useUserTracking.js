import { ref } from 'vue'
import recommendationAPI from '@/api/recommendations'
import performanceAPI from '@/api/performances'
import { useAuthStore } from '@/stores/authStore'

export function useUserTracking() {
  const authStore = useAuthStore()
  const loading = ref(false)
  const error = ref(null)
  const likeLoading = ref(false)

  /**
   * 사용자 행동 로깅 (범용 함수)
   * @param {string} actionType - 'view', 'like', 'review'
   * @param {string} performanceId - 공연 ID
   * @param {object} additionalData - 추가 데이터 (rating 등)
   */
  const logAction = async (actionType, performanceId, additionalData = {}) => {
    // 인증되지 않은 사용자는 로그 전송 안 함
    if (!authStore.isAuthenticated) {
      return
    }

    loading.value = true
    error.value = null

    try {
      await recommendationAPI.logAction({
        action_type: actionType,
        performance_id: performanceId,
        ...additionalData
      })
    } catch (err) {
      // 로깅 실패는 사용자 경험에 영향 없음 (조용히 실패)
      console.warn('User tracking error:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  /**
   * 공연 조회 로그
   */
  const logView = (performanceId) => {
    return logAction('view', performanceId)
  }

  /**
   * 찜하기 토글 (실제 찜하기 + 로그 저장)
   * @param {string} performanceId - 공연 ID
   * @returns {Promise<{is_liked: boolean, like_count: number}>}
   */
  const toggleLike = async (performanceId) => {
    if (!authStore.isAuthenticated) {
      throw new Error('로그인이 필요합니다.')
    }

    likeLoading.value = true
    error.value = null

    try {
      // 찜하기 API 호출 (백엔드에서 자동으로 로그 저장)
      const response = await performanceAPI.toggleLike(performanceId)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      likeLoading.value = false
    }
  }

  /**
   * 리뷰 작성 로그
   */
  const logReview = (performanceId, rating) => {
    return logAction('review', performanceId, { rating })
  }

  return {
    loading,
    error,
    likeLoading,
    logAction,
    logView,
    toggleLike,
    logReview
  }
}
