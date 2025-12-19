import apiClient from './axios'

export default {
  // 사용자 목록 조회
  getUsers() {
    return apiClient.get('/users/')
  },

  // 사용자 상세 조회
  getUser(id) {
    return apiClient.get(`/users/${id}/`)
  },

  // 현재 로그인한 사용자 정보
  getCurrentUser() {
    return apiClient.get('/users/me/')
  },

  // 팔로우/언팔로우 토글
  followUser(id) {
    return apiClient.post(`/users/${id}/follow/`)
  }
}
