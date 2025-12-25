import axios from 'axios'

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // CORS 인증 정보 포함
})

// 요청 인터셉터 - JWT 토큰 자동 추가
apiClient.interceptors.request.use(
  (config) => {
    // localStorage에서 access_token 가져오기
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터 - 토큰 만료 시 자동 갱신
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // 401 에러이고, 재시도하지 않은 요청인 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')

        if (refreshToken) {
          // 토큰 갱신 요청
          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/accounts/token/refresh/`,
            { refresh: refreshToken }
          )

          const { access } = response.data

          // 새 토큰 저장
          localStorage.setItem('access_token', access)

          // 원래 요청에 새 토큰 적용
          originalRequest.headers.Authorization = `Bearer ${access}`

          // 원래 요청 재시도
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // 토큰 갱신 실패 시 로그아웃 처리
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        // 로그인 페이지로 리다이렉트 (필요시)
        // window.location.href = '/login'

        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
