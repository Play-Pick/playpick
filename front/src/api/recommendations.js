import apiClient from './axios'

export default {
  // 개인화 추천 목록 조회
  getRecommendations(params = {}) {
    return apiClient.get('/recommendations/', { params })
  },

  // 사용자 행동 로깅
  logAction(data) {
    return apiClient.post('/recommendations/log/', data)
  }
}
