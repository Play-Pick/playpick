# Community API 엔드포인트 변경사항

## 리팩토링 개요
- 날짜: 2025-12-22
- 변경 이유: 백엔드 구조 개선 (views/ 폴더 분리)
- 변경 범위: community 앱의 모든 API 엔드포인트가 `/api/community/` 하위로 이동

## 📌 중요: 모든 community 관련 엔드포인트 경로 변경

### 기존 경로 → 새 경로

| 기능 | 기존 경로 | 새 경로 | 변경사항 |
|------|----------|---------|---------|
| **게시글 목록** | `/api/articles/` | `/api/community/articles/` | ✅ 경로 변경 |
| **게시글 상세** | `/api/articles/{id}/` | `/api/community/articles/{id}/` | ✅ 경로 변경 |
| **게시글 작성** | `POST /api/articles/` | `POST /api/community/articles/` | ✅ 경로 변경 |
| **게시글 수정** | `PUT /api/articles/{id}/` | `PUT /api/community/articles/{id}/` | ✅ 경로 변경 |
| **게시글 삭제** | `DELETE /api/articles/{id}/` | `DELETE /api/community/articles/{id}/` | ✅ 경로 변경 |
| **게시글 좋아요** | `POST /api/articles/{id}/like/` | `POST /api/community/articles/{id}/like/` | ✅ 경로 변경 |
| **베스트 리뷰** | `/api/articles/best-reviews/` | `/api/community/articles/best-reviews/` | ✅ 경로 변경 |
| **댓글 목록** | `/api/comments/` | `/api/community/comments/` | ✅ 경로 변경 |
| **댓글 상세** | `/api/comments/{id}/` | `/api/community/comments/{id}/` | ✅ 경로 변경 |
| **댓글 작성** | `POST /api/comments/` | `POST /api/community/comments/` | ✅ 경로 변경 |
| **댓글 수정** | `PUT /api/comments/{id}/` | `PUT /api/community/comments/{id}/` | ✅ 경로 변경 |
| **댓글 삭제** | `DELETE /api/comments/{id}/` | `DELETE /api/community/comments/{id}/` | ✅ 경로 변경 |

---

## 1. Articles API (게시글)

### 기본 CRUD
- `GET /api/community/articles/` - 게시글 목록 조회
  - Query Parameters:
    - `board_type`: 게시판 타입 (GENERAL, PERFORMANCE)
    - `category`: 카테고리 (REVIEW, DISCUSSION, QUESTION, etc.)
    - `performance_mt20id`: 특정 공연의 게시글 필터링
    - `search`: 제목/내용 검색
    - `ordering`: 정렬 (-created_at, created_at, -like_count, like_count)

- `POST /api/community/articles/` - 게시글 작성 (인증 필요)
  - Body: `{ title, content, board_type, category, performance }`

- `GET /api/community/articles/{id}/` - 게시글 상세 조회

- `PUT /api/community/articles/{id}/` - 게시글 수정 (작성자만)

- `PATCH /api/community/articles/{id}/` - 게시글 부분 수정 (작성자만)

- `DELETE /api/community/articles/{id}/` - 게시글 삭제 (작성자만)

### Custom Actions
- `POST /api/community/articles/{id}/like/` - 게시글 좋아요/취소 토글 (인증 필요)
  - Response: `{ is_liked: boolean, like_count: number }`

- `GET /api/community/articles/best-reviews/` - 베스트 관람후기
  - Query Parameters:
    - `limit`: 결과 개수 (기본값: 4)
  - 최근 14일의 후기 중 좋아요 수 기준 정렬
  - Response: `{ success: true, results: [...], count: number }`

---

## 2. Comments API (댓글)

### 기본 CRUD
- `GET /api/community/comments/` - 댓글 목록 조회
  - Query Parameters:
    - `article`: 특정 게시글의 댓글만 조회

- `POST /api/community/comments/` - 댓글 작성 (인증 필요)
  - Body: `{ article, content }`

- `GET /api/community/comments/{id}/` - 댓글 상세 조회

- `PUT /api/community/comments/{id}/` - 댓글 수정 (작성자만)

- `PATCH /api/community/comments/{id}/` - 댓글 부분 수정 (작성자만)

- `DELETE /api/community/comments/{id}/` - 댓글 삭제 (작성자만)

---

## 프론트엔드 수정 필요 파일

다음 경로를 사용하는 파일들을 수정해야 합니다:

### 1. Articles 관련 (경로 변경 필요)
- `/api/articles/` → `/api/community/articles/`

**수정 대상 예상 파일:**
- `front/src/api/community.js` (또는 articles.js)
- 게시글 관련 컴포넌트 (게시판 목록, 상세, 작성 폼 등)
- 베스트 리뷰 컴포넌트

### 2. Comments 관련 (경로 변경 필요)
- `/api/comments/` → `/api/community/comments/`

**수정 대상 예상 파일:**
- `front/src/api/community.js` (또는 comments.js)
- 댓글 관련 컴포넌트

---

## 백엔드 디렉토리 구조 (변경 후)

```
community/
├── views/
│   ├── __init__.py
│   └── api_views.py          # ArticleViewSet, CommentViewSet
├── models.py
├── serializers.py
├── urls.py                   # community 앱 URL 설정
└── admin.py
```

---

## 마이그레이션 체크리스트

### 프론트엔드 개발자
- [ ] `/api/articles/` → `/api/community/articles/` 경로 변경
- [ ] `/api/comments/` → `/api/community/comments/` 경로 변경
- [ ] API 호출 테스트
  - [ ] 게시글 목록 조회
  - [ ] 게시글 상세 조회
  - [ ] 게시글 작성/수정/삭제
  - [ ] 게시글 좋아요
  - [ ] 베스트 리뷰 조회
  - [ ] 댓글 목록 조회
  - [ ] 댓글 작성/수정/삭제

### 백엔드 개발자
- [x] views/ 폴더 생성 및 파일 이동
- [x] community/urls.py 설정
- [x] mypjt/urls.py 수정
- [x] import 경로 수정
- [ ] 서버 재시작 및 동작 확인

---

## 변경 사항 없는 API

다음 API들은 경로 변경이 없습니다:

- `/api/accounts/` - 계정 관련 API
- `/api/performances/` - 공연 관련 API
- `/api/recommendations/` - 추천 API

---

## 예시: 기존 코드 vs 변경 후 코드

### 기존 코드 (변경 전)
```javascript
// front/src/api/community.js
const API_BASE_URL = 'http://localhost:8000/api'

export default {
  // 게시글 목록 조회
  getArticles(params) {
    return axios.get(`${API_BASE_URL}/articles/`, { params })
  },

  // 댓글 목록 조회
  getComments(articleId) {
    return axios.get(`${API_BASE_URL}/comments/`, {
      params: { article: articleId }
    })
  },

  // 베스트 리뷰 조회
  getBestReviews(limit = 4) {
    return axios.get(`${API_BASE_URL}/articles/best-reviews/`, {
      params: { limit }
    })
  }
}
```

### 변경 후 코드
```javascript
// front/src/api/community.js
const API_BASE_URL = 'http://localhost:8000/api'

export default {
  // 게시글 목록 조회
  getArticles(params) {
    return axios.get(`${API_BASE_URL}/community/articles/`, { params })
  },

  // 댓글 목록 조회
  getComments(articleId) {
    return axios.get(`${API_BASE_URL}/community/comments/`, {
      params: { article: articleId }
    })
  },

  // 베스트 리뷰 조회
  getBestReviews(limit = 4) {
    return axios.get(`${API_BASE_URL}/community/articles/best-reviews/`, {
      params: { limit }
    })
  }
}
```

---

## 문의사항

궁금한 점이 있으면 백엔드 팀에게 문의해주세요.
