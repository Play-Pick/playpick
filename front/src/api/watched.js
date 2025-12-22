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
  /**
   * 관람한 공연 목록 조회
   * GET /api/performances/watched/
   */
  fetchWatched() {
    return apiClient.get('/performances/watched/')
  },

  /**
   * 공연 관람함 추가
   * POST /api/performances/{mt20id}/watch/
   */
  addWatched(performanceId) {
    return apiClient.post(`/performances/${performanceId}/watch/`)
  },

  /**
   * 공연 관람함 해제
   * DELETE /api/performances/{mt20id}/watch/
   */
  removeWatched(performanceId) {
    return apiClient.delete(`/performances/${performanceId}/watch/`)
  },

  normalizeResponse,
}
