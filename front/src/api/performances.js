import apiClient from './axios'

export default {
  // 공연 목록 조회
  getPerformances(params) {
    return apiClient.get('/performances/', { params })
  },

  // 공연 상세 조회
  getPerformance(id) {
    return apiClient.get(`/performances/${id}/`)
  },

  // 장르 목록 조회
  getGenres() {
    return apiClient.get('/performances/genres/')
  },

  // 박스오피스 랭킹 조회
  getBoxOffice(params) {
    return apiClient.get('/boxoffice/', { params })
  },

  // 장르별 최신 박스오피스
  getLatestBoxOfficeByGenre(genreCode) {
    return apiClient.get('/boxoffice/latest_by_genre/', {
      params: { genre_code: genreCode }
    })
  },

  // 장르별 박스오피스 (LandingView용)
  getBoxOfficeByGenre(genre) {
    return apiClient.get('/performances/boxoffice-genre/', {
      params: { genre }
    })
  },

  // 전체 박스오피스 랭킹 (좌석수 기준 Top 10)
  getBoxOfficeAll() {
    return apiClient.get('/performances/boxoffice-all/')
  },

  // 하이라이트 캐러셀용 박스오피스 (Top 6~8)
  getBoxOfficeHighlight() {
    return apiClient.get('/performances/boxoffice-highlight/')
  },

  // 공연 찜하기/취소 토글
  toggleLike(performanceId) {
    return apiClient.post(`/performances/${performanceId}/like/`)
  }
}
