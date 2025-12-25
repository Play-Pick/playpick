# 프론트엔드 API 호출 리팩토링 가이드

## 문제점
현재 많은 Vue 컴포넌트에서 `apiClient`를 직접 import하여 사용하고 있습니다.
이미 `src/api/` 폴더에 API 함수들이 정의되어 있지만 활용되지 않고 있습니다.

## 리팩토링 원칙
- `apiClient`를 직접 사용하지 말고, `src/api/` 모듈의 함수를 사용
- 코드 재사용성 향상
- API 엔드포인트 변경 시 한 곳만 수정하면 됨
- 타입 안정성 및 유지보수성 향상

---

## 수정이 필요한 파일 목록

### 1. PerformanceDetailView.vue
**위치**: `src/views/Performance/PerformanceDetailView.vue`

**문제**:
- Line 258: `apiClient.get('/community/articles/')` 직접 사용

**수정 방법**:
```javascript
// 현재 (잘못된 방식)
import apiClient from '@/api/axios'

const loadReviews = async () => {
  const response = await apiClient.get('/community/articles/')
  const allArticles = response.data.results || response.data
  reviews.value = allArticles.filter(
    article => article.performance === route.params.id
  )
}

// 수정 후 (올바른 방식)
import communityAPI from '@/api/community'

const loadReviews = async () => {
  const response = await communityAPI.getArticles({
    performance_mt20id: route.params.id,
    board_type: 'PERFORMANCE',
    category: 'REVIEW'
  })
  reviews.value = response.data.results || response.data
}
```

**참고**: `community.js`의 `getArticles()` 함수는 이미 params를 지원함

---

### 2. ReviewList.vue
**위치**: `src/components/PerformanceDetail/ReviewList.vue`

**예상 문제**: apiClient 직접 사용 (2회)

**수정 방법**:
```javascript
// import 변경
import communityAPI from '@/api/community'

// 게시글 조회 시
communityAPI.getArticles(params)

// 좋아요 토글 시
communityAPI.likeArticle(articleId)
```

---

### 3. ReviewForm.vue
**위치**: `src/components/PerformanceDetail/ReviewForm.vue`

**예상 문제**: apiClient 직접 사용 (1회)

**수정 방법**:
```javascript
// import 변경
import communityAPI from '@/api/community'

// 리뷰 생성 시
communityAPI.createArticle(data)

// 리뷰 수정 시
communityAPI.updateArticle(id, data)
```

---

### 4. CommunityWriteView.vue
**위치**: `src/views/Community/CommunityWriteView.vue`

**예상 문제**: apiClient 직접 사용 (2회)

**수정 방법**:
```javascript
import communityAPI from '@/api/community'

// 게시글 작성
communityAPI.createArticle(data)

// 게시글 수정
communityAPI.updateArticle(id, data)
```

---

### 5. MyPageView.vue
**위치**: `src/views/User/MyPageView.vue`

**예상 문제**: apiClient 직접 사용 (5회)

**수정 방법**:
```javascript
// 여러 API 모듈 import
import authAPI from '@/api/auth'
import communityAPI from '@/api/community'
import wishlistAPI from '@/api/wishlist'
import watchedAPI from '@/api/watched'

// 사용자 정보 조회
authAPI.getCurrentUser()

// 내가 쓴 글 조회
communityAPI.getArticles({ user: userId })

// 찜한 공연 조회
wishlistAPI.getWishlist()

// 본 공연 조회
watchedAPI.getWatchedPerformances()
```

---

### 6. EditAccountView.vue
**위치**: `src/views/User/EditAccountView.vue`

**예상 문제**: apiClient 직접 사용 (3회)

**수정 방법**:
```javascript
import authAPI from '@/api/auth'

// 사용자 정보 조회
authAPI.getCurrentUser()

// 사용자 정보 수정
authAPI.updateProfile(userId, data)

// 비밀번호 변경
authAPI.changePassword(data)
```

---

### 7. RegisterView.vue
**위치**: `src/views/Auth/RegisterView.vue`

**예상 문제**: apiClient 직접 사용 (1회)

**수정 방법**:
```javascript
import authAPI from '@/api/auth'

// 회원가입
authAPI.register(userData)
```

---

### 8. AdminDashboardView.vue
**위치**: `src/views/Admin/AdminDashboardView.vue`

**예상 문제**: apiClient 직접 사용 (6회)

**참고**: Admin 전용 API 모듈이 없는 경우 `src/api/admin.js` 생성 필요

**수정 방법**:
```javascript
// 1. src/api/admin.js 생성
import apiClient from './axios'

export default {
  collectBoxOffice() {
    return apiClient.post('/performances/management/collect-boxoffice/')
  },

  collectPerformances() {
    return apiClient.post('/performances/management/collect-performances/')
  },

  collectPerformanceDetail(mt20id) {
    return apiClient.post('/performances/management/collect-performance-detail/', { mt20id })
  },

  getDataStats() {
    return apiClient.get('/performances/management/data-stats/')
  }

  // ... 기타 관리자 API
}

// 2. AdminDashboardView.vue에서 사용
import adminAPI from '@/api/admin'

adminAPI.collectBoxOffice()
adminAPI.getDataStats()
```

---

### 9. TestAPIView.vue
**위치**: `src/views/TestAPIView.vue`

**수정 방법**: 테스트 목적이면 그대로 유지 가능 (선택)

---

## 기존 API 모듈 목록

현재 `src/api/` 폴더에 이미 정의된 모듈들:

1. **auth.js** - 인증 관련
   - `login()`, `logout()`, `register()`, `getCurrentUser()`, `updateProfile()`, `changePassword()` 등

2. **community.js** - 커뮤니티 관련
   - `getArticles()`, `getArticle()`, `createArticle()`, `updateArticle()`, `deleteArticle()`
   - `likeArticle()`, `getBestReviews()`
   - `getComments()`, `createComment()`, `updateComment()`, `deleteComment()`

3. **performances.js** - 공연 관련
   - `getPerformances()`, `getPerformance()`, `searchPerformances()`, `getBoxOffice()`

4. **wishlist.js** - 찜 관련
   - `getWishlist()`, `addWishlist()`, `removeWishlist()`, `checkWishlist()`

5. **watched.js** - 봤어요 관련
   - `getWatchedPerformances()`, `addWatched()`, `removeWatched()`, `checkWatched()`

6. **recommendations.js** - 추천 관련
   - `getRecommendations()`, `refreshRecommendations()`, `saveUserLog()`

7. **onboarding.js** - 온보딩 관련
   - `getCandidates()`, `saveSignals()`, `completeOnboarding()`

8. **youtube.js** - YouTube 관련
   - `getPlaylistVideos()`, `getPerformanceVideo()`

9. **users.js** - 사용자 관련 (auth.js와 중복 가능성 확인 필요)

---

## 추가 생성이 필요한 API 모듈

### src/api/admin.js (신규 생성)
관리자 전용 API를 위한 모듈

```javascript
import apiClient from './axios'

export default {
  // 박스오피스 수집
  collectBoxOffice() {
    return apiClient.post('/performances/management/collect-boxoffice/')
  },

  // 공연 목록 수집
  collectPerformances(params) {
    return apiClient.post('/performances/management/collect-performances/', params)
  },

  // 공연 상세 수집
  collectPerformanceDetail(mt20id) {
    return apiClient.post('/performances/management/collect-performance-detail/', { mt20id })
  },

  // 테스트 박스오피스 생성
  createTestBoxOffice() {
    return apiClient.post('/performances/management/create-test-boxoffice/')
  },

  // 데이터 통계 조회
  getDataStats() {
    return apiClient.get('/performances/management/data-stats/')
  }
}
```

---

## 리팩토링 순서 (권장)

1. **단순한 것부터 시작**
   - RegisterView.vue (1회)
   - ReviewForm.vue (1회)

2. **중간 복잡도**
   - EditAccountView.vue (3회)
   - CommunityWriteView.vue (2회)
   - ReviewList.vue (2회)

3. **복잡한 것**
   - PerformanceDetailView.vue (1회지만 로직 수정 필요)
   - MyPageView.vue (5회, 여러 API 모듈 사용)

4. **관리자**
   - admin.js 모듈 생성
   - AdminDashboardView.vue (6회)

---

## 검증 방법

각 파일 수정 후:

1. **import 확인**
   ```javascript
   // AS-IS: apiClient 직접 사용
   import apiClient from '@/api/axios'

   // TO-BE: API 모듈 사용
   import communityAPI from '@/api/community'
   import authAPI from '@/api/auth'
   ```

2. **함수 호출 확인**
   ```javascript
   // AS-IS
   apiClient.get('/community/articles/')
   apiClient.post('/community/articles/', data)

   // TO-BE
   communityAPI.getArticles()
   communityAPI.createArticle(data)
   ```

3. **브라우저 테스트**
   - 각 기능이 정상 작동하는지 확인
   - Network 탭에서 API 호출 확인

---

## 예외 사항

다음 파일들은 `apiClient` 직접 사용이 허용됨:

1. **src/api/*.js** - API 모듈 내부에서는 당연히 apiClient 사용
2. **src/api/axios.js** - axios 인스턴스 정의 파일
3. **TestAPIView.vue** - 테스트 목적이면 그대로 유지 가능

---

## 완료 체크리스트

- [ ] RegisterView.vue
- [ ] ReviewForm.vue
- [ ] EditAccountView.vue
- [ ] CommunityWriteView.vue
- [ ] ReviewList.vue
- [ ] PerformanceDetailView.vue
- [ ] MyPageView.vue
- [ ] admin.js 모듈 생성
- [ ] AdminDashboardView.vue
- [ ] 전체 기능 테스트

---

## 참고 링크

- API 모듈 위치: `src/api/`
- 백엔드 API 문서:
  - `back/performances/API_ENDPOINTS.md`
  - `back/community/API_ENDPOINTS.md`
  - `back/recommendations/API_ENDPOINTS.md`
