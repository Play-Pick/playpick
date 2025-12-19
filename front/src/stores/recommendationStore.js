import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import recommendationAPI from '@/api/recommendations'

export const useRecommendationStore = defineStore('recommendation', () => {
  // State
  const recommendations = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const hasRecommendations = computed(() => recommendations.value.length > 0)
  const recommendationCount = computed(() => recommendations.value.length)

  // Actions
  const fetchRecommendations = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await recommendationAPI.getRecommendations(params)
      recommendations.value = response.data.recommendations || response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message

      // 401 (미인증) 또는 404 (추천 없음)는 빈 배열 반환
      if (err.response?.status === 401 || err.response?.status === 404) {
        recommendations.value = []
        error.value = null
      } else {
        throw err
      }
    } finally {
      loading.value = false
    }
  }

  const clearRecommendations = () => {
    recommendations.value = []
    error.value = null
  }

  return {
    // State
    recommendations,
    loading,
    error,
    // Getters
    hasRecommendations,
    recommendationCount,
    // Actions
    fetchRecommendations,
    clearRecommendations
  }
})
