# Performances API 엔드포인트 변경사항

## 리팩토링 개요
- 날짜: 2025-12-22
- 변경 이유: 백엔드 구조 개선 (views/, services/ 폴더 분리)
- 변경 범위: performances 앱의 모든 API 엔드포인트가 `/api/performances/` 하위로 이동

## 📌 중요: 모든 performances 관련 엔드포인트 경로 변경

### 기존 경로 → 새 경로

| 기능 | 기존 경로 | 새 경로 | 변경사항 |
|------|----------|---------|---------|
| **공연 목록** | `/api/performances/` | `/api/performances/` | 변경 없음 |
| **공연 상세** | `/api/performances/{id}/` | `/api/performances/{id}/` | 변경 없음 |
| **박스오피스 전체** | `/api/boxoffice/` | `/api/performances/boxoffice/` | ✅ 경로 변경 |
| **관리자 API** | `/api/management/...` | `/api/performances/management/...` | ✅ 경로 변경 |

---

## 1. 공연 정보 API (PerformanceViewSet)

### 기본 CRUD
- `GET /api/performances/` - 공연 목록 조회
- `GET /api/performances/{mt20id}/` - 공연 상세 조회

### Custom Actions
- `GET /api/performances/boxoffice-genre/?genre=BBBC` - 장르별 박스오피스 랭킹
- `GET /api/performances/boxoffice-all/` - 전체 박스오피스 Top 10 (좌석수 기준)
- `GET /api/performances/boxoffice-highlight/` - 하이라이트 캐러셀용 Top 8
- `GET /api/performances/genres/` - 장르 목록
- `GET /api/performances/search-autocomplete/?query={query}` - 자동완성 검색
- `GET /api/performances/liked/` - 내가 찜한 공연 (인증 필요)
- `POST /api/performances/{mt20id}/like/` - 공연 찜하기/취소 토글 (인증 필요)
- `GET /api/performances/watched/` - 내가 관람한 공연 (인증 필요)
- `POST /api/performances/{mt20id}/watch/` - 관람함 추가 (인증 필요)
- `DELETE /api/performances/{mt20id}/watch/` - 관람함 해제 (인증 필요)
- `POST /api/performances/ai-search/` - AI 의미 기반 검색
- `GET /api/performances/youtube/playlist/` - YouTube 플레이리스트 영상
- `GET /api/performances/{mt20id}/youtube/` - 공연 관련 YouTube 영상

---

## 2. 박스오피스 랭킹 API (BoxOfficeRankingViewSet)

**⚠️ 경로 변경됨**

### 기존 경로
```
/api/boxoffice/
```

### 새 경로
```
/api/performances/boxoffice/
```

### 엔드포인트
- `GET /api/performances/boxoffice/` - 박스오피스 랭킹 목록
- `GET /api/performances/boxoffice/{id}/` - 특정 랭킹 조회
- `GET /api/performances/boxoffice/latest_by_genre/?genre_code=BBBC` - 장르별 최신 랭킹

---

## 3. 관리자 전용 API (Management APIs)

**⚠️ 경로 변경됨**

### 기존 경로
```
/api/management/...
```

### 새 경로
```
/api/performances/management/...
```

### 엔드포인트
- `POST /api/performances/management/collect-boxoffice/` - 박스오피스 데이터 수집
- `POST /api/performances/management/collect-performances/` - 공연 정보 수집
- `POST /api/performances/management/collect-details/` - 공연 상세 정보 수집
- `POST /api/performances/management/create-test-boxoffice/` - 테스트 박스오피스 데이터 생성
- `GET /api/performances/management/stats/` - 데이터 통계 조회

---

## 프론트엔드 수정 필요 파일

다음 경로를 사용하는 파일들을 수정해야 합니다:

### 1. BoxOffice 관련 (경로 변경 필요)
- `/api/boxoffice/` → `/api/performances/boxoffice/`

**수정 대상:**
- `front/src/api/performances.js` (또는 boxoffice.js)
- 박스오피스 관련 컴포넌트

### 2. Management API 관련 (경로 변경 필요)
- `/api/management/...` → `/api/performances/management/...`

**수정 대상:**
- 관리자 페이지/컴포넌트 (있는 경우)

---

## 백엔드 디렉토리 구조 (변경 후)

```
performances/
├── views/
│   ├── __init__.py
│   ├── api_views.py          # PerformanceViewSet, BoxOfficeRankingViewSet
│   └── management_api_views.py  # 관리자 전용 API
├── services/
│   ├── __init__.py
│   ├── ai_search.py          # AI 검색 엔진
│   └── youtube_service.py    # YouTube 서비스
├── models.py
├── serializers.py
├── urls.py                   # performances 앱 URL 설정
└── management/
    └── commands/
```

---

## 마이그레이션 체크리스트

### 프론트엔드 개발자
- [ ] `/api/boxoffice/` → `/api/performances/boxoffice/` 경로 변경
- [ ] `/api/management/` → `/api/performances/management/` 경로 변경
- [ ] API 호출 테스트

### 백엔드 개발자
- [x] views/ 폴더 생성 및 파일 이동
- [x] services/ 폴더 생성 및 파일 이동
- [x] performances/urls.py 설정
- [x] mypjt/urls.py 수정
- [x] import 경로 수정
- [ ] 서버 재시작 및 동작 확인

---

## 변경 사항 없는 API

다음 API들은 경로 변경이 없습니다:

- `/api/accounts/` - 계정 관련 API
- `/api/articles/` - 커뮤니티 게시글 API
- `/api/comments/` - 댓글 API
- `/api/recommendations/` - 추천 API

---

## 문의사항

궁금한 점이 있으면 백엔드 팀에게 문의해주세요.
