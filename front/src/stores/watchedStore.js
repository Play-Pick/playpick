import { defineStore } from 'pinia'
import { ref } from 'vue'
import watchedAPI from '@/api/watched'

const normalizePerformance = (item) => {
  const source = item?.performance || item
  const mt20id = source?.mt20id || source?.id || source?.performance_id
  return {
    ...source,
    mt20id,
    prfnm: source?.prfnm || source?.title || source?.name || source?.performance_name,
    poster: source?.poster || source?.poster_url || source?.image,
    fcltynm: source?.fcltynm || source?.venue || source?.place,
    prfpdfrom: source?.prfpdfrom || source?.start_date || source?.startDate,
    prfpdto: source?.prfpdto || source?.end_date || source?.endDate,
    genrenm: source?.genrenm || source?.genre,
    is_watched: source?.is_watched ?? true
  }
}

const normalizeWatched = (payload) => {
  const list = watchedAPI.normalizeResponse(payload)
  return list.map(normalizePerformance)
}

export const useWatchedStore = defineStore('watched', () => {
  const items = ref([])
  const loading = ref(false)
  const errorMessage = ref('')

  const fetchWatched = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
      const response = await watchedAPI.fetchWatched()
      items.value = normalizeWatched(response)
      return items.value
    } catch (err) {
      const status = err?.response?.status
      if (status === 401 || status === 404) {
        items.value = []
        return items.value
      }
      errorMessage.value = err?.response?.data?.detail || err?.message || '관람한 공연 목록을 불러오지 못했어요.'
      throw err
    } finally {
      loading.value = false
    }
  }

  const addToWatched = async (performanceId) => {
    errorMessage.value = ''
    try {
      await watchedAPI.addWatched(performanceId)
      // 낙관적 업데이트: 전체 목록을 다시 불러오지 않고 클라이언트에서 추가
      // 실제 데이터는 fetchWatched() 호출 시 서버에서 받아옴
      return true
    } catch (err) {
      const status = err?.response?.status
      if (status === 401 || status === 404) {
        return false
      }
      errorMessage.value = err?.response?.data?.detail || err?.message || '관람함 추가에 실패했습니다.'
      throw err
    }
  }

  const removeFromWatched = async (performanceId) => {
    errorMessage.value = ''
    try {
      await watchedAPI.removeWatched(performanceId)
    } catch (err) {
      const status = err?.response?.status
      if (status === 401 || status === 404) {
        items.value = []
        return
      }
      errorMessage.value = err?.response?.data?.detail || err?.message || '관람함 삭제에 실패했습니다.'
      throw err
    }

    // 로컬 상태에서 제거
    const targetId = String(performanceId)
    items.value = items.value.filter((item) => {
      const itemId = String(item.mt20id || item.id || '')
      return itemId !== targetId
    })
  }

  const isWatched = (performanceId) => {
    const targetId = String(performanceId)
    return items.value.some((item) => {
      const itemId = String(item.mt20id || item.id || '')
      return itemId === targetId
    })
  }

  return {
    items,
    loading,
    errorMessage,
    fetchWatched,
    addToWatched,
    removeFromWatched,
    isWatched
  }
})
