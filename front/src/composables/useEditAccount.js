import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import authAPI from '@/api/auth'

export function useEditAccount() {
  const router = useRouter()
  const authStore = useAuthStore()

  const loading = ref(false) // 초기값을 false로 변경
  const submitting = ref(false)
  const errorMessage = ref('')
  const successMessage = ref('')

  // authStore에서 사용자 정보를 즉시 가져와 초기화
  const currentUser = authStore.user
  const formData = ref({
    email: currentUser?.email || '',
    birth_date: currentUser?.birth_date || '',
    region: currentUser?.region || '',
    password: '',
    password2: ''
  })

  // 회원 탈퇴 모달
  const showDeleteModal = ref(false)
  const deleteError = ref('')
  const deleteLoading = ref(false)

  // 현재 사용자 정보 불러오기 (필요시에만 호출)
  const loadUserData = async () => {
    try {
      loading.value = true
      const response = await authAPI.getCurrentUser()
      const user = response.data

      formData.value.email = user.email || ''
      formData.value.birth_date = user.birth_date || ''
      formData.value.region = user.region || ''
    } catch (err) {
      console.error('사용자 정보 로드 실패:', err)
      errorMessage.value = '사용자 정보를 불러올 수 없습니다.'
    } finally {
      loading.value = false
    }
  }

  // 회원정보 수정
  const updateAccount = async () => {
    try {
      submitting.value = true
      errorMessage.value = ''
      successMessage.value = ''

      // 비밀번호 확인 검증
      if (formData.value.password || formData.value.password2) {
        if (formData.value.password !== formData.value.password2) {
          errorMessage.value = '비밀번호가 일치하지 않습니다.'
          return
        }
      }

      const updateData = {}

      // 값이 있는 필드만 추가
      if (formData.value.email) updateData.email = formData.value.email
      if (formData.value.birth_date) updateData.birth_date = formData.value.birth_date
      if (formData.value.region) updateData.region = formData.value.region

      // 비밀번호가 입력된 경우에만 추가
      if (formData.value.password) {
        updateData.password = formData.value.password
        updateData.password2 = formData.value.password2
      }

      await authAPI.updateProfile(updateData)

      // authStore의 사용자 정보 업데이트
      if (authStore.user) {
        if (updateData.email) authStore.user.email = updateData.email
        if (updateData.birth_date) authStore.user.birth_date = updateData.birth_date
        if (updateData.region) authStore.user.region = updateData.region
      }

      // 즉시 마이페이지로 이동 (성공 메시지는 마이페이지에서 토스트로 표시 가능)
      router.push({ name: 'mypage' })
    } catch (err) {
      console.error('회원정보 수정 실패:', err)
      errorMessage.value = err.response?.data?.error || err.response?.data?.password2?.[0] || '회원정보 수정에 실패했습니다.'
    } finally {
      submitting.value = false
    }
  }

  // 회원 탈퇴 모달 열기
  const showDeleteConfirm = () => {
    showDeleteModal.value = true
    deleteError.value = ''
  }

  // 회원 탈퇴 모달 닫기
  const closeDeleteModal = () => {
    showDeleteModal.value = false
    deleteError.value = ''
  }

  // 회원 탈퇴
  const deleteAccount = async (password) => {
    if (!password) {
      deleteError.value = '비밀번호를 입력해주세요.'
      return
    }

    try {
      deleteLoading.value = true
      deleteError.value = ''

      await authAPI.deleteAccount(password)

      alert('회원 탈퇴가 완료되었습니다.')

      // 로그아웃 처리
      authStore.logout()
      router.push({ name: 'home' })
    } catch (err) {
      console.error('회원 탈퇴 실패:', err)
      deleteError.value = err.response?.data?.error || '회원 탈퇴에 실패했습니다.'
    } finally {
      deleteLoading.value = false
    }
  }

  // 뒤로 가기
  const goBack = () => {
    router.push({ name: 'mypage' })
  }

  // onMounted 제거 - authStore에서 즉시 데이터를 가져오므로 불필요
  // 필요한 경우에만 loadUserData()를 수동으로 호출 가능

  return {
    // State
    loading,
    submitting,
    errorMessage,
    successMessage,
    formData,
    showDeleteModal,
    deleteError,
    deleteLoading,
    // Methods
    loadUserData,
    updateAccount,
    showDeleteConfirm,
    closeDeleteModal,
    deleteAccount,
    goBack
  }
}
