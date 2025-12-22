import apiClient from './axios'

const RESOURCE = 'accounts/users'

export default {
  // 사용자 목록 조회
  getUsers() {
    return apiClient.get(`${RESOURCE}/`)
  },

  // 사용자 상세 조회
  getUser(id) {
    return apiClient.get(`${RESOURCE}/${id}/`)
  },

  // 현재 로그인한 사용자 정보
  getCurrentUser() {
    return apiClient.get(`${RESOURCE}/me/`)
  }
}
