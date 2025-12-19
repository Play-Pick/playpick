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
            <label for="nickname">닉네임</label>
            <input
              id="nickname"
              v-model="formData.nickname"
              type="text"
              placeholder="닉네임을 입력하세요 (선택사항)"
            />
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
            <span class="field-help">공연 추천 알고리즘에 활용됩니다</span>
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
            선호 정보 (선택사항)
          </h3>
          <p class="section-description">맞춤 공연을 추천받을 수 있습니다</p>

          <div class="form-group">
            <label for="preference_tags">선호 장르/분위기</label>
            <div class="tags-input-wrapper">
              <div class="tags-list">
                <span
                  v-for="(tag, index) in formData.preference_tags"
                  :key="index"
                  class="tag"
                >
                  {{ tag }}
                  <i class="fas fa-times" @click="removeTag('preference_tags', index)"></i>
                </span>
              </div>
              <input
                v-model="preferenceTagInput"
                type="text"
                placeholder="태그 입력 후 Enter (예: 뮤지컬, 로맨틱)"
                @keypress.enter.prevent="addTag('preference_tags')"
                class="tag-input"
              />
            </div>
            <span class="field-help">
              <i class="fas fa-info-circle"></i>
              태그를 입력하고 Enter를 누르세요
            </span>
          </div>

          <div class="form-group">
            <label for="favorite_actors">선호 배우</label>
            <div class="tags-input-wrapper">
              <div class="tags-list">
                <span
                  v-for="(actor, index) in formData.favorite_actors"
                  :key="index"
                  class="tag actor-tag"
                >
                  {{ actor }}
                  <i class="fas fa-times" @click="removeTag('favorite_actors', index)"></i>
                </span>
              </div>
              <input
                v-model="actorInput"
                type="text"
                placeholder="배우 이름 입력 후 Enter (예: 조승우)"
                @keypress.enter.prevent="addTag('favorite_actors')"
                class="tag-input"
              />
            </div>
            <span class="field-help">
              <i class="fas fa-info-circle"></i>
              좋아하는 배우를 추가하세요
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
  favorite_actors: [],
})

const loading = ref(false)
const errorMessage = ref('')
const errors = ref({})

// 태그 입력
const preferenceTagInput = ref('')
const actorInput = ref('')

// 태그 추가
const addTag = (field) => {
  const input = field === 'preference_tags' ? preferenceTagInput : actorInput
  const value = input.value.trim()

  if (value && !formData.value[field].includes(value)) {
    formData.value[field].push(value)
    input.value = ''
  }
}

// 태그 제거
const removeTag = (field, index) => {
  formData.value[field].splice(index, 1)
}

const handleRegister = async () => {
  loading.value = true
  errorMessage.value = ''
  errors.value = {}

  // 클라이언트 측 유효성 검사
  if (formData.value.password !== formData.value.password2) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.'
    loading.value = false
    return
  }

  try {
    // 빈 값 제거 및 데이터 정리
    const submitData = {
      username: formData.value.username,
      password: formData.value.password,
      password2: formData.value.password2,
    }

    // 선택 필드는 값이 있을 때만 포함
    if (formData.value.nickname) submitData.nickname = formData.value.nickname
    if (formData.value.email) submitData.email = formData.value.email
    if (formData.value.birth_date) submitData.birth_date = formData.value.birth_date
    if (formData.value.region) submitData.region = formData.value.region
    if (formData.value.preference_tags.length > 0) {
      submitData.preference_tags = formData.value.preference_tags
    }
    if (formData.value.favorite_actors.length > 0) {
      submitData.favorite_actors = formData.value.favorite_actors
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
}

.register-container {
  width: 100%;
  max-width: 600px;
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.register-container h1 {
  text-align: center;
  margin-bottom: 0.5rem;
  color: #1f2937;
  font-size: 2rem;
}

.subtitle {
  text-align: center;
  color: #6b7280;
  margin-bottom: 2rem;
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
}

.section-title {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title i {
  color: #6366f1;
}

.section-description {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
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
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.field-error {
  color: #ef4444;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.field-help {
  color: #6b7280;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.field-help i {
  color: #9ca3af;
}

/* 태그 입력 */
.tags-input-wrapper {
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem;
  background: white;
  transition: all 0.3s;
}

.tags-input-wrapper:focus-within {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  font-size: 0.875rem;
  font-weight: 500;
}

.actor-tag {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.tag i {
  cursor: pointer;
  transition: transform 0.2s;
}

.tag i:hover {
  transform: scale(1.2);
}

.tag-input {
  width: 100%;
  border: none;
  outline: none;
  padding: 0.5rem;
  font-size: 1rem;
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

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Footer */
.footer-links {
  margin-top: 1.5rem;
  text-align: center;
}

.footer-links p {
  color: #6b7280;
  font-size: 0.875rem;
}

.footer-links a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
}

.footer-links a:hover {
  text-decoration: underline;
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
