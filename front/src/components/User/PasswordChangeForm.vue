<template>
  <div class="password-section">
    <h3 v-if="mode === 'edit'">비밀번호 변경 (선택사항)</h3>
    <p v-if="mode === 'edit'" class="section-description">비밀번호를 변경하지 않으려면 비워두세요.</p>

    <div class="form-group">
      <label for="password">{{ mode === 'edit' ? '새 비밀번호' : '비밀번호' }} {{ mode === 'register' ? '*' : '' }}</label>
      <input
        id="password"
        :value="password"
        @input="$emit('update:password', $event.target.value)"
        type="password"
        :placeholder="mode === 'edit' ? '새 비밀번호' : '비밀번호를 입력하세요'"
        :required="mode === 'register'"
        class="form-input"
      />
      <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
    </div>

    <div class="form-group">
      <label for="password2">{{ mode === 'edit' ? '새 비밀번호 확인' : '비밀번호 확인' }} {{ mode === 'register' ? '*' : '' }}</label>
      <input
        id="password2"
        :value="password2"
        @input="$emit('update:password2', $event.target.value)"
        type="password"
        :placeholder="mode === 'edit' ? '새 비밀번호 확인' : '비밀번호를 다시 입력하세요'"
        :required="mode === 'register'"
        class="form-input"
      />
      <span v-if="errors.password2" class="field-error">{{ errors.password2 }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  password: {
    type: String,
    default: ''
  },
  password2: {
    type: String,
    default: ''
  },
  mode: {
    type: String,
    default: 'edit', // 'edit' or 'register'
    validator: (value) => ['edit', 'register'].includes(value)
  },
  errors: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['update:password', 'update:password2'])
</script>

<style scoped>
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

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
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
</style>
