<template>
  <div class="basic-info-form">
    <!-- 아이디 -->
    <div class="form-group">
      <label for="username">아이디 *</label>
      <input
        id="username"
        :value="formData.username"
        @input="$emit('update:username', $event.target.value)"
        type="text"
        required
        placeholder="아이디를 입력하세요"
        class="form-input"
      />
      <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
    </div>

    <!-- 닉네임 -->
    <div class="form-group">
      <label for="nickname">닉네임 *</label>
      <input
        id="nickname"
        :value="formData.nickname"
        @input="$emit('update:nickname', $event.target.value)"
        @blur="$emit('check-nickname')"
        type="text"
        required
        placeholder="닉네임을 입력하세요"
        class="form-input"
      />
      <span v-if="nicknameCheckResult === 'checking'" class="field-help">
        <i class="fas fa-spinner fa-spin"></i>
        중복 확인 중...
      </span>
      <span v-else-if="nicknameCheckResult === 'available'" class="field-success">
        <i class="fas fa-check-circle"></i>
        사용 가능한 닉네임입니다
      </span>
      <span v-else-if="nicknameCheckResult === 'duplicate'" class="field-error">
        <i class="fas fa-times-circle"></i>
        이미 사용 중인 닉네임입니다
      </span>
      <span v-if="errors.nickname" class="field-error">{{ errors.nickname }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  formData: {
    type: Object,
    required: true
  },
  errors: {
    type: Object,
    default: () => ({})
  },
  nicknameCheckResult: {
    type: String,
    default: '' // '', 'checking', 'available', 'duplicate'
  }
})

defineEmits(['update:username', 'update:nickname', 'check-nickname'])
</script>

<style scoped>
.basic-info-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #e5e7eb;
}

.form-input {
  padding: 0.75rem;
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
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .form-input:focus {
  border-color: #818cf8;
  background: #4b5563;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .form-input::placeholder {
  color: #6b7280;
}

.field-error {
  color: #ef4444;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.3s;
}

:root.dark .field-error {
  color: #fca5a5;
}

.field-success {
  color: #10b981;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.3s;
}

:root.dark .field-success {
  color: #6ee7b7;
}

.field-help {
  color: #6b7280;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

:root.dark .field-help {
  color: #9ca3af;
}

.field-help i {
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .field-help i {
  color: #6b7280;
}
</style>
