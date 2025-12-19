import apiClient from './axios'

export default {
  // 게시글 목록 조회
  getArticles(params) {
    return apiClient.get('/articles/', { params })
  },

  // 게시글 상세 조회
  getArticle(id) {
    return apiClient.get(`/articles/${id}/`)
  },

  // 게시글 생성
  createArticle(data) {
    return apiClient.post('/articles/', data)
  },

  // 게시글 수정
  updateArticle(id, data) {
    return apiClient.put(`/articles/${id}/`, data)
  },

  // 게시글 삭제
  deleteArticle(id) {
    return apiClient.delete(`/articles/${id}/`)
  },

  // 게시글 좋아요 토글
  likeArticle(id) {
    return apiClient.post(`/articles/${id}/like/`)
  },

  // 댓글 목록 조회
  getComments(articleId) {
    return apiClient.get('/comments/', {
      params: { article: articleId }
    })
  },

  // 댓글 생성
  createComment(data) {
    return apiClient.post('/comments/', data)
  },

  // 댓글 삭제
  deleteComment(id) {
    return apiClient.delete(`/comments/${id}/`)
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
