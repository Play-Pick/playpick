# 프로젝트 구조 및 동작 방식 설명

## 1. Django REST Framework Router 동작 방식

### 기존 방식 (URLConf)
```python
# urls.py
urlpatterns = [
    path('api/performances/', views.performance_list),
    path('api/performances/<int:pk>/', views.performance_detail),
]

# views.py
def performance_list(request):
    if request.method == 'GET':
        # 목록 조회
    elif request.method == 'POST':
        # 생성
```

### 새로운 방식 (DRF Router + ViewSet)
```python
# urls.py
router = DefaultRouter()
router.register(r'performances', PerformanceViewSet, basename='performance')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Router가 자동으로 생성하는 URL들:**
```
GET     /api/performances/              → 목록 조회 (list)
POST    /api/performances/              → 생성 (create)
GET     /api/performances/{id}/         → 상세 조회 (retrieve)
PUT     /api/performances/{id}/         → 전체 수정 (update)
PATCH   /api/performances/{id}/         → 부분 수정 (partial_update)
DELETE  /api/performances/{id}/         → 삭제 (destroy)
```

**추가 액션 (@action 데코레이터):**
```python
# api_views.py
@action(detail=False, methods=['get'])
def genres(self, request):
    # GET /api/performances/genres/
```

## 2. 현재 프로젝트의 API 엔드포인트

### 공연 관련 (PerformanceViewSet)
```
✅ GET /api/performances/              → 공연 목록
✅ GET /api/performances/{id}/         → 공연 상세
✅ GET /api/performances/genres/       → 장르 목록 (커스텀 액션)
```

### 박스오피스 관련 (BoxOfficeRankingViewSet)
```
✅ GET /api/boxoffice/                      → 박스오피스 목록
✅ GET /api/boxoffice/{id}/                 → 박스오피스 상세
✅ GET /api/boxoffice/latest_by_genre/      → 장르별 최신 랭킹
```

### 리뷰 관련 (ReviewViewSet)
```
✅ GET    /api/reviews/           → 리뷰 목록
✅ POST   /api/reviews/           → 리뷰 생성
✅ GET    /api/reviews/{id}/      → 리뷰 상세
✅ PUT    /api/reviews/{id}/      → 리뷰 수정
✅ DELETE /api/reviews/{id}/      → 리뷰 삭제
✅ POST   /api/reviews/{id}/like/ → 좋아요/취소 (커스텀 액션)
```

### 댓글 관련 (CommentViewSet)
```
✅ GET    /api/comments/          → 댓글 목록
✅ POST   /api/comments/          → 댓글 생성
✅ DELETE /api/comments/{id}/     → 댓글 삭제
```

### 사용자 관련 (UserViewSet)
```
✅ GET  /api/users/              → 사용자 목록
✅ GET  /api/users/{id}/         → 사용자 상세
✅ GET  /api/users/me/           → 현재 사용자 정보 (커스텀 액션)
✅ POST /api/users/{id}/follow/  → 팔로우/언팔로우 (커스텀 액션)
```

## 3. Vue3 Axios 사용 방식

### 기존 방식 (직접 axios 사용)
```javascript
// 컴포넌트에서 직접 사용
import axios from 'axios'

axios.get('http://127.0.0.1:8000/api/performances/')
  .then(response => {
    console.log(response.data)
  })
```

### 현재 프로젝트 방식 (Axios 인스턴스 + API 모듈)

**1단계: Axios 인스턴스 생성 (src/api/axios.js)**
```javascript
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // 기본 URL
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true  // CORS 인증 정보 포함
})
```

**2단계: API 함수 정의 (src/api/performances.js)**
```javascript
import apiClient from './axios'

export default {
  getPerformances(params) {
    return apiClient.get('/performances/', { params })
    // 실제 요청: GET http://127.0.0.1:8000/api/performances/
  },

  getPerformance(id) {
    return apiClient.get(`/performances/${id}/`)
    // 실제 요청: GET http://127.0.0.1:8000/api/performances/PF123456/
  }
}
```

**3단계: Pinia 스토어에서 사용 (src/stores/performanceStore.js)**
```javascript
import performanceAPI from '@/api/performances'

export const usePerformanceStore = defineStore('performance', () => {
  const performances = ref([])

  const fetchPerformances = async (params = {}) => {
    const response = await performanceAPI.getPerformances(params)
    performances.value = response.data.results || response.data
  }

  return { performances, fetchPerformances }
})
```

**4단계: Vue 컴포넌트에서 사용**
```javascript
// PerformanceListView.vue
import { usePerformanceStore } from '@/stores/performanceStore'

const performanceStore = usePerformanceStore()

onMounted(async () => {
  await performanceStore.fetchPerformances()
})
```

## 4. 데이터 흐름도

```
┌─────────────────┐
│  Vue Component  │  ← 사용자 인터페이스
└────────┬────────┘
         │
         │ 1. 스토어 액션 호출
         ↓
┌─────────────────┐
│  Pinia Store    │  ← 상태 관리
└────────┬────────┘
         │
         │ 2. API 함수 호출
         ↓
┌─────────────────┐
│  API Module     │  ← API 요청 함수 모음
└────────┬────────┘
         │
         │ 3. Axios 인스턴스 사용
         ↓
┌─────────────────┐
│  Axios Client   │  ← HTTP 요청
└────────┬────────┘
         │
         │ 4. HTTP 요청 (CORS 포함)
         ↓
┌─────────────────┐
│  Django Server  │  ← 백엔드 서버
│  127.0.0.1:8000 │
└────────┬────────┘
         │
         │ 5. Router → ViewSet
         ↓
┌─────────────────┐
│  ViewSet        │  ← API 로직 처리
└────────┬────────┘
         │
         │ 6. Serializer → Model
         ↓
┌─────────────────┐
│  Database       │  ← 데이터 저장소
└─────────────────┘
```

## 5. 실제 요청 예시

### 공연 목록 조회
```
1. 사용자가 /performances 페이지 접속
2. PerformanceListView.vue 마운트
3. performanceStore.fetchPerformances() 호출
4. performanceAPI.getPerformances() 호출
5. apiClient.get('/performances/') 실행
6. HTTP 요청: GET http://127.0.0.1:8000/api/performances/
7. Django Router가 PerformanceViewSet.list() 메소드로 연결
8. Serializer가 데이터를 JSON으로 변환
9. 응답: { "count": 100, "results": [...] }
10. 스토어에 데이터 저장
11. 컴포넌트가 데이터 렌더링
```

### 리뷰 좋아요
```
1. 사용자가 좋아요 버튼 클릭
2. communityStore.likeReview(id) 호출
3. communityAPI.likeReview(id) 호출
4. apiClient.post(`/reviews/${id}/like/`) 실행
5. HTTP 요청: POST http://127.0.0.1:8000/api/reviews/5/like/
6. Django Router가 ReviewViewSet.like() 메소드로 연결
7. 좋아요 토글 처리
8. 응답: { "is_liked": true, "like_count": 10 }
9. 스토어 업데이트
10. UI 반영
```

## 6. CORS 문제 해결 과정

### 문제 상황
```
Access to XMLHttpRequest at 'http://127.0.0.1:8000/api/performances/genres/'
from origin 'http://localhost:5174' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### 해결 방법
```python
# Django settings.py

# 1. CORS 허용 출처
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 2. 인증 정보 포함 허용
CORS_ALLOW_CREDENTIALS = True

# 3. 허용 헤더
CORS_ALLOW_HEADERS = [
    'accept', 'authorization', 'content-type',
    'x-csrftoken', 'x-requested-with',
]

# 4. 허용 메소드
CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

# 5. CSRF 신뢰 출처
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

## 7. 디버깅 체크리스트

### 백엔드 확인
```bash
# Django 서버 실행 확인
http://127.0.0.1:8000/api/

# API 엔드포인트 확인 (브라우저에서 직접 접속)
http://127.0.0.1:8000/api/performances/
http://127.0.0.1:8000/api/reviews/
```

### 프론트엔드 확인
```javascript
// 개발자 도구 Console에서 직접 테스트
fetch('http://127.0.0.1:8000/api/performances/')
  .then(r => r.json())
  .then(data => console.log(data))
```

### CORS 헤더 확인
```
개발자 도구 → Network 탭
요청 선택 → Headers 탭
Response Headers에서 확인:
- access-control-allow-origin: http://localhost:5173
- access-control-allow-credentials: true
```

## 8. 이 프로젝트의 장점

### 기존 방식 문제점
- 컴포넌트마다 axios 직접 사용 → 중복 코드
- baseURL 하드코딩 → 수정 어려움
- 에러 처리 반복 → 유지보수 힘듦

### 현재 방식 장점
✅ **중앙 집중식 관리**: API 로직을 한 곳에서 관리
✅ **재사용성**: 여러 컴포넌트에서 같은 API 함수 사용
✅ **유지보수**: baseURL 변경 시 한 곳만 수정
✅ **인터셉터**: 요청/응답 전처리 (토큰 자동 추가)
✅ **타입 안정성**: API 함수로 타입 추론 가능
✅ **테스트 용이**: API 모듈만 따로 테스트 가능
