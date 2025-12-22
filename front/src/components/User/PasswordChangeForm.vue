<template>
  <div class="password-section">
    <h3>비밀번호 변경 (선택사항)</h3>
    <p class="section-description">비밀번호를 변경하지 않으려면 비워두세요.</p>

    <div class="form-group">
      <label for="password">새 비밀번호</label>
      <input
        id="password"
        :value="password"
        @input="$emit('update:password', $event.target.value)"
        type="password"
        placeholder="새 비밀번호"
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label for="password2">새 비밀번호 확인</label>
      <input
        id="password2"
        :value="password2"
        @input="$emit('update:password2', $event.target.value)"
        type="password"
        placeholder="새 비밀번호 확인"
        class="form-input"
      />
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
</style>
