<template>
  <div class="login-view">
    <div class="login-container">
      <h1>로그인</h1>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            required
            placeholder="아이디를 입력하세요"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            required
            placeholder="비밀번호를 입력하세요"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="btn-login" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </form>

      <div class="footer-links">
        <p>
          계정이 없으신가요?
          <router-link to="/register">회원가입</router-link>
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

const credentials = ref({
  username: '',
  password: '',
})

const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(credentials.value)

    // 로그인 성공 시 홈으로 이동
    router.push('/')
  } catch (error) {
    console.error('로그인 실패:', error)

    // 에러 메시지 표시
    if (error.response?.data) {
      const data = error.response.data
      if (data.detail) {
        // JWT 에러 메시지를 한글로 변환
        if (data.detail.includes('No active account') || data.detail.includes('credentials')) {
          errorMessage.value = '아이디 또는 비밀번호를 확인할 수 없습니다.'
        } else {
          errorMessage.value = data.detail
        }
      } else if (data.non_field_errors) {
        errorMessage.value = data.non_field_errors[0]
      } else {
        errorMessage.value = '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.'
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
.login-view {
  min-height: calc(100vh - 200px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-container h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.login-form {
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
  color: #2c3e50;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #42b983;
}

.error-message {
  padding: 0.75rem;
  background-color: #fee;
  color: #c00;
  border: 1px solid #fcc;
  border-radius: 4px;
  font-size: 0.875rem;
}

.btn-login {
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-login:hover:not(:disabled) {
  background-color: #359268;
}

.btn-login:disabled {
  background-color: #95c9af;
  cursor: not-allowed;
}

.footer-links {
  margin-top: 1.5rem;
  text-align: center;
}

.footer-links p {
  color: #666;
  font-size: 0.875rem;
}

.footer-links a {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}

.footer-links a:hover {
  text-decoration: underline;
}
</style>
