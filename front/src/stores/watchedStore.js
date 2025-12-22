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

  const addToWatched = async (performanceId, performanceData = null) => {
    errorMessage.value = ''
    try {
      await watchedAPI.addWatched(performanceId)

      // 프론트에서 공연 데이터를 받아 items에 추가 (실시간 동기화)
      if (performanceData) {
        const newItem = normalizePerformance(performanceData)

        // 이미 존재하지 않는 경우에만 추가
        const targetId = String(performanceId)
        const exists = items.value.some((item) => {
          const itemId = String(item.mt20id || item.id || '')
          return itemId === targetId
        })

        if (!exists) {
          items.value.unshift(newItem) // 최신 항목을 앞에 추가
        }
      }

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

    // 로컬 상태에서 먼저 제거 (낙관적 업데이트)
    const targetId = String(performanceId)
    const previousItems = [...items.value]
    items.value = items.value.filter((item) => {
      const itemId = String(item.mt20id || item.id || '')
      return itemId !== targetId
    })

    try {
      await watchedAPI.removeWatched(performanceId)
    } catch (err) {
      const status = err?.response?.status
      if (status === 401 || status === 404) {
        items.value = []
        return
      }

      // API 호출 실패 시 이전 상태로 롤백
      items.value = previousItems

      errorMessage.value = err?.response?.data?.detail || err?.message || '관람함 삭제에 실패했습니다.'
      throw err
    }
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
