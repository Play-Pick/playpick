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

          <div class="form-group">
            <label for="username">아이디 *</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              placeholder="아이디를 입력하세요"
            />
            <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
          </div>

          <div class="form-group">
            <label for="nickname">닉네임 *</label>
            <input
              id="nickname"
              v-model="formData.nickname"
              type="text"
              required
              placeholder="닉네임을 입력하세요"
              @blur="checkNicknameDuplicate"
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

          <div class="form-group">
            <label for="email">이메일</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="이메일을 입력하세요 (선택사항)"
            />
            <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label for="password">비밀번호 *</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              placeholder="비밀번호를 입력하세요"
            />
            <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
          </div>

          <div class="form-group">
            <label for="password2">비밀번호 확인 *</label>
            <input
              id="password2"
              v-model="formData.password2"
              type="password"
              required
              placeholder="비밀번호를 다시 입력하세요"
            />
            <span v-if="errors.password2" class="field-error">{{ errors.password2 }}</span>
          </div>

          <div class="form-group">
            <label for="birth_date">생년월일</label>
            <input
              id="birth_date"
              v-model="formData.birth_date"
              type="date"
              placeholder="생년월일을 선택하세요"
            />
          </div>
        </div>

        <!-- 위치 정보 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-map-marker-alt"></i>
            거주 지역 (선택사항)
          </h3>
          <p class="section-description">근처 공연을 추천받을 수 있습니다</p>

          <div class="form-group">
            <label for="region">광역시/도</label>
            <select
              id="region"
              v-model="formData.region"
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

        <!-- 선호 정보 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-heart"></i>
            선호 장르 (선택사항)
          </h3>
          <p class="section-description">맞춤 공연을 추천받을 수 있습니다</p>

          <div class="form-group">
            <label>선호 장르 선택</label>
            <div class="genre-grid">
              <label
                v-for="genre in availableGenres"
                :key="genre.code"
                class="genre-checkbox"
              >
                <input
                  type="checkbox"
                  :value="genre.name"
                  v-model="formData.preference_tags"
                />
                <span class="genre-label">{{ genre.name }}</span>
              </label>
            </div>
            <span class="field-help">
              <i class="fas fa-info-circle"></i>
              선호하는 장르를 선택해주세요 (중복 선택 가능)
            </span>
          </div>
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
import apiClient from '@/api/axios'

const router = useRouter()
const authStore = useAuthStore()

// 사용 가능한 장르 목록
const availableGenres = [
  { code: 'BBBC', name: '뮤지컬' },
  { code: 'AAAA', name: '연극' },
  { code: 'CCCA', name: '클래식' },
  { code: 'CCCC', name: '오페라' },
  { code: 'CCCD', name: '무용' },
  { code: 'EEEA', name: '복합' },
  { code: 'EEEB', name: '서커스/마술' },
  { code: 'GGGA', name: '대중음악' },
  { code: 'KID', name: '아동' },
]

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
      const response = await apiClient.get('/accounts/users/')
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
    alert('회원가입이 완료되었습니다!')
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

/* 폼 그룹 */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .form-group input,
:root.dark .form-group select {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .form-group input:focus,
:root.dark .form-group select:focus {
  border-color: #818cf8;
  background: #4b5563;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.form-group input::placeholder {
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .form-group input::placeholder {
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

/* 장르 선택 그리드 */
.genre-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.genre-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

:root.dark .genre-checkbox {
  background: #374151;
  border-color: #4b5563;
}

.genre-checkbox:hover {
  border-color: #6366f1;
  background: #f9fafb;
}

:root.dark .genre-checkbox:hover {
  border-color: #818cf8;
  background: #4b5563;
}

.genre-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #6366f1;
}

.genre-checkbox input[type="checkbox"]:checked + .genre-label {
  color: #6366f1;
  font-weight: 600;
}

:root.dark .genre-checkbox input[type="checkbox"]:checked + .genre-label {
  color: #818cf8;
}

.genre-label {
  font-size: 0.875rem;
  color: #374151;
  transition: all 0.3s;
}

:root.dark .genre-label {
  color: #e5e7eb;
}

@media (max-width: 640px) {
  .genre-grid {
    grid-template-columns: repeat(2, 1fr);
  }
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
