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
  },

  // 현재 사용자 정보 조회
  getCurrentUser() {
    return apiClient.get('/accounts/users/me/')
  },

  // 회원정보 수정
  updateProfile(data) {
    return apiClient.patch('/users/update_profile/', data)
  },

  // 회원 탈퇴
  deleteAccount(password) {
    return apiClient.delete('/users/delete_account/', {
      data: { password }
    })
  },

  // 비밀번호 확인
  verifyPassword(password) {
    return apiClient.post('/accounts/users/verify_password/', { password })
  }
}
