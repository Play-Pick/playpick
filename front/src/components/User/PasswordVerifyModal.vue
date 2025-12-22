<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>비밀번호 확인</h2>
        <button @click="$emit('close')" class="modal-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <p>회원정보를 수정하려면 비밀번호를 입력해주세요.</p>
        <input
          :value="password"
          @input="$emit('update:password', $event.target.value)"
          type="password"
          placeholder="비밀번호"
          class="password-input"
          @keyup.enter="$emit('verify')"
        />
        <p v-if="error" class="error-message">{{ error }}</p>
      </div>
      <div class="modal-footer">
        <button @click="$emit('verify')" class="btn-confirm" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-spin"></i>
          <span v-else>확인</span>
        </button>
        <button @click="$emit('close')" class="btn-cancel-modal">취소</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  password: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['close', 'verify', 'update:password'])
</script>

<style scoped>
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

.modal-body > p:first-child {
  color: #374151;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .modal-body > p:first-child {
  color: #d1d5db;
}

.password-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .password-input {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.password-input:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .password-input:focus {
  border-color: #818cf8;
  background: #4b5563;
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

.btn-confirm {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  min-width: 100px;
}

.btn-confirm:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

:root.dark .btn-confirm {
  background: #818cf8;
}

:root.dark .btn-confirm:hover:not(:disabled) {
  background: #6366f1;
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
</style>
