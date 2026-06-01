import apiClient from './axios'

export default {
  // 데이터 통계 조회
  getStats() {
    return apiClient.get('/performances/management/stats/')
  },

  // 박스오피스 수집
  collectBoxOffice(params = {}) {
    return apiClient.post('/performances/management/collect-boxoffice/', params, {
      timeout: 300000 // 5분
    })
  },

  // 공연 목록 수집
  collectPerformances(params = {}) {
    return apiClient.post('/performances/management/collect-performances/', params, {
      timeout: 300000 // 5분
    })
  },

  // 공연 상세 정보 수집
  collectDetails(params = {}) {
    return apiClient.post('/performances/management/collect-details/', params, {
      timeout: 300000 // 5분
    })
  },

  // 테스트 박스오피스 생성
  createTestBoxOffice() {
    return apiClient.post('/performances/management/create-test-boxoffice/')
  }
}
