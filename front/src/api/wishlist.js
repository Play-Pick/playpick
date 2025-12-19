import apiClient from './axios'

const normalizeResponse = (response) => {
  if (!response) return []
  if (Array.isArray(response)) return response
  if (Array.isArray(response.data)) return response.data
  if (Array.isArray(response.data?.results)) return response.data.results
  if (Array.isArray(response.data?.data)) return response.data.data
  return []
}

export default {
  fetchWishlist() {
    return apiClient.get('/wishlist/')
  },
  removeWishlist(performanceId) {
    return apiClient.delete(`/wishlist/${performanceId}/`)
  },
  toggleWishlist(performanceId) {
    return apiClient.post(`/wishlist/${performanceId}/`)
  },
  normalizeResponse,
}
