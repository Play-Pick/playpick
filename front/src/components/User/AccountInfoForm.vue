<template>
  <div class="account-info-form">
    <!-- 이메일 -->
    <div class="form-group">
      <label for="email">이메일</label>
      <input
        id="email"
        :value="formData.email"
        @input="$emit('update:email', $event.target.value)"
        type="email"
        placeholder="이메일"
        class="form-input"
      />
    </div>

    <!-- 생년월일 -->
    <div class="form-group">
      <label for="birth_date">생년월일</label>
      <input
        id="birth_date"
        :value="formData.birth_date"
        @input="$emit('update:birthDate', $event.target.value)"
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
        @change="$emit('update:region', $event.target.value)"
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
  </div>
</template>

<script setup>
defineProps({
  formData: {
    type: Object,
    required: true
  }
})

defineEmits(['update:email', 'update:birthDate', 'update:region'])
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
