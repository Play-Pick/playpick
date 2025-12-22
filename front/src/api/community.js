import apiClient from './axios'

export default {
  // 게시글 목록 조회
  getArticles(params) {
    return apiClient.get('/community/articles/', { params })
  },

  // 게시글 상세 조회
  getArticle(id) {
    return apiClient.get(`/community/articles/${id}/`)
  },

  // 게시글 생성
  createArticle(data) {
    return apiClient.post('/community/articles/', data)
  },

  // 게시글 수정
  updateArticle(id, data) {
    return apiClient.put(`/community/articles/${id}/`, data)
  },

  // 게시글 삭제
  deleteArticle(id) {
    return apiClient.delete(`/community/articles/${id}/`)
  },

  // 게시글 좋아요 토글
  likeArticle(id) {
    return apiClient.post(`/community/articles/${id}/like/`)
  },

  // 베스트 관람후기 조회
  getBestReviews(limit = 4) {
    return apiClient.get('/community/articles/best-reviews/', {
      params: { limit }
    })
  },

  // 댓글 목록 조회
  getComments(articleId) {
    if (articleId) {
      return apiClient.get('/community/comments/', {
        params: { article: articleId }
      })
    }
    // articleId가 없으면 전체 댓글 조회
    return apiClient.get('/community/comments/')
  },

  // 댓글 생성
  createComment(data) {
    return apiClient.post('/community/comments/', data)
  },

  // 댓글 수정
  updateComment(id, data) {
    return apiClient.patch(`/community/comments/${id}/`, data)
  },

  // 댓글 삭제
  deleteComment(id) {
    return apiClient.delete(`/community/comments/${id}/`)
  },

  // 하위 호환성을 위한 별칭 (기존 코드가 있을 경우)
  getReviews(params) {
    return this.getArticles(params)
  },
  getReview(id) {
    return this.getArticle(id)
  },
  createReview(data) {
    return this.createArticle(data)
  },
  updateReview(id, data) {
    return this.updateArticle(id, data)
  },
  deleteReview(id) {
    return this.deleteArticle(id)
  },
  likeReview(id) {
    return this.likeArticle(id)
  }
}
