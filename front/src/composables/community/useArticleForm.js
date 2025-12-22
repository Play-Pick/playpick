import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

/**
 * 게시글 작성/수정 공통 로직
 */
export function useArticleForm() {
  const router = useRouter()

  const submitting = ref(false)

  // 카테고리별 아이콘
  const getCategoryIcon = (category) => {
    const icons = {
      REVIEW: 'fas fa-star',
      EXPECT: 'fas fa-heart',
      EXPECTATION: 'fas fa-heart',
      QNA: 'fas fa-question-circle',
      INFO: 'fas fa-info-circle',
      FREE: 'fas fa-comment-dots'
    }
    return icons[category] || 'fas fa-pen'
  }

  // 카테고리별 라벨
  const getCategoryLabel = (category) => {
    const labels = {
      REVIEW: '관람후기',
      EXPECT: '기대평',
      EXPECTATION: '기대평',
      QNA: 'Q&A',
      INFO: '정보공유',
      FREE: '자유게시판'
    }
    return labels[category] || '글'
  }

  // 말머리(board_type) 라벨
  const getBoardTypeLabel = (boardType) => {
    return boardType === 'GENERAL' ? '자유/정보' : '공연글'
  }

  // 별점이 필요한 카테고리인지 확인
  const needsRating = (category) => {
    return category === 'REVIEW' || category === 'EXPECT' || category === 'EXPECTATION'
  }

  // 뒤로 가기
  const goBack = () => {
    router.back()
  }

  // 로그인 페이지로 이동
  const goToLogin = () => {
    router.push({ name: 'login' })
  }

  return {
    submitting,
    getCategoryIcon,
    getCategoryLabel,
    getBoardTypeLabel,
    needsRating,
    goBack,
    goToLogin
  }
}
