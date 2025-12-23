<template>
  <div class="register-view">
    <div class="register-container">
      <h1>회원가입</h1>
      <p class="subtitle">공연 추천 커뮤니티에 오신 것을 환영합니다!</p>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- 기본 정보 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-user"></i>
            기본 정보
          </h3>

          <BasicInfoForm
            :form-data="formData"
            :errors="errors"
            :nickname-check-result="nicknameCheckResult"
            @update:username="formData.username = $event"
            @update:nickname="formData.nickname = $event"
            @check-nickname="checkNicknameDuplicate"
          />

          <AccountInfoForm
            :form-data="formData"
            @update:email="formData.email = $event"
            @update:birth-date="formData.birth_date = $event"
            @update:region="formData.region = $event"
          />

          <PasswordChangeForm
            mode="register"
            :password="formData.password"
            :password2="formData.password2"
            :errors="errors"
            @update:password="formData.password = $event"
            @update:password2="formData.password2 = $event"
          />
        </div>

        <!-- 선호 정보 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-heart"></i>
            선호 장르 (선택사항)
          </h3>
          <p class="section-description">맞춤 공연을 추천받을 수 있습니다</p>

          <PreferenceForm
            v-model="formData.preference_tags"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          <i class="fas fa-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <button type="submit" class="btn-register" :disabled="loading">
          <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-user-plus'"></i>
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <div class="footer-links">
        <p>
          이미 계정이 있으신가요?
          <router-link to="/login">로그인</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import usersAPI from '@/api/users'
import BasicInfoForm from '@/components/User/BasicInfoForm.vue'
import AccountInfoForm from '@/components/User/AccountInfoForm.vue'
import PasswordChangeForm from '@/components/User/PasswordChangeForm.vue'
import PreferenceForm from '@/components/User/PreferenceForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  nickname: '',
  email: '',
  password: '',
  password2: '',
  birth_date: '',
  region: '',
  preference_tags: [],
})

const loading = ref(false)
const errorMessage = ref('')
const errors = ref({})

// 닉네임 중복 확인
const nicknameCheckResult = ref('') // '', 'checking', 'available', 'duplicate'
let nicknameCheckTimeout = null

const checkNicknameDuplicate = async () => {
  const nickname = formData.value.nickname.trim()

  if (!nickname) {
    nicknameCheckResult.value = ''
    return
  }

  // 디바운싱
  clearTimeout(nicknameCheckTimeout)
  nicknameCheckTimeout = setTimeout(async () => {
    try {
      nicknameCheckResult.value = 'checking'

      // 모든 사용자 조회하여 닉네임 중복 확인
      const response = await usersAPI.getUsers()
      const users = response.data.results || response.data

      const isDuplicate = users.some(user => user.nickname === nickname)

      nicknameCheckResult.value = isDuplicate ? 'duplicate' : 'available'
    } catch (error) {
      console.error('닉네임 중복 확인 실패:', error)
      nicknameCheckResult.value = ''
    }
  }, 500)
}

const handleRegister = async () => {
  loading.value = true
  errorMessage.value = ''
  errors.value = {}

  // 클라이언트 측 유효성 검사
  if (!formData.value.nickname.trim()) {
    errors.value.nickname = '닉네임은 필수 입력 항목입니다.'
    loading.value = false
    return
  }

  if (nicknameCheckResult.value === 'duplicate') {
    errors.value.nickname = '이미 사용 중인 닉네임입니다.'
    loading.value = false
    return
  }

  if (formData.value.password !== formData.value.password2) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.'
    loading.value = false
    return
  }

  try {
    // 빈 값 제거 및 데이터 정리
    const submitData = {
      username: formData.value.username,
      nickname: formData.value.nickname,
      password: formData.value.password,
      password2: formData.value.password2,
    }

    // 선택 필드는 값이 있을 때만 포함
    if (formData.value.email) submitData.email = formData.value.email
    if (formData.value.birth_date) submitData.birth_date = formData.value.birth_date
    if (formData.value.region) submitData.region = formData.value.region
    if (formData.value.preference_tags.length > 0) {
      submitData.preference_tags = formData.value.preference_tags
    }

    await authStore.register(submitData)
    // 회원가입 성공 시 홈으로 이동
    router.push('/')
  } catch (error) {
    console.error('회원가입 실패:', error)

    // 에러 메시지 표시
    if (error.response?.data) {
      const data = error.response.data

      // 필드별 에러 메시지
      Object.keys(data).forEach(key => {
        if (key !== 'detail' && key !== 'non_field_errors') {
          errors.value[key] = Array.isArray(data[key]) ? data[key][0] : data[key]
        }
      })

      // 일반 에러 메시지
      if (data.detail) {
        errorMessage.value = data.detail
      } else if (data.non_field_errors) {
        errorMessage.value = data.non_field_errors[0]
      } else if (Object.keys(errors.value).length === 0) {
        errorMessage.value = '회원가입에 실패했습니다.'
      }
    } else {
      errorMessage.value = '네트워크 오류가 발생했습니다.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-view {
  min-height: calc(100vh - 200px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  transition: background 0.3s;
}

:root.dark .register-view {
  background: linear-gradient(to bottom, #111827, #1f2937);
}

.register-container {
  width: 100%;
  max-width: 600px;
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

:root.dark .register-container {
  background: #1f2937;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.register-container h1 {
  text-align: center;
  margin-bottom: 0.5rem;
  color: #1f2937;
  font-size: 2rem;
  transition: color 0.3s;
}

:root.dark .register-container h1 {
  color: #f3f4f6;
}

.subtitle {
  text-align: center;
  color: #6b7280;
  margin-bottom: 2rem;
  transition: color 0.3s;
}

:root.dark .subtitle {
  color: #9ca3af;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* 섹션 */
.section {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: background-color 0.3s, border-color 0.3s;
}

:root.dark .section {
  background: #111827;
  border-color: #374151;
}

.section-title {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

:root.dark .section-title {
  color: #f3f4f6;
}

.section-title i {
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .section-title i {
  color: #818cf8;
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


/* 에러 메시지 */
.error-message {
  padding: 1rem;
  background-color: #fef2f2;
  color: #ef4444;
  border: 1px solid #fecaca;
  border-radius: 6px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}

:root.dark .error-message {
  background-color: #7f1d1d;
  color: #fca5a5;
  border-color: #991b1b;
}

/* 버튼 */
.btn-register {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

:root.dark .btn-register {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

:root.dark .btn-register:hover:not(:disabled) {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 8px 16px rgba(99, 102, 241, 0.4);
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

:root.dark .btn-register:disabled {
  background: #4b5563;
  color: #9ca3af;
  opacity: 1;
}

/* Footer */
.footer-links {
  margin-top: 1.5rem;
  text-align: center;
}

.footer-links p {
  color: #6b7280;
  font-size: 0.875rem;
  transition: color 0.3s;
}

:root.dark .footer-links p {
  color: #9ca3af;
}

.footer-links a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

:root.dark .footer-links a {
  color: #818cf8;
}

.footer-links a:hover {
  text-decoration: underline;
}

:root.dark .footer-links a:hover {
  color: #a5b4fc;
}

/* 반응형 */
@media (max-width: 640px) {
  .register-container {
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .section {
    padding: 1rem;
  }
}
</style>
