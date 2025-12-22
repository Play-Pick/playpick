import apiClient from './axios'

export default {
  // 회원가입
  register(data) {
    return apiClient.post('/accounts/register/', data)
  },

  // 로그인 (JWT 토큰 발급)
  login(credentials) {
    return apiClient.post('/accounts/token/', credentials)
  },

  // 토큰 갱신
  refreshToken(refresh) {
    return apiClient.post('/accounts/token/refresh/', { refresh })
  },

  // 로그아웃 (클라이언트 측에서 토큰 삭제)
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    return Promise.resolve()
  }
}
