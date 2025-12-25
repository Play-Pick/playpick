<template>
  <div class="account-info-form">
    <!-- 이메일 -->
    <div class="form-group">
      <label for="email">이메일</label>
      <input
        id="email"
        :value="formData.email"
        @input="handleEmailInput"
        @blur="validateEmail"
        type="email"
        placeholder="example@email.com"
        :class="['form-input', { 'input-error': errors.email }]"
      />
      <p v-if="errors.email" class="error-text">
        <i class="fas fa-exclamation-circle"></i>
        {{ errors.email }}
      </p>
    </div>

    <!-- 생년월일 -->
    <div class="form-group">
      <label for="birth_date">생년월일</label>
      <input
        id="birth_date"
        :value="formData.birth_date"
        @input="emit('update:birthDate', $event.target.value)"
        type="date"
        class="form-input"
      />
    </div>

    <!-- 거주 지역 -->
    <div class="form-group">
      <label for="region">거주 지역</label>
      <select
        id="region"
        :value="formData.region"
        @change="emit('update:region', $event.target.value)"
        class="form-input"
      >
        <option value="">선택하세요</option>
        <option value="서울특별시">서울특별시</option>
        <option value="부산광역시">부산광역시</option>
        <option value="대구광역시">대구광역시</option>
        <option value="인천광역시">인천광역시</option>
        <option value="광주광역시">광주광역시</option>
        <option value="대전광역시">대전광역시</option>
        <option value="울산광역시">울산광역시</option>
        <option value="세종특별자치시">세종특별자치시</option>
        <option value="경기도">경기도</option>
        <option value="강원특별자치도">강원특별자치도</option>
        <option value="충청북도">충청북도</option>
        <option value="충청남도">충청남도</option>
        <option value="전북특별자치도">전북특별자치도</option>
        <option value="전라남도">전라남도</option>
        <option value="경상북도">경상북도</option>
        <option value="경상남도">경상남도</option>
        <option value="제주특별자치도">제주특별자치도</option>
      </select>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  formData: {
    type: Object,
    required: true
  },
  errors: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:email', 'update:birthDate', 'update:region'])

// 이메일 입력 처리
const handleEmailInput = (event) => {
  const value = event.target.value
  emit('update:email', value)

  // 입력 중에는 에러 메시지 제거
  if (props.errors.email) {
    delete props.errors.email
  }
}

// 이메일 유효성 검사
const validateEmail = () => {
  const email = props.formData.email.trim()

  // 이메일이 비어있으면 검사하지 않음 (선택 필드)
  if (!email) {
    delete props.errors.email
    return true
  }

  // 이메일 정규식 검사 (RFC 5322 기반)
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

  if (!emailRegex.test(email)) {
    props.errors.email = '올바른 이메일 형식이 아닙니다. (예: example@email.com)'
    return false
  }

  delete props.errors.email
  return true
}

// 외부에서 호출 가능하도록 expose
defineExpose({
  validateEmail
})
</script>

<style scoped>
.account-info-form {
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

.form-input,
select.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .form-input,
:root.dark select.form-input {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.form-input:focus,
select.form-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .form-input:focus,
:root.dark select.form-input:focus {
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

/* 에러 상태 */
.input-error {
  border-color: #ef4444 !important;
}

:root.dark .input-error {
  border-color: #f87171 !important;
}

.error-text {
  color: #ef4444;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-top: -0.25rem;
}

:root.dark .error-text {
  color: #fca5a5;
}

.error-text i {
  font-size: 0.75rem;
}
</style>
