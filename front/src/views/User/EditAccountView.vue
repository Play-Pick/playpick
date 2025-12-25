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
        <!-- 계정 정보 -->
        <AccountInfoForm
          :form-data="formData"
          @update:email="formData.email = $event"
          @update:birth-date="formData.birth_date = $event"
          @update:region="formData.region = $event"
        />

        <!-- 비밀번호 변경 섹션 -->
        <PasswordChangeForm
          v-model:password="formData.password"
          v-model:password2="formData.password2"
        />

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
    <DeleteAccountModal
      :show="showDeleteModal"
      :loading="deleteLoading"
      :error="deleteError"
      @close="closeDeleteModal"
      @delete="deleteAccount"
    />
  </div>
</template>

<script setup>
import { useEditAccount } from '@/composables/useEditAccount'
import AccountInfoForm from '@/components/User/AccountInfoForm.vue'
import PasswordChangeForm from '@/components/User/PasswordChangeForm.vue'
import DeleteAccountModal from '@/components/User/DeleteAccountModal.vue'

// useEditAccount composable 사용
const {
  loading,
  submitting,
  errorMessage,
  successMessage,
  formData,
  showDeleteModal,
  deleteError,
  deleteLoading,
  updateAccount,
  showDeleteConfirm,
  closeDeleteModal,
  deleteAccount,
  goBack
} = useEditAccount()
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
