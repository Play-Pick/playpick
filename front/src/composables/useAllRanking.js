import { ref } from 'vue'
import performanceApi from '@/api/performances'

// 전역 상태
const allRankings = ref([])
const highlightPerformances = ref([])
const loading = ref(false)
const error = ref(null)

export function useAllRanking() {
  // 전체 랭킹 로드 (Top 10)
  const loadAllRankings = async () => {
    loading.value = true
    error.value = null

    try {
      const { data } = await performanceApi.getBoxOfficeAll()
      if (data.success) {
        allRankings.value = data.data
      } else {
        error.value = '전체 랭킹 데이터를 불러올 수 없습니다.'
      }
    } catch (e) {
      console.error('Error loading all rankings:', e)
      error.value = '오류가 발생했습니다.'
    } finally {
      loading.value = false
    }
  }

  // 하이라이트 캐러셀 데이터 로드 (Top 6~8)
  const loadHighlightPerformances = async () => {
    loading.value = true
    error.value = null

    try {
      const { data } = await performanceApi.getBoxOfficeHighlight()
      if (data.success) {
        highlightPerformances.value = data.data
      } else {
        error.value = '하이라이트 데이터를 불러올 수 없습니다.'
      }
    } catch (e) {
      console.error('Error loading highlight performances:', e)
      error.value = '오류가 발생했습니다.'
    } finally {
      loading.value = false
    }
  }

  return {
    allRankings,
    highlightPerformances,
    loading,
    error,
    loadAllRankings,
    loadHighlightPerformances
  }
}
