import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useWatchedStore } from '@/stores/watchedStore'
import { usePerformanceStore } from '@/stores/performanceStore'
import authAPI from '@/api/auth'
import communityAPI from '@/api/community'

export function useMyPage() {
  const router = useRouter()
  const authStore = useAuthStore()
  const wishlistStore = useWishlistStore()
  const watchedStore = useWatchedStore()
  const performanceStore = usePerformanceStore()

  const loading = ref(true)
  const error = ref(null)
  const isEditMode = ref(false)
  const activeTab = ref('articles')

  const currentUser = ref({})
  const myArticles = ref([])
  const myComments = ref([])
  const articles = ref([])

  const profileImage = ref(null)
  const editForm = ref({
    nickname: '',
    profileImage: null,
  })

  // 비밀번호 확인 모달 관련
  const showPasswordModal = ref(false)
  const passwordVerify = ref('')
  const passwordError = ref('')
  const verifyLoading = ref(false)

  // 평균 별점 계산
  const averageRating = computed(() => {
    const ratedArticles = myArticles.value.filter(a => a.rank !== null)
    if (ratedArticles.length === 0) return '0.0'
    const sum = ratedArticles.reduce((acc, a) => acc + a.rank, 0)
    return (sum / ratedArticles.length).toFixed(1)
  })

  // 데이터 로드
  const loadData = async () => {
    try {
      loading.value = true
      error.value = null

      // 현재 사용자 정보
      const userRes = await authAPI.getCurrentUser()
      currentUser.value = userRes.data

      // 내가 쓴 게시글
      const articlesRes = await communityAPI.getArticles()
      const allArticles = articlesRes.data.results || articlesRes.data
      myArticles.value = allArticles.filter(a => a.user === currentUser.value.id)

      // 내가 쓴 댓글
      const commentsRes = await communityAPI.getComments()
      const allComments = commentsRes.data.results || commentsRes.data
      myComments.value = allComments.filter(c => c.user === currentUser.value.id)

      // 전체 게시글 목록 (댓글의 게시글 제목 찾기용)
      articles.value = allArticles

      // 프로필 이미지 설정
      if (currentUser.value.profile_image) {
        profileImage.value = currentUser.value.profile_image
      }

      editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
    } catch (err) {
      console.error('데이터 로드 실패:', err)
      error.value = '데이터를 불러오는데 실패했습니다.'
    } finally {
      loading.value = false
    }
  }

  // Wishlist & Watched 초기화
  const initWishlist = async () => {
    try {
      await wishlistStore.fetchWishlist()
    } catch (err) {
      // Error message is handled in store
    }
  }

  const initWatched = async () => {
    try {
      await watchedStore.fetchWatched()
    } catch (err) {
      // Error message is handled in store
    }
  }

  // 프로필 편집 토글
  const toggleEditMode = () => {
    isEditMode.value = !isEditMode.value
    if (isEditMode.value) {
      editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
    }
  }

  // 이미지 변경 핸들러
  const handleImageChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      editForm.value.profileImage = file
      // 미리보기
      const reader = new FileReader()
      reader.onload = (e) => {
        profileImage.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }

  // 프로필 저장
  const saveProfile = async () => {
    try {
      const formData = new FormData()
      if (editForm.value.nickname) {
        formData.append('nickname', editForm.value.nickname)
      }
      if (editForm.value.profileImage) {
        formData.append('profile_image', editForm.value.profileImage)
      }

      // TODO: 백엔드 API 호출 (현재는 로컬 상태만 업데이트)
      // await apiClient.patch(`/users/${currentUser.value.id}/`, formData)

      // 로컬 상태 업데이트
      currentUser.value.nickname = editForm.value.nickname

      isEditMode.value = false
      alert('프로필이 업데이트되었습니다!')
    } catch (err) {
      console.error('프로필 저장 실패:', err)
      alert('프로필 저장에 실패했습니다.')
    }
  }

  // 편집 취소
  const cancelEdit = () => {
    isEditMode.value = false
    editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
    profileImage.value = currentUser.value.profile_image || null
  }

  // 비밀번호 확인 모달 열기
  const showEditAccountModal = () => {
    showPasswordModal.value = true
    passwordVerify.value = ''
    passwordError.value = ''
  }

  // 비밀번호 확인 모달 닫기
  const closePasswordModal = () => {
    showPasswordModal.value = false
    passwordVerify.value = ''
    passwordError.value = ''
  }

  // 비밀번호 검증
  const verifyPassword = async () => {
    if (!passwordVerify.value) {
      passwordError.value = '비밀번호를 입력해주세요.'
      return
    }

    try {
      verifyLoading.value = true
      passwordError.value = ''

      const response = await authAPI.verifyPassword(passwordVerify.value)

      if (response.data.verified) {
        closePasswordModal()
        // 회원정보 수정 페이지로 이동
        router.push({ name: 'edit-account' })
      }
    } catch (err) {
      console.error('비밀번호 확인 실패:', err)
      passwordError.value = err.response?.data?.error || '비밀번호가 일치하지 않습니다.'
    } finally {
      verifyLoading.value = false
    }
  }

  // 네비게이션
  const goToPerformance = (performanceId) => {
    router.push({ name: 'performance-detail', params: { id: performanceId } })
  }

  const goToArticle = (articleId) => {
    router.push({ name: 'community', query: { articleId } })
  }

  const goToPerformances = () => {
    router.push({ name: 'performances' })
  }

  // Wishlist & Watched 처리
  const handleWishlistToggle = async (performanceId) => {
    try {
      // performanceStore의 toggleLike를 사용하여 전역 상태 업데이트
      await performanceStore.toggleLike(performanceId)
      // 찜 목록도 새로고침
      await wishlistStore.fetchWishlist()
    } catch (err) {
      if (err.message === '로그인이 필요합니다.') {
        alert('로그인이 필요한 기능입니다.')
      } else {
        console.error('찜하기 실패:', err)
      }
    }
  }

  const handleWatchedRemove = async (performanceId) => {
    try {
      await watchedStore.removeFromWatched(performanceId)
    } catch (err) {
      // Error message is handled in store
    }
  }

  return {
    // State
    loading,
    error,
    isEditMode,
    activeTab,
    currentUser,
    myArticles,
    myComments,
    articles,
    profileImage,
    editForm,
    showPasswordModal,
    passwordVerify,
    passwordError,
    verifyLoading,
    // Computed
    averageRating,
    // Methods
    loadData,
    initWishlist,
    initWatched,
    toggleEditMode,
    handleImageChange,
    saveProfile,
    cancelEdit,
    showEditAccountModal,
    closePasswordModal,
    verifyPassword,
    goToPerformance,
    goToArticle,
    goToPerformances,
    handleWishlistToggle,
    handleWatchedRemove
  }
}
