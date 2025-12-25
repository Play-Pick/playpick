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

      // success 여부와 관계없이 data 배열을 설정 (빈 배열도 정상 처리)
      allRankings.value = data.data || []
      // 데이터가 없는 경우는 에러가 아님
    } catch (e) {
      console.error('Error loading all rankings:', e)
      // 네트워크 에러 등 실제 오류만 error로 표시
      if (e.response && e.response.status >= 500) {
        error.value = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      } else if (e.message === 'Network Error' || !e.response) {
        error.value = '네트워크 연결을 확인해주세요.'
      } else {
        error.value = '데이터를 불러오는 중 오류가 발생했습니다.'
      }
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

      // success 여부와 관계없이 data 배열을 설정 (빈 배열도 정상 처리)
      highlightPerformances.value = data.data || []
      // 데이터가 없는 경우는 에러가 아님
    } catch (e) {
      console.error('Error loading highlight performances:', e)
      // 네트워크 에러 등 실제 오류만 error로 표시
      if (e.response && e.response.status >= 500) {
        error.value = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      } else if (e.message === 'Network Error' || !e.response) {
        error.value = '네트워크 연결을 확인해주세요.'
      } else {
        error.value = '데이터를 불러오는 중 오류가 발생했습니다.'
      }
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
