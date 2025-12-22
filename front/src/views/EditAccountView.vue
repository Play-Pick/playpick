<template>
  <div class="edit-account-container">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <div v-else class="edit-account-content">
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1>회원정보 수정</h1>
      </div>

      <form @submit.prevent="updateAccount" class="edit-form">
        <!-- 이메일 -->
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="이메일"
            class="form-input"
          />
        </div>

        <!-- 닉네임 -->
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input
            id="nickname"
            v-model="formData.nickname"
            type="text"
            placeholder="닉네임"
            class="form-input"
          />
        </div>

        <!-- 생년월일 -->
        <div class="form-group">
          <label for="birth_date">생년월일</label>
          <input
            id="birth_date"
            v-model="formData.birth_date"
            type="date"
            class="form-input"
          />
        </div>

        <!-- 거주 지역 -->
        <div class="form-group">
          <label for="region">거주 지역</label>
          <select
            id="region"
            v-model="formData.region"
            class="form-input"
          >
            <option value="">선택 안함</option>
            <option value="서울특별시">서울특별시</option>
            <option value="경기도">경기도</option>
            <option value="인천광역시">인천광역시</option>
            <option value="부산광역시">부산광역시</option>
            <option value="대구광역시">대구광역시</option>
            <option value="대전광역시">대전광역시</option>
            <option value="광주광역시">광주광역시</option>
            <option value="울산광역시">울산광역시</option>
            <option value="세종특별자치시">세종특별자치시</option>
            <option value="강원도">강원도</option>
            <option value="충청북도">충청북도</option>
            <option value="충청남도">충청남도</option>
            <option value="전라북도">전라북도</option>
            <option value="전라남도">전라남도</option>
            <option value="경상북도">경상북도</option>
            <option value="경상남도">경상남도</option>
            <option value="제주특별자치도">제주특별자치도</option>
          </select>
        </div>

        <!-- 비밀번호 변경 섹션 -->
        <div class="password-section">
          <h3>비밀번호 변경 (선택사항)</h3>
          <p class="section-description">비밀번호를 변경하지 않으려면 비워두세요.</p>

          <div class="form-group">
            <label for="password">새 비밀번호</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="새 비밀번호"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="password2">새 비밀번호 확인</label>
            <input
              id="password2"
              v-model="formData.password2"
              type="password"
              placeholder="새 비밀번호 확인"
              class="form-input"
            />
          </div>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="errorMessage" class="error-alert">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ errorMessage }}</span>
        </div>

        <!-- 성공 메시지 -->
        <div v-if="successMessage" class="success-alert">
          <i class="fas fa-check-circle"></i>
          <span>{{ successMessage }}</span>
        </div>

        <!-- 버튼 그룹 -->
        <div class="button-group">
          <button type="submit" class="btn-submit" :disabled="submitting">
            <i v-if="submitting" class="fas fa-spinner fa-spin"></i>
            <span v-else>저장</span>
          </button>
          <button type="button" @click="goBack" class="btn-cancel">취소</button>
          <button type="button" @click="showDeleteConfirm" class="btn-delete">
            <i class="fas fa-trash"></i> 회원 탈퇴
          </button>
        </div>
      </form>
    </div>

    <!-- 회원 탈퇴 확인 모달 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>회원 탈퇴</h2>
          <button @click="closeDeleteModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p class="warning-text">
            <i class="fas fa-exclamation-triangle"></i>
            정말로 탈퇴하시겠습니까? 모든 데이터가 삭제되며 복구할 수 없습니다.
          </p>
          <div class="form-group">
            <label for="delete-password">비밀번호를 입력하여 확인해주세요</label>
            <input
              id="delete-password"
              v-model="deletePassword"
              type="password"
              placeholder="비밀번호"
              class="form-input"
              @keyup.enter="deleteAccount"
            />
          </div>
          <p v-if="deleteError" class="error-message">{{ deleteError }}</p>
        </div>
        <div class="modal-footer">
          <button @click="deleteAccount" class="btn-delete-confirm" :disabled="deleteLoading">
            <i v-if="deleteLoading" class="fas fa-spinner fa-spin"></i>
            <span v-else>탈퇴하기</span>
          </button>
          <button @click="closeDeleteModal" class="btn-cancel-modal">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const formData = ref({
  email: '',
  nickname: '',
  birth_date: '',
  region: '',
  password: '',
  password2: ''
})

// 회원 탈퇴 모달
const showDeleteModal = ref(false)
const deletePassword = ref('')
const deleteError = ref('')
const deleteLoading = ref(false)

// 현재 사용자 정보 불러오기
const loadUserData = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/users/me/')
    const user = response.data

    formData.value.email = user.email || ''
    formData.value.nickname = user.nickname || ''
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

    const updateData = {
      email: formData.value.email,
      nickname: formData.value.nickname,
      birth_date: formData.value.birth_date,
      region: formData.value.region
    }

    // 비밀번호가 입력된 경우에만 추가
    if (formData.value.password) {
      updateData.password = formData.value.password
      updateData.password2 = formData.value.password2
    }

    const response = await apiClient.patch('/users/update_profile/', updateData)

    successMessage.value = '회원정보가 성공적으로 수정되었습니다.'

    // 비밀번호 필드 초기화
    formData.value.password = ''
    formData.value.password2 = ''

    // 2초 후 마이페이지로 이동
    setTimeout(() => {
      router.push({ name: 'mypage' })
    }, 2000)
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
  deletePassword.value = ''
  deleteError.value = ''
}

// 회원 탈퇴 모달 닫기
const closeDeleteModal = () => {
  showDeleteModal.value = false
  deletePassword.value = ''
  deleteError.value = ''
}

// 회원 탈퇴
const deleteAccount = async () => {
  if (!deletePassword.value) {
    deleteError.value = '비밀번호를 입력해주세요.'
    return
  }

  try {
    deleteLoading.value = true
    deleteError.value = ''

    await apiClient.delete('/users/delete_account/', {
      data: { password: deletePassword.value }
    })

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

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.edit-account-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
  transition: background 0.3s;
}

:root.dark .edit-account-container {
  background: linear-gradient(to bottom, #111827, #1f2937);
}

.loading {
  text-align: center;
  padding: 5rem 2rem;
  color: #1f2937;
  transition: color 0.3s;
}

:root.dark .loading {
  color: #f3f4f6;
}

.spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

:root.dark .spinner {
  border-color: #374151;
  border-top-color: #818cf8;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.edit-account-content {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

:root.dark .edit-account-content {
  background: #1f2937;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .page-header {
  border-bottom-color: #374151;
}

.btn-back {
  background: #f3f4f6;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: #1f2937;
}

.btn-back:hover {
  background: #e5e7eb;
}

:root.dark .btn-back {
  background: #374151;
  color: #f3f4f6;
}

:root.dark .btn-back:hover {
  background: #4b5563;
}

.page-header h1 {
  font-size: 1.75rem;
  color: #1f2937;
  margin: 0;
  transition: color 0.3s;
}

:root.dark .page-header h1 {
  color: #f3f4f6;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #d1d5db;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .form-input {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .form-input:focus {
  border-color: #818cf8;
  background: #4b5563;
}

.password-section {
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .password-section {
  border-top-color: #374151;
}

.password-section h3 {
  font-size: 1.25rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

:root.dark .password-section h3 {
  color: #f3f4f6;
}

.section-description {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .section-description {
  color: #9ca3af;
}

.error-alert,
.success-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
}

.error-alert {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

:root.dark .error-alert {
  background: #7f1d1d;
  color: #fecaca;
  border-color: #991b1b;
}

.success-alert {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

:root.dark .success-alert {
  background: #064e3b;
  color: #a7f3d0;
  border-color: #065f46;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-submit {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  min-width: 80px;
}

.btn-submit:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #1f2937;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

:root.dark .btn-cancel {
  background: #374151;
  color: #f3f4f6;
}

:root.dark .btn-cancel:hover {
  background: #4b5563;
}

.btn-delete {
  padding: 0.75rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-delete:hover {
  background: #dc2626;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
  transition: background-color 0.3s;
}

:root.dark .modal-content {
  background: #1f2937;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .modal-header {
  border-bottom-color: #374151;
}

.modal-header h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0;
  transition: color 0.3s;
}

:root.dark .modal-header h2 {
  color: #f3f4f6;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

:root.dark .modal-close {
  color: #9ca3af;
}

:root.dark .modal-close:hover {
  background: #374151;
  color: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.warning-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #dc2626;
  font-weight: 500;
  margin-bottom: 1rem;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.modal-footer {
  display: flex;
  gap: 0.5rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  justify-content: flex-end;
  transition: border-color 0.3s;
}

:root.dark .modal-footer {
  border-top-color: #374151;
}

.btn-delete-confirm {
  padding: 0.75rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  min-width: 100px;
}

.btn-delete-confirm:hover:not(:disabled) {
  background: #dc2626;
}

.btn-delete-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel-modal {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #1f2937;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-cancel-modal:hover {
  background: #e5e7eb;
}

:root.dark .btn-cancel-modal {
  background: #374151;
  color: #f3f4f6;
}

:root.dark .btn-cancel-modal:hover {
  background: #4b5563;
}

/* 반응형 */
@media (max-width: 768px) {
  .edit-account-container {
    padding: 1rem;
  }

  .edit-account-content {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn-submit,
  .btn-cancel,
  .btn-delete {
    width: 100%;
  }
}
</style>
