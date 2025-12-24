# JWT 인증 시스템 구현 가이드

## 📋 목차
1. [개요](#개요)
2. [구현 과정](#구현-과정)
3. [백엔드 구조](#백엔드-구조)
4. [프론트엔드 구조](#프론트엔드-구조)
5. [데이터 흐름](#데이터-흐름)
6. [트러블슈팅](#트러블슈팅)

---

## 개요

### JWT란?
JWT(JSON Web Token)는 사용자 인증 정보를 안전하게 전달하기 위한 토큰 기반 인증 방식입니다.

**세션 방식 vs JWT 방식**
```
[세션 방식]
1. 로그인 → 서버가 세션 생성 → 세션 ID를 쿠키로 전달
2. 이후 요청 시 쿠키의 세션 ID로 서버에서 사용자 확인
3. 문제점: 서버에 세션 저장 필요, 확장성 낮음

[JWT 방식]
1. 로그인 → 서버가 JWT 토큰 생성 → 클라이언트에 전달
2. 클라이언트가 토큰을 localStorage에 저장
3. 이후 요청 시 토큰을 Authorization 헤더에 포함
4. 서버는 토큰만 검증 (DB 조회 불필요)
5. 장점: 서버 부담 적음, 확장성 좋음
```

### 사용한 기술 스택
- **백엔드**: Django REST Framework + djangorestframework-simplejwt
- **프론트엔드**: Vue 3 + Pinia + Axios
- **인증 방식**: JWT (Access Token + Refresh Token)

---

## 구현 과정

### 1단계: Django 백엔드 설정

#### 1.1 패키지 설치
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

#### 1.2 Django settings.py 설정

**INSTALLED_APPS에 추가**
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]
```

**MIDDLEWARE에 CORS 추가**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware 추가
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

**JWT 인증 설정**
```python
from datetime import timedelta

# REST Framework 기본 인증 방식을 JWT로 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWT 토큰 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),     # Access Token 유효기간: 1시간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh Token 유효기간: 7일
    'ROTATE_REFRESH_TOKENS': True,                   # 토큰 갱신 시 새 Refresh Token 발급
    'AUTH_HEADER_TYPES': ('Bearer',),                # "Bearer {토큰}" 형식
}
```

**CORS 설정**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # Vue dev server 포트
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True  # 쿠키/인증 정보 허용

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5174',
]
```

#### 1.3 회원가입 Serializer 작성

**파일: `back/accounts/serializers.py`**
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """회원가입용 Serializer"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # Django 비밀번호 검증
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': False}
        }

    def validate(self, attrs):
        """비밀번호 확인"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "비밀번호가 일치하지 않습니다."
            })
        return attrs

    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop('password2')  # password2는 검증용이므로 제거
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']  # 자동 해시 처리
        )
        return user
```

#### 1.4 회원가입 View 작성

**파일: `back/accounts/api_views.py`**
```python
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """회원가입 View"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # 누구나 접근 가능

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),   # Access Token
            'refresh': str(refresh),                # Refresh Token
        }, status=status.HTTP_201_CREATED)
```

**주요 포인트:**
- `RefreshToken.for_user(user)`: 사용자 정보로 토큰 생성
- `refresh.access_token`: Access Token 추출
- 회원가입 성공 시 바로 토큰을 발급하여 자동 로그인 효과

#### 1.5 URL 설정

**파일: `back/mypjt/urls.py`**
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.api_views import RegisterView

urlpatterns = [
    # JWT 토큰 발급 (로그인)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT 토큰 갱신
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 회원가입
    path('api/register/', RegisterView.as_view(), name='register'),
]
```

**API 엔드포인트:**
- `POST /api/register/` - 회원가입
- `POST /api/token/` - 로그인 (JWT 토큰 발급)
- `POST /api/token/refresh/` - 토큰 갱신

---

### 2단계: Vue 프론트엔드 설정

#### 2.1 Axios 인스턴스 생성

**파일: `front/src/api/axios.js`**

```javascript
import axios from 'axios'

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // Django API 서버
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // CORS 인증 정보 포함
})

// 요청 인터셉터 - JWT 토큰 자동 추가
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터 - 토큰 만료 시 자동 갱신
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // 401 에러이고, 재시도하지 않은 요청인 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')

        if (refreshToken) {
          // 토큰 갱신 요청
          const response = await axios.post(
            'http://127.0.0.1:8000/api/token/refresh/',
            { refresh: refreshToken }
          )

          const { access } = response.data

          // 새 토큰 저장
          localStorage.setItem('access_token', access)

          // 원래 요청에 새 토큰 적용
          originalRequest.headers.Authorization = `Bearer ${access}`

          // 원래 요청 재시도
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // 토큰 갱신 실패 시 로그아웃 처리
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
```

**인터셉터 동작 원리:**

1. **요청 인터셉터**: 모든 API 요청에 자동으로 `Authorization: Bearer {token}` 헤더 추가
2. **응답 인터셉터**:
   - 401 에러 발생 → Access Token 만료
   - Refresh Token으로 새 Access Token 발급
   - 새 토큰으로 원래 요청 재시도
   - 무한 루프 방지: `_retry` 플래그 사용

#### 2.2 Auth API 모듈

**파일: `front/src/api/auth.js`**
```javascript
import apiClient from './axios'

export default {
  // 회원가입
  register(data) {
    return apiClient.post('/register/', data)
  },

  // 로그인 (JWT 토큰 발급)
  login(credentials) {
    return apiClient.post('/token/', credentials)
  },

  // 토큰 갱신
  refreshToken(refresh) {
    return apiClient.post('/token/refresh/', { refresh })
  },

  // 로그아웃 (클라이언트 측에서 토큰 삭제)
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    return Promise.resolve()
  }
}
```

**주의사항:**
- baseURL이 이미 `/api`를 포함하므로 경로는 `/register/` (O)
- `/api/register/` (X) - 이렇게 하면 `/api/api/register/`가 됨

#### 2.3 Pinia Store 설정

**파일: `front/src/stores/authStore.js`**
```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authAPI from '@/api/auth'
import usersAPI from '@/api/users'

export const useAuthStore = defineStore('auth', () => {
  // 상태
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value)
  const username = computed(() => user.value?.username || '')

  // 회원가입
  const register = async (formData) => {
    const response = await authAPI.register(formData)

    // 토큰 저장
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // 사용자 정보 저장
    user.value = response.data.user
  }

  // 로그인
  const login = async (credentials) => {
    const response = await authAPI.login(credentials)

    // 토큰 저장
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // 사용자 정보 가져오기
    await fetchCurrentUser()
  }

  // 현재 사용자 정보 가져오기
  const fetchCurrentUser = async () => {
    try {
      const response = await usersAPI.getCurrentUser()
      user.value = response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
    }
  }

  // 로그아웃
  const logout = async () => {
    await authAPI.logout()
    user.value = null
    accessToken.value = null
    refreshToken.value = null
  }

  // 앱 초기화 시 토큰 확인
  const initialize = async () => {
    if (accessToken.value) {
      await fetchCurrentUser()
    }
  }

  return {
    user,
    isAuthenticated,
    username,
    register,
    login,
    logout,
    initialize,
  }
})
```

#### 2.4 회원가입 페이지

**파일: `front/src/views/RegisterView.vue`**
```vue
<template>
  <div class="register-view">
    <div class="register-container">
      <h1>회원가입</h1>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">아이디 *</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            placeholder="아이디를 입력하세요"
          />
          <span v-if="errors.username" class="field-error">
            {{ errors.username }}
          </span>
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="이메일을 입력하세요 (선택사항)"
          />
          <span v-if="errors.email" class="field-error">
            {{ errors.email }}
          </span>
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
          <span v-if="errors.password" class="field-error">
            {{ errors.password }}
          </span>
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
          <span v-if="errors.password2" class="field-error">
            {{ errors.password2 }}
          </span>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="btn-register" :disabled="loading">
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
  email: '',
  password: '',
  password2: '',
})

const loading = ref(false)
const errorMessage = ref('')
const errors = ref({})

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
    await authStore.register(formData.value)
    // 회원가입 성공 시 홈으로 이동
    router.push('/')
  } catch (error) {
    console.error('회원가입 실패:', error)

    // 에러 메시지 표시
    if (error.response?.data) {
      const data = error.response.data

      // 필드별 에러 메시지
      if (data.username) {
        errors.value.username = Array.isArray(data.username)
          ? data.username[0]
          : data.username
      }
      if (data.email) {
        errors.value.email = Array.isArray(data.email)
          ? data.email[0]
          : data.email
      }
      if (data.password) {
        errors.value.password = Array.isArray(data.password)
          ? data.password[0]
          : data.password
      }
      if (data.password2) {
        errors.value.password2 = Array.isArray(data.password2)
          ? data.password2[0]
          : data.password2
      }

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
```

#### 2.5 로그인 페이지

**파일: `front/src/views/LoginView.vue`**
```vue
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
        if (data.detail.includes('No active account') ||
            data.detail.includes('credentials')) {
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
```

#### 2.6 App.vue 네비게이션 바

**파일: `front/src/App.vue`**
```vue
<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

// 앱 초기화 시 인증 상태 확인
onMounted(async () => {
  await authStore.initialize()
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/" class="nav-logo">공연 커뮤니티</RouterLink>
        <div class="nav-menu">
          <RouterLink to="/" class="nav-link">홈</RouterLink>
          <RouterLink to="/performances" class="nav-link">공연</RouterLink>
          <RouterLink to="/community" class="nav-link">커뮤니티</RouterLink>

          <!-- 인증 상태에 따른 버튼 -->
          <div class="auth-buttons">
            <template v-if="authStore.isAuthenticated">
              <span class="username">{{ authStore.username }}</span>
              <button @click="handleLogout" class="nav-btn">로그아웃</button>
            </template>
            <template v-else>
              <RouterLink to="/login" class="nav-btn">로그인</RouterLink>
              <RouterLink to="/register" class="nav-btn btn-register">
                회원가입
              </RouterLink>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>
```

---

## 백엔드 구조

### 파일 구조
```
back/
├── mypjt/
│   ├── settings.py          # Django 설정 (JWT, CORS)
│   └── urls.py              # URL 라우팅
└── accounts/
    ├── models.py            # User 모델
    ├── serializers.py       # RegisterSerializer
    └── api_views.py         # RegisterView
```

### 핵심 컴포넌트

#### 1. RegisterSerializer
- **역할**: 회원가입 데이터 검증 및 사용자 생성
- **검증 항목**:
  - 비밀번호 강도 검증 (`validate_password`)
  - 비밀번호 확인 일치 검사
  - 중복 아이디 검사 (자동)

#### 2. RegisterView
- **역할**: 회원가입 API 엔드포인트
- **프로세스**:
  1. 요청 데이터 검증 (`serializer.is_valid()`)
  2. 사용자 생성 (`serializer.save()`)
  3. JWT 토큰 생성 (`RefreshToken.for_user()`)
  4. 응답 반환 (사용자 정보 + 토큰)

#### 3. JWT 엔드포인트
- **TokenObtainPairView**: 로그인 (아이디/비밀번호 → 토큰)
- **TokenRefreshView**: 토큰 갱신 (Refresh Token → 새 Access Token)

---

## 프론트엔드 구조

### 파일 구조
```
front/src/
├── api/
│   ├── axios.js             # Axios 인스턴스 + 인터셉터
│   └── auth.js              # 인증 API 함수
├── stores/
│   └── authStore.js         # Pinia 인증 스토어
├── views/
│   ├── RegisterView.vue     # 회원가입 페이지
│   └── LoginView.vue        # 로그인 페이지
└── App.vue                  # 네비게이션 바
```

### 핵심 컴포넌트

#### 1. Axios 인터셉터
```javascript
요청 인터셉터: 모든 요청에 토큰 자동 추가
  └─ localStorage에서 access_token 가져오기
  └─ Authorization 헤더에 "Bearer {token}" 추가

응답 인터셉터: 토큰 만료 시 자동 갱신
  └─ 401 에러 감지
  └─ Refresh Token으로 새 Access Token 발급
  └─ 원래 요청 재시도
```

#### 2. Pinia authStore
```javascript
상태:
  - user: 현재 로그인한 사용자 정보
  - accessToken: Access Token
  - refreshToken: Refresh Token

주요 메서드:
  - register(): 회원가입
  - login(): 로그인
  - logout(): 로그아웃
  - initialize(): 앱 초기화 시 토큰 확인
  - fetchCurrentUser(): 사용자 정보 가져오기
```

---

## 데이터 흐름

### 회원가입 흐름
```
[Vue] RegisterView.vue
  ↓ (1) 폼 제출
[Pinia] authStore.register(formData)
  ↓ (2) API 호출
[Axios] POST /api/register/
  ↓ (3) 요청
[Django] RegisterView.create()
  ↓ (4) 데이터 검증
[Django] RegisterSerializer.is_valid()
  ↓ (5) 사용자 생성
[Django] User.objects.create_user()
  ↓ (6) JWT 토큰 생성
[Django] RefreshToken.for_user(user)
  ↓ (7) 응답
{
  user: { id, username, email },
  access: "eyJ...",
  refresh: "eyJ..."
}
  ↓ (8) 토큰 저장
[Pinia] localStorage.setItem('access_token', ...)
  ↓ (9) 페이지 이동
[Vue] router.push('/')
```

### 로그인 흐름
```
[Vue] LoginView.vue
  ↓ (1) 폼 제출
[Pinia] authStore.login(credentials)
  ↓ (2) API 호출
[Axios] POST /api/token/
  ↓ (3) 요청
[Django] TokenObtainPairView
  ↓ (4) 아이디/비밀번호 확인
[Django] authenticate(username, password)
  ↓ (5) JWT 토큰 생성
{
  access: "eyJ...",
  refresh: "eyJ..."
}
  ↓ (6) 토큰 저장
[Pinia] localStorage.setItem('access_token', ...)
  ↓ (7) 사용자 정보 가져오기
[Axios] GET /api/users/me/
  ↓ (8) 페이지 이동
[Vue] router.push('/')
```

### 인증된 API 요청 흐름
```
[Vue] 컴포넌트에서 API 호출
  ↓
[Axios] apiClient.get('/some-api/')
  ↓ (요청 인터셉터)
Authorization 헤더 추가: "Bearer {access_token}"
  ↓
[Django] JWT 인증 미들웨어
  ↓
토큰 검증 → 사용자 확인 → 요청 처리
  ↓
[Vue] 응답 데이터 받음
```

### 토큰 만료 시 자동 갱신 흐름
```
[Axios] API 요청
  ↓
[Django] 401 Unauthorized (Access Token 만료)
  ↓
[Axios] 응답 인터셉터 감지
  ↓
[Axios] POST /api/token/refresh/
       { refresh: "eyJ..." }
  ↓
[Django] TokenRefreshView
  ↓
새 Access Token 발급
{ access: "새토큰..." }
  ↓
[Axios] localStorage 업데이트
  ↓
[Axios] 원래 요청 재시도 (새 토큰 사용)
  ↓
[Django] 요청 처리 성공
```

---

## 트러블슈팅

### 문제 1: CORS 에러
**증상**
```
Access to XMLHttpRequest at 'http://127.0.0.1:8000/api/register/'
from origin 'http://localhost:5174' has been blocked by CORS policy
```

**원인**
- Django CORS 설정에서 Vue 개발 서버 포트가 허용되지 않음
- Vue 앱이 포트 5174에서 실행 중이지만 설정은 5173만 허용

**해결**
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # 추가
    "http://127.0.0.1:5174",  # 추가
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # 추가
    "http://127.0.0.1:5174",  # 추가
]
```

### 문제 2: API 경로 중복 (`/api/api/register/`)
**증상**
```
POST /api/api/register/ 404 Not Found
```

**원인**
- `axios.js`의 `baseURL`이 이미 `/api` 포함
- `auth.js`에서 또 `/api/register/` 사용

**해결**
```javascript
// ❌ 잘못된 코드
export default {
  register(data) {
    return apiClient.post('/api/register/', data)  // 중복!
  }
}

// ✅ 올바른 코드
export default {
  register(data) {
    return apiClient.post('/register/', data)  // baseURL에 /api가 있음
  }
}
```

### 문제 3: "No active account found" 에러 메시지
**증상**
- 잘못된 로그인 시 영어 에러 메시지 표시

**원인**
- Django JWT가 기본으로 영어 메시지 반환

**해결**
```javascript
// LoginView.vue
if (data.detail) {
  // JWT 에러 메시지를 한글로 변환
  if (data.detail.includes('No active account') ||
      data.detail.includes('credentials')) {
    errorMessage.value = '아이디 또는 비밀번호를 확인할 수 없습니다.'
  } else {
    errorMessage.value = data.detail
  }
}
```

### 문제 4: RegisterSerializer import 에러
**증상**
```python
ImportError: cannot import name 'RegisterSerializer' from 'accounts.serializers'
```

**원인**
- `serializers.py`에 `RegisterSerializer` 클래스가 없음

**해결**
- `accounts/serializers.py`에 `RegisterSerializer` 클래스 추가
- `accounts/api_views.py`에서 import 확인

### 문제 5: 토큰 갱신 무한 루프
**증상**
- 401 에러 시 토큰 갱신이 무한 반복

**원인**
- `_retry` 플래그가 없어서 같은 요청을 계속 재시도

**해결**
```javascript
// axios.js 응답 인터셉터
if (error.response?.status === 401 && !originalRequest._retry) {
  originalRequest._retry = true  // 무한 루프 방지
  // ... 토큰 갱신 로직
}
```

---

## 보안 고려사항

### 1. 토큰 저장 위치
**현재 방식: localStorage**
```javascript
✅ 장점:
- 탭/브라우저 닫아도 유지됨
- 구현이 간단함
- JavaScript에서 쉽게 접근 가능

❌ 단점:
- XSS 공격에 취약할 수 있음
```

**보안 강화 방법:**
1. HTTPS 사용 필수
2. XSS 방지 (사용자 입력 sanitize)
3. 짧은 토큰 만료 시간 설정 (1시간)
4. Refresh Token 분리 (7일)

### 2. 비밀번호 검증
```python
# Django의 validate_password 사용
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### 3. CORS 설정
```python
# 프로덕션 환경에서는 구체적인 도메인만 허용
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",  # 실제 도메인으로 변경
]
```

---

## 테스트 방법

### 1. 회원가입 테스트
```javascript
// 브라우저 콘솔
// 1. 회원가입
fetch('http://127.0.0.1:8000/api/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    password: 'testpass123',
    password2: 'testpass123'
  })
})
.then(res => res.json())
.then(data => console.log(data))

// 2. 토큰 확인
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
```

### 2. 로그인 테스트
```javascript
// 브라우저 콘솔
fetch('http://127.0.0.1:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    password: 'testpass123'
  })
})
.then(res => res.json())
.then(data => console.log(data))
```

### 3. 토큰 검증
```javascript
// https://jwt.io 에서 토큰 디코딩
const token = localStorage.getItem('access_token')
// jwt.io에 붙여넣기

// Payload 확인:
{
  "user_id": 1,
  "username": "testuser",
  "exp": 1234567890  // 만료 시간
}
```

---

## 참고 자료

- [Django REST Framework JWT 공식 문서](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT 소개](https://jwt.io/introduction)
- [Vue 3 공식 문서](https://vuejs.org/)
- [Pinia 공식 문서](https://pinia.vuejs.org/)
- [Axios 공식 문서](https://axios-http.com/)
