import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/communityStore'
import { useAuthStore } from '@/stores/authStore'

export const useArticleDetail = (articleId) => {
  const router = useRouter()
  const communityStore = useCommunityStore()
  const authStore = useAuthStore()

  const likeLoading = ref(false)
  const commentLoading = ref(false)

  // 좋아요 처리
  const handleLike = async () => {
    if (!authStore.isAuthenticated) {
      alert('로그인이 필요합니다.')
      return
    }

    likeLoading.value = true
    try {
      await communityStore.likeArticle(articleId)
      // 좋아요 상태 토글
      if (communityStore.currentArticle) {
        communityStore.currentArticle.is_liked = !communityStore.currentArticle.is_liked
      }
    } catch (err) {
      console.error('좋아요 처리 실패:', err)
    } finally {
      likeLoading.value = false
    }
  }

  // 댓글 작성
  const submitComment = async (content) => {
    commentLoading.value = true
    try {
      await communityStore.createComment({
        article: articleId,
        content: content
      })
    } catch (err) {
      console.error('댓글 작성 실패:', err)
      alert('댓글 작성에 실패했습니다.')
    } finally {
      commentLoading.value = false
    }
  }

  // 댓글 삭제
  const deleteComment = async (commentId) => {
    try {
      await communityStore.deleteComment(commentId)
    } catch (err) {
      console.error('댓글 삭제 실패:', err)
      alert('댓글 삭제에 실패했습니다.')
    }
  }

  // 게시글 수정
  const editArticle = () => {
    router.push(`/community/${articleId}/edit`)
  }

  // 게시글 삭제
  const deleteArticle = async () => {
    if (!confirm('게시글을 삭제하시겠습니까?')) return

    try {
      await communityStore.deleteArticle(articleId)
      router.push('/community')
    } catch (err) {
      console.error('게시글 삭제 실패:', err)
      alert('게시글 삭제에 실패했습니다.')
    }
  }

  // 목록으로 돌아가기
  const goBack = () => {
    router.push('/community')
  }

  // 데이터 로드
  const loadArticleData = async () => {
    try {
      await Promise.all([
        communityStore.fetchArticle(articleId),
        communityStore.fetchComments(articleId)
      ])
    } catch (err) {
      console.error('게시글 데이터 로딩 실패:', err)
    }
  }

  return {
    // State
    likeLoading,
    commentLoading,
    // Store refs
    currentArticle: communityStore.currentArticle,
    comments: communityStore.comments,
    loading: communityStore.loading,
    error: communityStore.error,
    // Actions
    handleLike,
    submitComment,
    deleteComment,
    editArticle,
    deleteArticle,
    goBack,
    loadArticleData
  }
}
