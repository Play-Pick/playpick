import { defineStore } from 'pinia'
import { ref } from 'vue'
import wishlistAPI from '@/api/wishlist'

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
    is_liked: source?.is_liked ?? true
  }
}

const normalizeWishlist = (payload) => {
  const list = wishlistAPI.normalizeResponse(payload)
  return list.map(normalizePerformance)
}

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref([])
  const loading = ref(false)
  const errorMessage = ref('')

  const fetchWishlist = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
      const response = await wishlistAPI.fetchWishlist()
      items.value = normalizeWishlist(response)
      return items.value
    } catch (err) {
      const status = err?.response?.status
      if (status === 401 || status === 404) {
        items.value = []
        return items.value
      }
      errorMessage.value = err?.response?.data?.detail || err?.message || '찜 목록을 불러오지 못했습니다.'
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeFromWishlist = async (performanceId) => {
    errorMessage.value = ''
    try {
      await wishlistAPI.removeWishlist(performanceId)
    } catch (err) {
      if (err?.response?.status === 405) {
        await wishlistAPI.toggleWishlist(performanceId)
      } else {
        const status = err?.response?.status
        if (status === 401 || status === 404) {
          items.value = []
          return
        }
        errorMessage.value = err?.response?.data?.detail || err?.message || '찜 해제에 실패했습니다.'
        throw err
      }
    }

    const targetId = String(performanceId)
    items.value = items.value.filter((item) => {
      const itemId = String(item.mt20id || item.id || '')
      return itemId !== targetId
    })
  }

  return {
    items,
    loading,
    errorMessage,
    fetchWishlist,
    removeFromWishlist
  }
})
