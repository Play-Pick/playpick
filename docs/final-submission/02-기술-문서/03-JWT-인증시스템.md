# JWT 인증 시스템 가이드

## 1. JWT란?

**JWT (JSON Web Token)**는 인증에 사용되는 토큰 기반 인증 방식입니다.

### 기존 세션 방식 vs JWT 방식

#### 세션 방식
```
1. 로그인 → 서버가 세션 생성 → 세션 ID를 쿠키로 전달
2. 이후 요청 시 쿠키의 세션 ID로 서버에서 사용자 확인
3. 문제점: 서버에 세션 저장 필요, 확장성 낮음
```

#### JWT 방식
```
1. 로그인 → 서버가 JWT 토큰 생성 → 클라이언트에 전달
2. 클라이언트가 토큰을 localStorage에 저장
3. 이후 요청 시 토큰을 헤더에 포함
4. 서버는 토큰만 검증 (DB 조회 불필요)
5. 장점: 서버 부담 적음, 확장성 좋음
```

## 2. 이 프로젝트의 JWT 흐름

### 회원가입
```
[Vue 클라이언트]                           [Django 서버]
     │                                           │
     │  1. POST /api/register/                  │
     │     { username, email, password }        │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                    2. 사용자 생성
     │                                    3. JWT 토큰 발급
     │                                           │
     │  4. Response                              │
     │     {                                     │
     │       user: {...},                        │
     │       access: "eyJ...",  ← Access Token   │
     │       refresh: "eyJ..." ← Refresh Token   │
     │     }                                     │
     │<──────────────────────────────────────────┤
     │                                           │
5. localStorage에 저장:                         │
   - access_token                               │
   - refresh_token                              │
```

### 로그인
```
[Vue 클라이언트]                           [Django 서버]
     │                                           │
     │  1. POST /api/token/                     │
     │     { username, password }               │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                    2. 사용자 인증
     │                                    3. JWT 토큰 발급
     │                                           │
     │  4. Response                              │
     │     {                                     │
     │       access: "eyJ...",                   │
     │       refresh: "eyJ..."                   │
     │     }                                     │
     │<──────────────────────────────────────────┤
     │                                           │
5. localStorage에 저장                          │
6. GET /api/users/me/ (사용자 정보 가져오기)    │
```

### 인증이 필요한 API 요청
```
[Vue 클라이언트]                           [Django 서버]
     │                                           │
     │  1. GET /api/reviews/                    │
     │     Headers:                              │
     │       Authorization: Bearer eyJ...        │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                    2. JWT 토큰 검증
     │                                    3. 사용자 확인
     │                                    4. 데이터 반환
     │                                           │
     │  5. Response { ... }                     │
     │<──────────────────────────────────────────┤
```

### 토큰 만료 시 자동 갱신
```
[Vue 클라이언트]                           [Django 서버]
     │                                           │
     │  1. GET /api/reviews/                    │
     │     Authorization: Bearer [만료된토큰]    │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                    2. 토큰 만료 확인
     │                                           │
     │  3. 401 Unauthorized                     │
     │<──────────────────────────────────────────┤
     │                                           │
4. Axios 인터셉터가 자동 실행                   │
     │                                           │
     │  5. POST /api/token/refresh/             │
     │     { refresh: "eyJ..." }                │
     ├──────────────────────────────────────────>│
     │                                           │
     │                                    6. 새 Access Token 발급
     │                                           │
     │  7. Response                              │
     │     { access: "새토큰..." }               │
     │<──────────────────────────────────────────┤
     │                                           │
8. localStorage 업데이트                        │
9. 원래 요청 재시도 (새 토큰 사용)              │
```

## 3. 코드 구조

### Django 백엔드

#### settings.py - JWT 설정
```python
# JWT 인증을 최우선으로 사용
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWT 토큰 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),     # 1시간 후 만료
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # 7일 후 만료
    'ROTATE_REFRESH_TOKENS': True,                   # 갱신 시 새 Refresh Token 발급
    'AUTH_HEADER_TYPES': ('Bearer',),                # "Bearer 토큰" 형식
}
```

#### URL 엔드포인트
```python
urlpatterns = [
    # JWT 토큰 발급 (로그인)
    path('api/token/', TokenObtainPairView.as_view()),

    # JWT 토큰 갱신
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 회원가입
    path('api/register/', RegisterView.as_view()),
]
```

### Vue 프론트엔드

#### axios.js - 토큰 자동 추가
```javascript
// 모든 요청에 자동으로 토큰 추가
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

#### axios.js - 토큰 만료 시 자동 갱신
```javascript
// 401 에러 시 자동으로 토큰 갱신
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh Token으로 새 Access Token 발급
      const refreshToken = localStorage.getItem('refresh_token')
      const response = await axios.post('/api/token/refresh/', {
        refresh: refreshToken
      })

      // 새 토큰 저장
      localStorage.setItem('access_token', response.data.access)

      // 원래 요청 재시도
      return apiClient(error.config)
    }
  }
)
```

#### authStore.js - 인증 상태 관리
```javascript
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))

  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (credentials) => {
    // 1. JWT 토큰 발급
    const response = await authAPI.login(credentials)

    // 2. 토큰 저장
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // 3. 사용자 정보 가져오기
    await fetchCurrentUser()
  }

  return { user, isAuthenticated, login }
})
```

## 4. 사용 예시

### 회원가입
```javascript
// RegisterView.vue
const handleRegister = async () => {
  await authStore.register({
    username: 'user1',
    email: 'user1@example.com',
    password: 'password123',
    password2: 'password123'
  })

  // 자동으로 토큰 저장됨
  // 자동으로 로그인 상태가 됨
}
```

### 로그인
```javascript
// LoginView.vue
const handleLogin = async () => {
  await authStore.login({
    username: 'user1',
    password: 'password123'
  })

  // 성공 시 홈으로 이동
  router.push('/')
}
```

### 인증이 필요한 API 호출
```javascript
// 컴포넌트에서
const createReview = async () => {
  // axios 인터셉터가 자동으로 토큰을 헤더에 추가
  await communityAPI.createReview({
    title: '리뷰 제목',
    content: '리뷰 내용'
  })
}
```

### 로그아웃
```javascript
const handleLogout = async () => {
  await authStore.logout()

  // localStorage에서 토큰 삭제
  // 상태 초기화
  // 로그인 페이지로 이동
}
```

## 5. 토큰 저장 위치

### localStorage vs sessionStorage vs Cookie

이 프로젝트는 **localStorage** 사용:

```javascript
// 장점
✅ 탭/브라우저 닫아도 유지됨
✅ 구현이 간단함
✅ JavaScript에서 쉽게 접근 가능

// 단점
❌ XSS 공격에 취약할 수 있음 (주의 필요)
```

### 보안 고려사항
```javascript
// 1. HTTPS 사용 필수
// 2. XSS 방지 (사용자 입력 sanitize)
// 3. 토큰 만료 시간 설정 (1시간)
// 4. Refresh Token 분리 (7일)
```

## 6. API 엔드포인트 정리

```
POST   /api/register/           # 회원가입
POST   /api/token/              # 로그인 (JWT 발급)
POST   /api/token/refresh/      # 토큰 갱신
GET    /api/users/me/           # 현재 사용자 정보
```

## 7. 디버깅 방법

### 토큰 확인
```javascript
// 브라우저 Console에서
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
```

### 토큰 디코딩 (jwt.io)
```
1. https://jwt.io/ 접속
2. 토큰 붙여넣기
3. Payload 확인:
   {
     "user_id": 1,
     "username": "user1",
     "exp": 1234567890  // 만료 시간
   }
```

### 네트워크 요청 확인
```
개발자 도구 → Network 탭
1. 요청 헤더에 Authorization: Bearer ... 확인
2. 응답 코드 확인 (200 성공, 401 인증 실패)
```

## 8. 문제 해결

### 로그인 후에도 인증 안됨
```javascript
// authStore.js에서 initialize 호출 확인
onMounted(async () => {
  await authStore.initialize()
})
```

### 토큰 갱신 무한 루프
```javascript
// axios.js에서 _retry 플래그 확인
if (error.response?.status === 401 && !originalRequest._retry) {
  originalRequest._retry = true
  // 갱신 로직
}
```

### CORS 오류
```python
# Django settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```
