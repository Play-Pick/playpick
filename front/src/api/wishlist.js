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
    // 백엔드: GET /api/performances/liked/
    return apiClient.get('/performances/liked/')
  },
  removeWishlist(performanceId) {
    // 백엔드: POST /api/performances/{mt20id}/like/ 토글 방식
    return apiClient.post(`/performances/${performanceId}/like/`)
  },
  toggleWishlist(performanceId) {
    // 동일 토글 엔드포인트 사용
    return apiClient.post(`/performances/${performanceId}/like/`)
  },
  normalizeResponse,
}
