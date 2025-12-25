import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import communityAPI from '@/api/community'
import { useAuthStore } from './authStore'

export const useCommunityStore = defineStore('community', () => {
  // State
  const articles = ref([])
  const currentArticle = ref(null)
  const comments = ref([])
  const loading = ref(false)
  const error = ref(null)
  const likeLoading = ref(false)

  // Filter state
  const filters = ref({
    board_type: null,      // 'PERFORMANCE' or 'GENERAL'
    category: null,        // REVIEW, EXPECTATION, QNA, FREE, INFO
    performance_mt20id: null,
    search: '',
    ordering: '-created_at'  // -created_at, created_at, -like_count, like_count
  })

  // Best reviews state
  const bestReviews = ref([])
  const bestLoading = ref(false)

  // Getters
  const articleCount = computed(() => articles.value.length)

  // Actions
  const fetchArticles = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await communityAPI.getArticles(params)
      articles.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchArticle = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await communityAPI.getArticle(id)
      currentArticle.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createArticle = async (data) => {
    loading.value = true
    error.value = null
    try {
      const response = await communityAPI.createArticle(data)
      articles.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateArticle = async (id, data) => {
    loading.value = true
    error.value = null
    try {
      const response = await communityAPI.updateArticle(id, data)
      const index = articles.value.findIndex(r => r.id === id)
      if (index !== -1) {
        articles.value[index] = response.data
      }
      if (currentArticle.value?.id === id) {
        currentArticle.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteArticle = async (id) => {
    loading.value = true
    error.value = null
    try {
      await communityAPI.deleteArticle(id)
      articles.value = articles.value.filter(r => r.id !== id)
      if (currentArticle.value?.id === id) {
        currentArticle.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const likeArticle = async (id) => {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      throw new Error('로그인이 필요합니다.')
    }

    likeLoading.value = true
    try {
      const response = await communityAPI.likeArticle(id)
      const { is_liked, like_count } = response.data

      // 모든 위치의 좋아요 상태 업데이트
      updateLikeStatus(id, is_liked, like_count)

      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      likeLoading.value = false
    }
  }

  /**
   * 게시글 ID로 모든 목록의 좋아요 상태 업데이트
   * @private
   */
  const updateLikeStatus = (articleId, isLiked, likeCount) => {
    // ID를 숫자로 변환 (문자열과 숫자 비교 문제 해결)
    const numericId = typeof articleId === 'string' ? parseInt(articleId) : articleId

    // 1. articles 배열 업데이트
    const articleIndex = articles.value.findIndex(a => a.id == numericId)
    if (articleIndex !== -1) {
      articles.value[articleIndex].is_liked = isLiked
      articles.value[articleIndex].like_count = likeCount
    }

    // 2. currentArticle 업데이트
    if (currentArticle.value && currentArticle.value.id == numericId) {
      currentArticle.value.is_liked = isLiked
      currentArticle.value.like_count = likeCount
    }
  }

  const fetchComments = async (articleId) => {
    try {
      const response = await communityAPI.getComments(articleId)
      // pagination 응답인 경우 results 추출, 아니면 배열로 변환
      if (response.data.results) {
        comments.value = response.data.results
      } else if (Array.isArray(response.data)) {
        comments.value = response.data
      } else {
        comments.value = []
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const createComment = async (data) => {
    try {
      const response = await communityAPI.createComment(data)
      // comments가 배열인지 확인 후 push
      if (Array.isArray(comments.value)) {
        comments.value.push(response.data)
      } else {
        comments.value = [response.data]
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateComment = async (id, data) => {
    try {
      const response = await communityAPI.updateComment(id, data)
      comments.value = comments.value.map(c => (c.id === id ? response.data : c))
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const deleteComment = async (id) => {
    try {
      await communityAPI.deleteComment(id)
      comments.value = comments.value.filter(c => c.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  // Filter actions
  const setFilter = (key, value) => {
    filters.value[key] = value
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const resetFilters = () => {
    filters.value = {
      board_type: null,
      category: null,
      performance_mt20id: null,
      search: '',
      ordering: '-created_at'
    }
  }

  const applyFilters = async () => {
    const params = {}
    if (filters.value.board_type) params.board_type = filters.value.board_type
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.performance_mt20id) params.performance_mt20id = filters.value.performance_mt20id
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.ordering) params.ordering = filters.value.ordering

    await fetchArticles(params)
  }

  // Best reviews actions
  const fetchBestReviews = async (limit = 4) => {
    bestLoading.value = true
    try {
      const response = await communityAPI.getBestReviews(limit)
      if (response.data.success) {
        bestReviews.value = response.data.results
      } else {
        bestReviews.value = []
      }
      return response.data
    } catch (err) {
      // 401/404는 빈 배열, 기타는 에러
      if (err.response && [401, 404].includes(err.response.status)) {
        bestReviews.value = []
      } else {
        error.value = err.message
        throw err
      }
    } finally {
      bestLoading.value = false
    }
  }

  return {
    // State
    articles,
    currentArticle,
    comments,
    loading,
    error,
    likeLoading,
    filters,
    bestReviews,
    bestLoading,
    // Getters
    articleCount,
    // Actions
    fetchArticles,
    fetchArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    likeArticle,
    fetchComments,
    createComment,
    updateComment,
    deleteComment,
    // Filter actions
    setFilter,
    setFilters,
    resetFilters,
    applyFilters,
    // Best reviews actions
    fetchBestReviews,
    // 하위 호환성을 위한 별칭
    reviews: articles,
    currentReview: currentArticle,
    reviewCount: articleCount,
    fetchReviews: fetchArticles,
    fetchReview: fetchArticle,
    createReview: createArticle,
    updateReview: updateArticle,
    deleteReview: deleteArticle,
    likeReview: likeArticle
  }
})
