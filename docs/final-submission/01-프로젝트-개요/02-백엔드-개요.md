# 🎭 Final-PJT Backend Documentation

## 📑 목차
1. [개요](#-개요)
2. [기술 스택](#-기술-스택)
3. [프로젝트 구조](#-프로젝트-구조)
4. [데이터베이스 설계](#-데이터베이스-설계)
5. [API 엔드포인트](#-api-엔드포인트)
6. [인증 시스템](#-인증-시스템-jwt)
7. [추천 시스템](#-추천-시스템)
8. [온보딩 시스템](#-온보딩-시스템)
9. [AI 검색 엔진](#-ai-검색-엔진)
10. [외부 API 연동](#-외부-api-연동)
11. [관리자 커맨드](#-관리자-커맨드)
12. [환경 설정](#-환경-설정)
13. [개발 가이드](#-개발-가이드)
14. [배포 가이드](#-배포-가이드)

---

## 🎯 개요

본 프로젝트는 **Django 5.2**와 **Django REST Framework**를 기반으로 한 공연 정보 플랫폼의 백엔드 API 서버입니다. KOPIS API 연동, OpenAI 임베딩 기반 AI 검색, 하이브리드 추천 시스템, Tinder 스타일 온보딩 등을 제공합니다.

### 주요 특징
- ✅ **RESTful API** 설계 (ViewSet 기반)
- ✅ **JWT 인증** (Access/Refresh Token 자동 갱신)
- ✅ **하이브리드 추천 엔진** (7개 점수 함수 조합)
- ✅ **AI 의미 기반 검색** (OpenAI text-embedding-3-small)
- ✅ **KOPIS API 연동** (공연 데이터 자동 수집)
- ✅ **온보딩 시스템** (사용자 선호도 벡터 생성)
- ✅ **YouTube API 연동** (관련 영상 추천)
- ✅ **캐싱 전략** (추천 결과, YouTube 영상)
- ✅ **관리자 커맨드** (데이터 수집, 임베딩 생성)

---

## 🛠 기술 스택

### Core Framework
| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.x | 프로그래밍 언어 |
| **Django** | 5.2.8 | 웹 프레임워크 |
| **Django REST Framework** | 3.16.1 | REST API 구축 |
| **SQLite** | 3.x | 데이터베이스 (개발/운영) |

### Authentication & Security
| 기술 | 버전 | 용도 |
|------|------|------|
| **djangorestframework-simplejwt** | 5.5.1 | JWT 토큰 인증 |
| **django-cors-headers** | 4.9.0 | CORS 처리 |

### External APIs & AI
| 기술 | 버전 | 용도 |
|------|------|------|
| **openai** | 2.14.0 | OpenAI API (임베딩 생성) |
| **requests** | 2.32.5 | HTTP 클라이언트 (KOPIS API) |
| **httpx** | 0.28.1 | 비동기 HTTP 클라이언트 |

### Data Science & ML
| 기술 | 버전 | 용도 |
|------|------|------|
| **numpy** | 2.3.5 | 수치 계산 |
| **scikit-learn** | 1.8.0 | 코사인 유사도 계산 |
| **scipy** | 1.16.3 | 과학 계산 |

### Utilities
| 기술 | 버전 | 용도 |
|------|------|------|
| **python-dotenv** | 1.2.1 | 환경 변수 관리 |
| **django-filter** | 25.2 | API 필터링 |
| **pillow** | 12.0.0 | 이미지 처리 |
| **joblib** | 1.5.3 | 병렬 처리 |
| **pydantic** | 2.12.5 | 데이터 검증 |

---

## 📂 프로젝트 구조

```
back/
├── mypjt/                              # Django 프로젝트 설정
│   ├── settings.py                     # 메인 설정 (CORS, JWT, DRF)
│   ├── urls.py                         # 루트 URL 라우팅
│   ├── wsgi.py                         # WSGI 애플리케이션
│   └── asgi.py                         # ASGI 애플리케이션
│
├── accounts/                            # 사용자 관리 앱
│   ├── models.py                       # User, UserPreference, UserPerformanceSignal, WatchedPerformance
│   ├── views/
│   │   ├── api_views.py                # UserViewSet, RegisterView
│   │   └── onboarding_views.py         # OnboardingViewSet
│   ├── services/
│   │   └── onboarding_service.py       # 온보딩 로직 (후보 선택, 벡터 계산)
│   ├── serializers.py                  # UserSerializer, RegisterSerializer
│   ├── urls.py                         # /api/accounts/* 라우팅
│   ├── admin.py                        # Django Admin 설정
│   └── migrations/                     # DB 마이그레이션 파일 (5개)
│
├── performances/                        # 공연 정보 앱
│   ├── models.py                       # Performance, PerformanceDetail, BoxOfficeRanking,
│   │                                   # PerformanceEmbedding, PerformanceMetric, YouTubeVideoCache
│   ├── views/
│   │   ├── api_views.py                # PerformanceViewSet (조회, 좋아요, AI 검색)
│   │   └── management_api_views.py     # ManagementAPIViewSet (데이터 수집 엔드포인트)
│   ├── services/
│   │   ├── ai_search.py                # AISearchEngine (임베딩 기반 검색)
│   │   └── youtube_service.py          # YouTube API 클라이언트
│   ├── management/
│   │   └── commands/                   # Django 관리 커맨드
│   │       ├── collect_performances.py         # KOPIS 공연 데이터 수집
│   │       ├── collect_boxoffice.py            # 박스오피스 랭킹 수집
│   │       ├── collect_performance_detail.py   # 공연 상세 정보 수집
│   │       ├── generate_embeddings.py          # OpenAI 임베딩 생성
│   │       ├── export_embeddings.py            # 임베딩 내보내기
│   │       ├── export_fixture.py               # 데이터 내보내기
│   │       ├── migrate_old_data.py             # 데이터 마이그레이션
│   │       ├── update_performances.py          # 공연 데이터 업데이트
│   │       └── utils/                          # 유틸리티 모듈
│   │           ├── kopis_client.py             # KOPIS API 클라이언트
│   │           ├── date_helper.py              # 날짜 처리 유틸
│   │           └── logger.py                   # 로깅 유틸
│   ├── serializers.py                  # PerformanceSerializer, BoxOfficeSerializer
│   ├── urls.py                         # /api/performances/* 라우팅
│   ├── admin.py                        # Django Admin 설정
│   └── migrations/                     # DB 마이그레이션 파일 (5개)
│
├── community/                           # 커뮤니티 앱
│   ├── models.py                       # Article (게시글), Comment (댓글)
│   ├── views/
│   │   └── api_views.py                # ArticleViewSet, CommentViewSet
│   ├── serializers.py                  # ArticleSerializer, CommentSerializer
│   ├── urls.py                         # /api/community/* 라우팅
│   ├── admin.py                        # Django Admin 설정
│   └── migrations/                     # DB 마이그레이션 파일 (2개)
│
├── recommendations/                     # 추천 시스템 앱
│   ├── models.py                       # UserLog (행동 로그), RecommendationCache (캐시)
│   ├── views/
│   │   └── api_views.py                # RecommendationViewSet
│   ├── services/
│   │   └── engine.py                   # RecommendationEngine (하이브리드 알고리즘)
│   ├── serializers.py                  # RecommendationItemSerializer
│   ├── urls.py                         # /api/recommendations/* 라우팅
│   ├── admin.py                        # Django Admin 설정
│   └── migrations/                     # DB 마이그레이션 파일 (1개)
│
├── embeddings/                          # 임베딩 벡터 저장 폴더 (.npy 파일)
├── templates/                           # HTML 템플릿 (관리자 페이지용)
├── logs/                                # 로그 파일
│   └── kopis_collection.log
├── fixtures/                            # 테스트 데이터 (JSON)
│
├── db.sqlite3                           # SQLite 데이터베이스 (~113MB)
├── manage.py                            # Django 관리 스크립트
├── requirements.txt                     # Python 패키지 의존성
├── .env                                # 환경 변수 (API 키)
└── .gitignore
```

---

## 🗄 데이터베이스 설계

### ERD 개요

```
User (accounts_user)
├─ 1:N → Article (community_article)
├─ 1:N → Comment (community_comment)
├─ 1:N → UserPerformanceSignal (accounts_userperformancesignal)
├─ 1:N → WatchedPerformance (accounts_watchedperformance)
├─ 1:1 → UserPreference (accounts_userpreference)
├─ 1:1 → RecommendationCache (recommendations_recommendationcache)
├─ M:N → Performance (like_users)
└─ M:N → User (followings, symmetrical=False)

Performance (performances_performance)
├─ 1:1 → PerformanceDetail (performances_performancedetail)
├─ 1:1 → PerformanceEmbedding (performances_performanceembedding)
├─ 1:1 → PerformanceMetric (performances_performancemetric)
├─ 1:N → PerformanceImage (performances_performanceimage)
├─ 1:N → BoxOfficeRanking (performances_boxofficeranking)
├─ 1:N → Article (community_article)
├─ 1:N → YouTubeVideoCache (performances_youtubevideocache)
└─ M:N → User (like_users)
```

### 주요 모델 상세

#### 1. User (accounts_user)

**테이블명:** `accounts_user`
**부모:** `AbstractUser` 확장

| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|---------|
| id | Integer | PK | AUTO_INCREMENT |
| username | CharField(150) | 사용자명 | UNIQUE, NOT NULL |
| email | EmailField | 이메일 | |
| password | CharField(128) | 해시된 비밀번호 | NOT NULL |
| **nickname** | CharField(20) | 닉네임 | |
| **profile_image** | ImageField | 프로필 이미지 | upload_to='profile/' |
| **region** | CharField(50) | 거주 지역 | 예: '서울특별시', '경기도' |
| **preference_tags** | JSONField | 선호 태그 | 예: ['감동적인', '코미디'] |
| **favorite_actors** | JSONField | 선호 배우 | 예: ['조승우', '옥주현'] |
| **birth_date** | DateField | 생년월일 | NULL 허용 |
| **has_onboarded** | BooleanField | 온보딩 완료 여부 | DEFAULT=False |
| **onboarded_at** | DateTimeField | 온보딩 완료 시각 | NULL 허용 |
| **followings** | ManyToManyField | 팔로잉 목록 | self 참조 |

**인덱스:**
- `username` (UNIQUE)
- `email`

**프로퍼티:**
```python
@property
def age(self):
    """생년월일로부터 나이 계산"""
    if not self.birth_date:
        return None
    return timezone.now().year - self.birth_date.year
```

#### 2. Performance (performances_performance)

**테이블명:** `performances_performance`

| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|---------|
| **mt20id** | CharField(20) | 공연 ID (KOPIS) | PK |
| prfnm | CharField(255) | 공연명 | NOT NULL |
| prfpdfrom | DateField | 공연 시작일 | NOT NULL |
| prfpdto | DateField | 공연 종료일 | NOT NULL |
| fcltynm | CharField(100) | 시설명 | |
| poster | URLField | 포스터 URL | |
| area | CharField(50) | 지역 | 예: '서울', '경기' |
| genrenm | CharField(50) | 장르 | 예: '뮤지컬', '연극' |
| prfstate | CharField(50) | 공연 상태 | '공연중', '공연예정', '공연완료' |
| openrun | BooleanField | 오픈런 여부 | DEFAULT=False |
| **cast_search_text** | TextField | 출연진 검색용 텍스트 | 성능 최적화용 |
| **like_users** | ManyToManyField | 찜한 사용자 | User 참조 |

**인덱스:**
- `mt20id` (PK)
- `prfstate` (INDEX)
- `genrenm` (INDEX)
- `area` (INDEX)
- `(prfpdfrom, prfpdto)` (COMPOSITE INDEX)

#### 3. PerformanceDetail (performances_performancedetail)

**테이블명:** `performances_performancedetail`

| 필드 | 타입 | 설명 |
|------|------|------|
| performance | OneToOneField | 공연 (FK) |
| prfcast | TextField | 출연진 |
| prfcrew | TextField | 제작진 |
| prfruntime | CharField(50) | 공연 시간 (예: '120분') |
| prfage | CharField(50) | 관람 연령 (예: '만 7세 이상') |
| sty | TextField | 줄거리/시놉시스 |
| pcseguidance | TextField | 가격 정보 |
| relates | TextField | 예매처 정보 |

#### 4. PerformanceEmbedding (performances_performanceembedding)

**테이블명:** `performances_performanceembedding`

| 필드 | 타입 | 설명 |
|------|------|------|
| performance | OneToOneField | 공연 (FK) |
| **vector** | JSONField | 1536차원 임베딩 벡터 |
| created_at | DateTimeField | 생성 시각 |
| updated_at | DateTimeField | 업데이트 시각 |

**임베딩 생성:**
- OpenAI `text-embedding-3-small` 모델 사용
- 입력: `{공연명} {장르} {출연진} {줄거리}`
- 출력: 1536차원 float 벡터

#### 5. BoxOfficeRanking (performances_boxofficeranking)

**테이블명:** `performances_boxofficeranking`

| 필드 | 타입 | 설명 |
|------|------|------|
| performance | ForeignKey | 공연 (FK) |
| genre_code | CharField(10) | 장르 코드 (예: 'BBBC') |
| ranking_date | DateField | 랭킹 기준일 |
| period_type | CharField(10) | 기간 유형 ('day', 'week', 'month') |
| rank | IntegerField | 순위 (1-10) |
| rnum | IntegerField | 예매 건수 |
| area | CharField(50) | 지역 |
| collected_at | DateTimeField | 수집 시각 |

**인덱스:**
- `(genre_code, ranking_date, rank)`
- `(performance, ranking_date)`

#### 6. Article (community_article)

**테이블명:** `community_article`

| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|---------|
| id | Integer | PK | AUTO_INCREMENT |
| user | ForeignKey | 작성자 | User 참조 |
| **board_type** | CharField(20) | 게시판 유형 | 'PERFORMANCE', 'GENERAL' |
| **category** | CharField(20) | 카테고리 | 'REVIEW', 'EXPECTATION', 'QNA', 'FREE', 'INFO' |
| performance | ForeignKey | 관련 공연 | NULL 허용 (GENERAL 게시판) |
| title | CharField(100) | 제목 | NOT NULL |
| content | TextField | 내용 | NOT NULL |
| **rank** | FloatField | 별점 (1-5) | NULL 허용 (REVIEW/EXPECTATION 필수) |
| **like_users** | ManyToManyField | 좋아요한 사용자 | User 참조 |
| created_at | DateTimeField | 작성 시각 | auto_now_add=True |
| updated_at | DateTimeField | 수정 시각 | auto_now=True |

**카테고리 규칙:**
- `PERFORMANCE` 게시판: REVIEW, EXPECTATION, QNA 허용
- `GENERAL` 게시판: FREE, INFO 허용
- REVIEW/EXPECTATION은 `rank` 필수

**인덱스:**
- `board_type`
- `category`
- `performance`
- `created_at`

#### 7. UserPreference (accounts_userpreference)

**테이블명:** `accounts_userpreference`

| 필드 | 타입 | 설명 |
|------|------|------|
| user | OneToOneField | 사용자 (FK) |
| **preference_vector** | JSONField | 1536차원 선호도 벡터 |
| updated_at | DateTimeField | 업데이트 시각 |

**선호도 벡터 계산:**
```python
# 온보딩 시그널 기반 계산
weighted_sum = sum(signal.weight * performance.embedding.vector
                   for signal in user_signals)
normalized = weighted_sum / ||weighted_sum||  # L2 정규화
```

#### 8. RecommendationCache (recommendations_recommendationcache)

**테이블명:** `recommendations_recommendationcache`

| 필드 | 타입 | 설명 |
|------|------|------|
| user | OneToOneField | 사용자 (FK) |
| **top_n_list** | JSONField | 추천 결과 리스트 |
| updated_at | DateTimeField | 업데이트 시각 |

**캐시 구조:**
```json
{
  "top_n_list": [
    {
      "mt20id": "PF123456",
      "score": 0.85,
      "reason": "location",
      "reason_text": "🏠 강남구 근처에서 공연해요!"
    }
  ]
}
```

**유효 시간:** 1시간

---

## 🌐 API 엔드포인트

### 인증 (accounts)

#### 회원가입 & 로그인

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/api/accounts/register/` | 회원가입 | ❌ |
| POST | `/api/accounts/token/` | JWT 토큰 발급 (로그인) | ❌ |
| POST | `/api/accounts/token/refresh/` | Access Token 갱신 | ❌ |

**회원가입 요청:**
```json
POST /api/accounts/register/
{
  "username": "testuser",
  "password": "password123",
  "password2": "password123",
  "email": "user@example.com",
  "nickname": "테스트유저",
  "region": "서울특별시",
  "birth_date": "1990-01-01"
}
```

**회원가입 응답:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "nickname": "테스트유저"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**로그인 요청:**
```json
POST /api/accounts/token/
{
  "username": "testuser",
  "password": "password123"
}
```

**로그인 응답:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 사용자 관리

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/accounts/users/` | 사용자 목록 | ❌ |
| GET | `/api/accounts/users/<id>/` | 사용자 상세 | ❌ |
| GET | `/api/accounts/users/me/` | 현재 사용자 정보 | ✅ |
| POST | `/api/accounts/users/<id>/follow/` | 팔로우/언팔로우 토글 | ✅ |
| POST | `/api/accounts/users/verify-password/` | 비밀번호 확인 | ✅ |
| PATCH | `/api/accounts/users/update-profile/` | 프로필 수정 | ✅ |
| DELETE | `/api/accounts/users/delete-account/` | 회원 탈퇴 | ✅ |

**현재 사용자 정보:**
```json
GET /api/accounts/users/me/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "username": "testuser",
  "email": "user@example.com",
  "nickname": "테스트유저",
  "region": "서울특별시",
  "has_onboarded": true,
  "preference_tags": ["감동적인", "웃긴"],
  "favorite_actors": ["조승우", "옥주현"],
  "followers_count": 5,
  "followings_count": 3
}
```

#### 온보딩

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/accounts/onboarding/candidates/` | 온보딩 후보 공연 (16개) | ✅ |
| POST | `/api/accounts/onboarding/signals/` | 사용자 선택 신호 저장 | ✅ |
| POST | `/api/accounts/onboarding/complete/` | 온보딩 완료 | ✅ |

**후보 공연 조회:**
```json
GET /api/accounts/onboarding/candidates/?strategy=balanced&exclude_ids=PF123,PF456

Response:
{
  "candidates": [
    {
      "mt20id": "PF123456",
      "prfnm": "레미제라블",
      "poster": "http://www.kopis.or.kr/upload/...",
      "genrenm": "뮤지컬",
      "prfpdfrom": "2024-01-01",
      "prfpdto": "2024-12-31"
    }
  ],
  "count": 16
}
```

**신호 저장:**
```json
POST /api/accounts/onboarding/signals/
{
  "signals": [
    {"performance_id": "PF123456", "signal": 1.5},    // 보고싶어요
    {"performance_id": "PF234567", "signal": 0.0},    // 모르겠어요
    {"performance_id": "PF345678", "signal": -1.0}    // 안보고싶어요
  ]
}

Response:
{
  "status": "signals_saved",
  "count": 3
}
```

**온보딩 완료:**
```json
POST /api/accounts/onboarding/complete/

Response:
{
  "status": "onboarding_completed",
  "preference_vector_generated": true,
  "has_onboarded": true
}
```

### 공연 정보 (performances)

#### 공연 조회

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/performances/` | 공연 목록 (필터링, 검색, 페이지네이션) | ❌ |
| GET | `/api/performances/<mt20id>/` | 공연 상세 | ❌ |
| POST | `/api/performances/<mt20id>/like/` | 공연 찜하기/취소 | ✅ |
| POST | `/api/performances/<mt20id>/watch/` | 관람함 추가 | ✅ |
| DELETE | `/api/performances/<mt20id>/watch/` | 관람함 제거 | ✅ |
| GET | `/api/performances/liked/` | 찜한 공연 목록 | ✅ |
| GET | `/api/performances/watched/` | 관람한 공연 목록 | ✅ |

**공연 목록 필터링:**
```
GET /api/performances/?genrenm=뮤지컬&prfstate=공연중&area=서울&page=1&page_size=10

Query Parameters:
- genrenm: 장르 필터 (예: '뮤지컬', '연극', '클래식')
- prfstate: 상태 필터 ('공연중', '공연예정', '공연완료')
- area: 지역 필터 (예: '서울', '경기')
- search: 검색어 (공연명, 시설명 검색)
- ordering: 정렬 기준 (prfpdfrom, -prfpdfrom, prfpdto, -prfpdto)
- page: 페이지 번호
- page_size: 페이지당 항목 수
```

**공연 목록 응답:**
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/performances/?page=2",
  "previous": null,
  "results": [
    {
      "mt20id": "PF123456",
      "prfnm": "레미제라블",
      "prfpdfrom": "2024-01-01",
      "prfpdto": "2024-12-31",
      "fcltynm": "샤롯데씨어터",
      "poster": "http://www.kopis.or.kr/upload/...",
      "area": "서울",
      "genrenm": "뮤지컬",
      "prfstate": "공연중",
      "openrun": false,
      "is_liked": true,
      "like_count": 1234
    }
  ]
}
```

**공연 상세 조회:**
```json
GET /api/performances/PF123456/

Response:
{
  "mt20id": "PF123456",
  "prfnm": "레미제라블",
  "prfpdfrom": "2024-01-01",
  "prfpdto": "2024-12-31",
  "fcltynm": "샤롯데씨어터",
  "poster": "http://www.kopis.or.kr/upload/...",
  "area": "서울",
  "genrenm": "뮤지컬",
  "prfstate": "공연중",
  "is_liked": false,
  "is_watched": false,
  "detail": {
    "prfcast": "조승우, 옥주현, 민영기",
    "prfcrew": "연출: 홍길동",
    "prfruntime": "170분",
    "prfage": "만 7세 이상",
    "sty": "빅토르 위고의 동명 소설을 원작으로...",
    "pcseguidance": "VIP석 140,000원, R석 120,000원...",
    "relates": "인터파크, 예스24..."
  },
  "intro_images": [
    {
      "id": 1,
      "styurl": "http://www.kopis.or.kr/upload/..."
    }
  ]
}
```

#### 박스오피스

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/performances/boxoffice-genre/` | 장르별 박스오피스 | ❌ |
| GET | `/api/performances/boxoffice-all/` | 전체 박스오피스 Top 10 | ❌ |
| GET | `/api/performances/boxoffice-highlight/` | 박스오피스 하이라이트 | ❌ |

**장르별 박스오피스:**
```
GET /api/performances/boxoffice-genre/?genre=BBBC

Genre Codes:
- AAAA: 연극
- BBBC: 뮤지컬
- CCCA: 클래식
- CCCD: 무용
- GGGA: 대중음악

Response:
{
  "genre_code": "BBBC",
  "genre_name": "뮤지컬",
  "rankings": [
    {
      "rank": 1,
      "performance": {
        "mt20id": "PF123456",
        "prfnm": "레미제라블",
        "poster": "...",
        "genrenm": "뮤지컬"
      },
      "rnum": 15234
    }
  ]
}
```

#### AI 검색

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/api/performances/ai-search/` | AI 의미 기반 검색 | ❌ |

**AI 검색 요청:**
```json
POST /api/performances/ai-search/
{
  "query": "감동적이고 웅장한 뮤지컬",
  "top_k": 10
}

Response:
{
  "query": "감동적이고 웅장한 뮤지컬",
  "results": [
    {
      "mt20id": "PF123456",
      "prfnm": "레미제라블",
      "similarity_score": 0.92,
      "poster": "...",
      "genrenm": "뮤지컬"
    }
  ],
  "ai_comment": "19세기 프랑스를 배경으로 한 감동적인 대서사시 뮤지컬입니다. 웅장한 스케일과 아름다운 음악이 특징입니다."
}
```

#### 관리자 API (데이터 수집)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/api/performances/management/collect-performances/` | 공연 데이터 수집 | ✅ (Admin) |
| POST | `/api/performances/management/collect-boxoffice/` | 박스오피스 수집 | ✅ (Admin) |
| POST | `/api/performances/management/collect-details/` | 공연 상세정보 수집 | ✅ (Admin) |
| GET | `/api/performances/management/stats/` | 데이터 통계 | ✅ (Admin) |

### 커뮤니티 (community)

#### 게시글

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/community/articles/` | 게시글 목록 | ❌ |
| POST | `/api/community/articles/` | 게시글 작성 | ✅ |
| GET | `/api/community/articles/<id>/` | 게시글 상세 | ❌ |
| PUT | `/api/community/articles/<id>/` | 게시글 수정 | ✅ (작성자) |
| DELETE | `/api/community/articles/<id>/` | 게시글 삭제 | ✅ (작성자) |
| POST | `/api/community/articles/<id>/like/` | 게시글 좋아요 | ✅ |
| GET | `/api/community/articles/best-reviews/` | 베스트 리뷰 | ❌ |

**게시글 목록 필터링:**
```
GET /api/community/articles/?board_type=PERFORMANCE&category=REVIEW&performance_mt20id=PF123&ordering=-created_at

Query Parameters:
- board_type: PERFORMANCE, GENERAL
- category: REVIEW, EXPECTATION, QNA, FREE, INFO
- performance_mt20id: 특정 공연의 게시글만 조회
- search: 제목/내용 검색
- ordering: created_at, -created_at, like_count
```

**게시글 작성:**
```json
POST /api/community/articles/
{
  "board_type": "PERFORMANCE",
  "category": "REVIEW",
  "performance": "PF123456",
  "title": "레미제라블 후기",
  "content": "정말 감동적이었습니다...",
  "rank": 4.5
}

Response:
{
  "id": 1,
  "board_type": "PERFORMANCE",
  "category": "REVIEW",
  "performance": "PF123456",
  "performance_name": "레미제라블",
  "title": "레미제라블 후기",
  "content": "정말 감동적이었습니다...",
  "rank": 4.5,
  "user": 1,
  "username": "testuser",
  "like_count": 0,
  "is_liked": false,
  "created_at": "2024-12-23T10:00:00Z",
  "comments": []
}
```

**베스트 리뷰:**
```
GET /api/community/articles/best-reviews/?limit=4

조건:
- 14일 이내 작성
- category=REVIEW
- 좋아요 많은 순

Response:
{
  "results": [...]
}
```

#### 댓글

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/community/comments/` | 댓글 목록 | ❌ |
| POST | `/api/community/comments/` | 댓글 작성 | ✅ |
| PATCH | `/api/community/comments/<id>/` | 댓글 수정 | ✅ (작성자) |
| DELETE | `/api/community/comments/<id>/` | 댓글 삭제 | ✅ (작성자) |

**댓글 조회:**
```
GET /api/community/comments/?article=1

Response:
{
  "results": [
    {
      "id": 1,
      "article": 1,
      "user": 2,
      "username": "user2",
      "content": "저도 감동받았어요!",
      "created_at": "2024-12-23T10:30:00Z"
    }
  ]
}
```

### 추천 시스템 (recommendations)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/api/recommendations/` | 개인화 추천 목록 | ✅ |
| POST | `/api/recommendations/log/` | 행동 로그 저장 | ✅ |
| POST | `/api/recommendations/refresh/` | 추천 캐시 강제 갱신 | ✅ |

**추천 조회:**
```json
GET /api/recommendations/?top_n=10
Authorization: Bearer <access_token>

Response:
{
  "recommendations": [
    {
      "mt20id": "PF123456",
      "score": 0.85,
      "reason": "location",
      "reason_text": "🏠 서울특별시 근처에서 공연해요!",
      "prfnm": "레미제라블",
      "poster": "...",
      "genrenm": "뮤지컬",
      "area": "서울"
    }
  ],
  "cached": true,
  "cache_age_seconds": 1234
}
```

**행동 로그 저장:**
```json
POST /api/recommendations/log/
{
  "performance_id": "PF123456",
  "action_type": "view"  // view, like, search
}

Response:
{
  "status": "logged"
}
```

---

## 🔐 인증 시스템 (JWT)

### JWT 설정

**파일:** [mypjt/settings.py](mypjt/settings.py)

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),       # 1시간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # 7일
    'ROTATE_REFRESH_TOKENS': True,                      # 토큰 자동 회전
    'BLACKLIST_AFTER_ROTATION': True,                   # 회전 후 블랙리스트
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
```

### 인증 흐름

```
1. 로그인
   POST /api/accounts/token/
   Body: {"username": "user", "password": "pass"}
   → Response: {"access": "...", "refresh": "..."}

2. API 요청
   GET /api/performances/
   Headers: Authorization: Bearer <access_token>

3. Access Token 만료 시 (1시간 후)
   POST /api/accounts/token/refresh/
   Body: {"refresh": "<refresh_token>"}
   → Response: {"access": "new_access_token"}

4. Refresh Token 만료 시 (7일 후)
   → 재로그인 필요
```

### 권한 클래스

```python
# IsAuthenticatedOrReadOnly: 읽기는 누구나, 쓰기는 로그인 필요
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

# IsAdminUser: 관리자만 접근 가능
class ManagementAPIViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

# Custom Permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
```

---

## 🎯 추천 시스템

### 하이브리드 추천 알고리즘

**파일:** [recommendations/services/engine.py](recommendations/services/engine.py)

#### 점수 함수 구성

```python
WEIGHTS = {
    'f1_click': 0.20,         # 클릭/관심 로그 기반
    'f2_preference': 0.15,    # 취향 매칭 (장르, 배우)
    'f3_location': 0.10,      # 위치 근접성
    'f4_popularity': 0.15,    # 대중성 (박스오피스)
    'f5_recency': 0.10,       # 최신성
    'f6_collaborative': 0.10, # 협업 필터링
    'f7_embedding': 0.20      # 임베딩 유사도
}

# 최종 점수 = Σ(weight_i × score_i)
```

#### f1: 클릭/관심 로그 기반

```python
def _score_f1_click(self, performance):
    """사용자의 과거 행동 패턴 분석"""
    logs = UserLog.objects.filter(
        user=self.user,
        performance=performance
    )

    score = 0
    for log in logs:
        action_weight = {
            'view': 1,
            'like': 3,
            'search': 2
        }[log.action_type]

        # Time Decay (λ=0.95)
        days_ago = (timezone.now() - log.timestamp).days
        decay = 0.95 ** days_ago

        score += action_weight * decay

    return normalize(score)
```

#### f2: 취향 매칭

```python
def _score_f2_preference(self, performance):
    """사용자 선호 태그/배우와 공연 정보 매칭"""
    score = 0

    # 장르 매칭
    if performance.genrenm in self.user.preference_tags:
        score += 0.5

    # 선호 배우 출연 여부
    for actor in self.user.favorite_actors:
        if actor in performance.cast_search_text:
            score += 0.5

    return normalize(score)
```

#### f3: 위치 근접성

```python
def _score_f3_location(self, performance):
    """사용자 거주 지역과 공연 장소 비교"""
    if self.user.region == performance.area:
        return 1.0

    # 인접 지역 점수 (예: 서울-경기)
    adjacent_regions = {
        '서울특별시': ['경기도'],
        '경기도': ['서울특별시', '인천광역시']
    }

    if performance.area in adjacent_regions.get(self.user.region, []):
        return 0.5

    return 0.0
```

#### f4: 대중성

```python
def _score_f4_popularity(self, performance):
    """박스오피스 랭킹 기반 인기도"""
    try:
        metric = performance.metric
        return metric.score_popularity  # 미리 계산된 점수
    except:
        return 0.0
```

#### f5: 최신성

```python
def _score_f5_recency(self, performance):
    """공연 시작일 기준 최신성"""
    days_since_start = (timezone.now().date() - performance.prfpdfrom).days

    # Time Decay
    decay = 0.98 ** days_since_start
    return max(0, decay)
```

#### f6: 협업 필터링

```python
def _score_f6_collaborative(self, performance):
    """유사 공연 기반 추천"""
    # 사용자가 좋아한 공연과 유사한 공연 찾기
    liked_performances = self.user.liked_performances.all()

    score = 0
    for liked in liked_performances:
        if performance.mt20id in liked.metric.similar_performances:
            score += 1

    return normalize(score)
```

#### f7: 임베딩 유사도

```python
def _score_f7_embedding(self, performance):
    """사용자 선호도 벡터와 공연 임베딩 코사인 유사도"""
    try:
        user_vector = self.user.preference.preference_vector
        performance_vector = performance.embedding.vector

        # 코사인 유사도
        similarity = cosine_similarity([user_vector], [performance_vector])[0][0]
        return (similarity + 1) / 2  # [-1, 1] → [0, 1]
    except:
        return 0.0
```

### 추천 프로세스

```python
class RecommendationEngine:
    def get_recommendations(self, top_n=10):
        # 1. 후보군 필터링 (공연 중/예정, 최대 300개)
        candidates = Performance.objects.filter(
            Q(prfstate='공연중') | Q(prfstate='공연예정')
        ).select_related('detail', 'embedding', 'metric')[:300]

        # 2. 점수 계산
        scored = []
        for perf in candidates:
            breakdown = {
                'f1': self._score_f1_click(perf) * WEIGHTS['f1_click'],
                'f2': self._score_f2_preference(perf) * WEIGHTS['f2_preference'],
                'f3': self._score_f3_location(perf) * WEIGHTS['f3_location'],
                'f4': self._score_f4_popularity(perf) * WEIGHTS['f4_popularity'],
                'f5': self._score_f5_recency(perf) * WEIGHTS['f5_recency'],
                'f6': self._score_f6_collaborative(perf) * WEIGHTS['f6_collaborative'],
                'f7': self._score_f7_embedding(perf) * WEIGHTS['f7_embedding'],
            }

            total_score = sum(breakdown.values())
            scored.append({
                'performance': perf,
                'score': total_score,
                'breakdown': breakdown
            })

        # 3. 정렬 및 Top-N 추출
        scored.sort(key=lambda x: x['score'], reverse=True)

        # 4. 추천 이유 생성
        recommendations = []
        for item in scored[:top_n]:
            reason, reason_text = self._get_top_reason(item['breakdown'])
            recommendations.append({
                'mt20id': item['performance'].mt20id,
                'score': round(item['score'], 2),
                'reason': reason,
                'reason_text': reason_text
            })

        return recommendations

    def _get_top_reason(self, breakdown):
        """가장 높은 점수의 이유 반환"""
        top_feature = max(breakdown, key=breakdown.get)

        reason_map = {
            'f3': ('location', '🏠 거주 지역 근처에서 공연해요!'),
            'f4': ('popularity', '🔥 많은 사람들이 좋아하는 인기 공연이에요!'),
            'f7': ('preference', '💖 회원님의 취향에 딱 맞는 공연이에요!'),
        }

        return reason_map.get(top_feature, ('general', '추천드립니다!'))
```

### 캐싱 전략

```python
# View에서 캐시 사용
def list(self, request):
    user = request.user

    # 1. 캐시 확인 (1시간 유효)
    try:
        cache = RecommendationCache.objects.get(user=user)
        if cache.is_fresh(max_age_hours=1):
            return Response({
                'recommendations': cache.top_n_list,
                'cached': True
            })
    except RecommendationCache.DoesNotExist:
        pass

    # 2. 추천 엔진 실행
    engine = RecommendationEngine(user)
    recommendations = engine.get_recommendations(top_n=10)

    # 3. 캐시 저장
    cache, created = RecommendationCache.objects.update_or_create(
        user=user,
        defaults={'top_n_list': recommendations}
    )

    return Response({
        'recommendations': recommendations,
        'cached': False
    })
```

---

## 🎓 온보딩 시스템

### 온보딩 프로세스

**파일:** [accounts/services/onboarding_service.py](accounts/services/onboarding_service.py)

#### 1단계: 후보 공연 제공 (16개)

```python
def get_onboarding_candidates(count=16, strategy='balanced', exclude_ids=None):
    """
    전략:
    - balanced: 8개(인기) + 4개(최신) + 4개(다양 장르)
    - popular: 인기도 기준
    - recent: 최신 공연 기준
    """

    performances = Performance.objects.filter(
        Q(prfstate='공연중') | Q(prfstate='공연예정')
    ).exclude(mt20id__in=exclude_ids or [])

    if strategy == 'balanced':
        # 8개: 인기 공연
        popular = performances.annotate(
            popularity=Coalesce('metric__score_popularity', 0.0)
        ).order_by('-popularity')[:8]

        # 4개: 최신 공연
        recent = performances.order_by('-prfpdfrom')[:4]

        # 4개: 장르별 다양성
        genres = ['뮤지컬', '연극', '클래식', '무용']
        diverse = []
        for genre in genres:
            perf = performances.filter(genrenm=genre).first()
            if perf:
                diverse.append(perf)

        # 병합 및 중복 제거
        candidates = list(set(list(popular) + list(recent) + diverse))
        return candidates[:count]
```

#### 2단계: 사용자 반응 수집

```python
# Signal 값
# - 1.5: 보고싶어요 (Like)
# - 0.0: 모르겠어요 (Skip)
# - -1.0: 안보고싶어요 (Dislike)

def save_user_signals(user, signals):
    """
    signals = [
        {'performance_id': 'PF123', 'signal': 1.5},
        {'performance_id': 'PF456', 'signal': 0.0},
        ...
    ]
    """

    for signal_data in signals:
        UserPerformanceSignal.objects.create(
            user=user,
            performance_id=signal_data['performance_id'],
            signal=signal_data['signal']
        )
```

#### 3단계: 선호도 벡터 계산

```python
def calculate_preference_vector(user):
    """
    알고리즘:
    1. 사용자의 모든 signal 조회
    2. signal 가중치 × 공연 임베딩 벡터
    3. 가중합 계산 후 L2 정규화

    결과: 1536차원 정규화 벡터
    """

    signals = UserPerformanceSignal.objects.filter(
        user=user,
        performance__embedding__isnull=False
    ).select_related('performance__embedding')

    if not signals.exists():
        return None

    # 가중합 계산
    weighted_sum = np.zeros(1536, dtype=np.float32)

    for signal_obj in signals:
        embedding_vector = np.array(signal_obj.performance.embedding.vector)
        weight = signal_obj.signal  # 1.5, 0.0, -1.0
        weighted_sum += weight * embedding_vector

    # L2 정규화
    norm = np.linalg.norm(weighted_sum)
    if norm > 0:
        normalized = weighted_sum / norm
    else:
        normalized = weighted_sum

    return normalized.tolist()
```

#### 4단계: 온보딩 완료

```python
def complete_onboarding(user):
    """온보딩 완료 처리"""

    # 1. 선호도 벡터 계산
    preference_vector = calculate_preference_vector(user)

    if preference_vector:
        # 2. UserPreference 저장
        UserPreference.objects.update_or_create(
            user=user,
            defaults={'preference_vector': preference_vector}
        )

    # 3. 온보딩 완료 플래그 설정
    user.has_onboarded = True
    user.onboarded_at = timezone.now()
    user.save()

    return True
```

### 온보딩 API 플로우

```
1. GET /api/accounts/onboarding/candidates/?strategy=balanced
   → 16개 공연 반환

2. POST /api/accounts/onboarding/signals/
   Body: {"signals": [...]}
   → 최소 8개 선택 필요

3. POST /api/accounts/onboarding/complete/
   → preference_vector 생성
   → has_onboarded=True 설정
```

---

## 🔍 AI 검색 엔진

### OpenAI 임베딩 기반 검색

**파일:** [performances/services/ai_search.py](performances/services/ai_search.py)

#### 임베딩 생성

```python
class AISearchEngine:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
            api_key=os.getenv("GMS_KEY"),
        )

    def get_embedding(self, text):
        """텍스트를 1536차원 벡터로 변환"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def generate_performance_embedding_text(self, performance):
        """공연 정보를 임베딩용 텍스트로 변환"""
        parts = [
            f"공연명: {performance.prfnm}",
            f"장르: {performance.genrenm}",
        ]

        if hasattr(performance, 'detail') and performance.detail:
            if performance.detail.prfcast:
                parts.append(f"출연: {performance.detail.prfcast}")
            if performance.detail.sty:
                parts.append(f"줄거리: {performance.detail.sty[:200]}")

        return " ".join(parts)
```

#### 유사도 검색

```python
def find_similar_performances(self, user_query, performances_qs, top_k=10):
    """
    코사인 유사도 기반 검색

    1. 사용자 쿼리 임베딩
    2. 모든 공연의 임베딩 벡터 로드
    3. 코사인 유사도 계산
    4. Top-K 반환
    """

    # 1. 쿼리 임베딩
    query_vector = self.get_embedding(user_query)

    # 2. 공연 임베딩 로드
    performances_with_embeddings = performances_qs.filter(
        embedding__isnull=False
    ).select_related('embedding')

    # 3. 유사도 계산
    performances_list = []
    vectors_list = []

    for perf in performances_with_embeddings:
        performances_list.append(perf)
        vectors_list.append(perf.embedding.vector)

    if not vectors_list:
        return []

    # 코사인 유사도
    similarities = cosine_similarity([query_vector], vectors_list)[0]

    # 4. 정렬 및 Top-K
    indexed_sims = list(enumerate(similarities))
    indexed_sims.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, sim in indexed_sims[:top_k]:
        results.append({
            'performance': performances_list[idx],
            'similarity_score': float(sim)
        })

    return results
```

#### AI 코멘트 생성

```python
def generate_recommendation_reason(self, user_input, performance):
    """GPT를 사용해 추천 이유 생성"""

    prompt = f"""
    사용자가 "{user_input}"라고 검색했을 때,
    다음 공연을 추천하는 이유를 한 문장으로 설명해주세요.

    공연명: {performance.prfnm}
    장르: {performance.genrenm}
    출연: {performance.detail.prfcast if performance.detail else '정보 없음'}

    친근하고 짧게 설명해주세요.
    """

    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()
```

### AI 검색 API

```python
# views/api_views.py
@action(detail=False, methods=['post'])
def ai_search(self, request):
    """AI 의미 기반 검색"""

    query = request.data.get('query')
    top_k = request.data.get('top_k', 10)

    # 검색 실행
    engine = AISearchEngine()
    results = engine.find_similar_performances(
        query,
        Performance.objects.all(),
        top_k=top_k
    )

    # AI 코멘트 생성
    if results:
        ai_comment = engine.generate_recommendation_reason(
            query,
            results[0]['performance']
        )
    else:
        ai_comment = "검색 결과가 없습니다."

    return Response({
        'query': query,
        'results': [
            {
                'mt20id': r['performance'].mt20id,
                'prfnm': r['performance'].prfnm,
                'similarity_score': r['similarity_score'],
                ...
            }
            for r in results
        ],
        'ai_comment': ai_comment
    })
```

---

## 🌍 외부 API 연동

### 1. KOPIS API (공연예술통합전산망)

**파일:** [performances/management/commands/utils/kopis_client.py](performances/management/commands/utils/kopis_client.py)

#### API 설정

```python
class KopisAPIClient:
    BASE_URL = "http://www.kopis.or.kr/openApi/restful/pblprfr"
    BOXOFFICE_URL = "http://kopis.or.kr/openApi/restful/boxoffice"

    def __init__(self):
        self.api_key = os.getenv('KOPIS_API')
        self.session = requests.Session()
        self.rate_limit_delay = 0.15  # 초당 6.67회
```

#### 공연 목록 조회

```python
def fetch_performances(self, start_date, end_date, page=1, prfstate=None):
    """
    공연 목록 조회

    Args:
        start_date: YYYYMMDD
        end_date: YYYYMMDD
        page: 페이지 번호
        prfstate: '공연중', '공연예정', '공연완료'

    Returns:
        {
            'db': [공연 목록],
            'totalCount': 전체 개수
        }
    """

    params = {
        'service': self.api_key,
        'stdate': start_date,
        'eddate': end_date,
        'cpage': page,
        'rows': 100,  # 페이지당 100개
    }

    if prfstate:
        params['prfstate'] = prfstate

    response = self.session.get(self.BASE_URL, params=params, timeout=10)

    # XML → Dict 변환
    data = xmltodict.parse(response.content)
    return data['dbs']
```

#### 박스오피스 조회

```python
def fetch_boxoffice(self, date, genre_code, period_type='week'):
    """
    박스오피스 랭킹 조회

    Args:
        date: YYYYMMDD
        genre_code: 'AAAA'(연극), 'BBBC'(뮤지컬), 'CCCA'(클래식), ...
        period_type: 'day', 'week', 'month'

    Returns:
        [
            {
                'mt20id': 공연ID,
                'prfnm': 공연명,
                'rnum': 예매 건수,
                'rank': 순위
            }
        ]
    """

    params = {
        'service': self.api_key,
        'ststype': period_type,
        'date': date,
        'catecode': genre_code
    }

    response = self.session.get(self.BOXOFFICE_URL, params=params)
    data = xmltodict.parse(response.content)

    return data['boxofs']['boxof']
```

#### 공연 상세 정보 조회

```python
def fetch_performance_detail(self, mt20id):
    """
    공연 상세 정보 조회

    Returns:
        {
            'prfcast': 출연진,
            'prfcrew': 제작진,
            'prfruntime': 공연시간,
            'prfage': 관람연령,
            'sty': 줄거리,
            'pcseguidance': 가격,
            'styurls': [소개 이미지 URL들]
        }
    """

    url = f"{self.BASE_URL}/{mt20id}"
    params = {'service': self.api_key}

    response = self.session.get(url, params=params, timeout=10)
    data = xmltodict.parse(response.content)

    return data['dbs']['db']
```

#### Rate Limiting

```python
def _respect_rate_limit(self):
    """API 호출 간격 제어 (0.15초)"""
    time.sleep(self.rate_limit_delay)

def fetch_with_retry(self, fetch_func, max_retries=3):
    """재시도 로직"""
    for attempt in range(max_retries):
        try:
            self._respect_rate_limit()
            return fetch_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 2. YouTube API

**파일:** [performances/services/youtube_service.py](performances/services/youtube_service.py)

#### API 설정

```python
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"

PLAYLIST_ID = os.getenv('YOUTUBE_PLAYLIST_ID_MAIN')
```

#### 플레이리스트 영상 조회

```python
def get_playlist_videos(max_results=6):
    """
    YouTube 플레이리스트에서 영상 조회

    캐시 전략:
    - YouTubeVideoCache 모델 사용
    - 1시간 유효
    """

    cache_key = 'playlist:main'

    # 1. 캐시 확인
    try:
        cache = YouTubeVideoCache.objects.get(cache_key=cache_key)
        if cache.is_fresh(max_age_hours=1):
            return cache.video_data
    except YouTubeVideoCache.DoesNotExist:
        pass

    # 2. YouTube API 호출
    url = f"{YOUTUBE_BASE_URL}/playlistItems"
    params = {
        'part': 'snippet',
        'playlistId': PLAYLIST_ID,
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    videos = []
    for item in data.get('items', []):
        videos.append({
            'video_id': item['snippet']['resourceId']['videoId'],
            'title': item['snippet']['title'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
        })

    # 3. 캐시 저장
    YouTubeVideoCache.objects.update_or_create(
        cache_key=cache_key,
        defaults={'video_data': videos}
    )

    return videos
```

#### 공연 영상 검색

```python
def search_performance_video(performance_name):
    """
    공연 이름으로 YouTube 검색

    쿼리 시도 순서:
    1. "{공연명} 예고편"
    2. "{공연명} 하이라이트"
    3. "{공연명} 공연"
    """

    queries = [
        f"{performance_name} 예고편",
        f"{performance_name} 하이라이트",
        f"{performance_name} 공연"
    ]

    for query in queries:
        url = f"{YOUTUBE_BASE_URL}/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 1,
            'key': YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get('items'):
            item = data['items'][0]
            return {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }

    return None
```

### 3. OpenAI API (GMS 프록시)

**환경 변수:**
```
GMS_KEY=S14P02EA04-d3c9dd17-d210-4f94-b377-f399392320f7
```

**프록시 URL:**
```
https://gms.ssafy.io/gmsapi/api.openai.com/v1
```

**사용 예시:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
    api_key=os.getenv("GMS_KEY"),
)

# 임베딩 생성
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="감동적인 뮤지컬"
)

embedding_vector = response.data[0].embedding  # 1536차원
```

---

## 🔧 관리자 커맨드

### 1. 공연 데이터 수집

**파일:** [performances/management/commands/collect_performances.py](performances/management/commands/collect_performances.py)

```bash
python manage.py collect_performances \
    --start-date 2023-01-01 \
    --end-date 2025-11-29 \
    --chunk-days 31 \
    --batch-size 100
```

**옵션:**
- `--start-date`: 수집 시작일 (YYYY-MM-DD)
- `--end-date`: 수집 종료일 (YYYY-MM-DD)
- `--chunk-days`: 날짜 범위 분할 단위 (기본 31일)
- `--batch-size`: 배치 크기 (기본 100)

**동작:**
1. 날짜 범위를 chunk_days 단위로 분할
2. KOPIS API 호출 (페이지네이션)
3. Performance 모델에 bulk_create
4. 로그 기록

### 2. 박스오피스 수집

**파일:** [performances/management/commands/collect_boxoffice.py](performances/management/commands/collect_boxoffice.py)

```bash
python manage.py collect_boxoffice \
    --date 20251223 \
    --period week
```

**옵션:**
- `--date`: 기준일 (YYYYMMDD)
- `--period`: 기간 유형 (day, week, month)

**수집 장르:**
- AAAA: 연극
- BBBC: 뮤지컬
- CCCA: 클래식
- CCCD: 무용
- GGGA: 대중음악

### 3. 공연 상세 정보 수집

**파일:** [performances/management/commands/collect_performance_detail.py](performances/management/commands/collect_performance_detail.py)

```bash
python manage.py collect_performance_detail
```

**동작:**
1. PerformanceDetail이 없는 Performance 조회
2. KOPIS API로 상세 정보 조회
3. PerformanceDetail 및 PerformanceImage 생성
4. cast_search_text 업데이트 (검색 최적화용)

### 4. 임베딩 생성

**파일:** [performances/management/commands/generate_embeddings.py](performances/management/commands/generate_embeddings.py)

```bash
python manage.py generate_embeddings \
    --batch-size 10 \
    --skip-existing
```

**옵션:**
- `--batch-size`: 배치 크기 (기본 10)
- `--skip-existing`: 기존 임베딩 스킵

**동작:**
1. 임베딩이 없는 Performance 조회
2. OpenAI API로 임베딩 생성 (1536차원)
3. PerformanceEmbedding 모델에 저장
4. Rate Limiting (배치당 1초 대기)

### 5. 데이터 내보내기

```bash
# 임베딩 내보내기
python manage.py export_embeddings

# 전체 데이터 Fixture 내보내기
python manage.py export_fixture
```

### 6. 데이터 업데이트

```bash
# 공연 데이터 업데이트 (최근 3개월)
python manage.py update_performances
```

---

## ⚙ 환경 설정

### 환경 변수 (.env)

**파일 위치:** `back/.env`

```env
# Django
SECRET_KEY=django-insecure-x_doak&k(a!a1n-n#&to-u7)jqo9%0tqupai@f@t80+y-mcy5t
DEBUG=True

# KOPIS API
KOPIS_API=d1feab7646ba4fe2adf138ba9499cec5
KOPIS_URL=http://www.kopis.or.kr/openApi/restful/pblprfr

# OpenAI (GMS 프록시)
GMS_KEY=S14P02EA04-d3c9dd17-d210-4f94-b377-f399392320f7

# YouTube
YOUTUBE_API_KEY=AIzaSyDSW-NnRulNrCyGG0bnP1qEKa1nv7zeFQ4
YOUTUBE_PLAYLIST_ID_MAIN=PLv_Yl-rq-62pyQ0wKHHRsjPZ7KCWMqsxL

# Database (SQLite - 기본값 사용)
# DATABASE_URL=sqlite:///db.sqlite3
```

### CORS 설정

**파일:** [mypjt/settings.py](mypjt/settings.py)

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Vue dev server
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5174',
]
```

### 로깅 설정

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'kopis_collection.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'collect_performances': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### 캐시 설정

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'youtube-cache',
    }
}
```

---

## 👨‍💻 개발 가이드

### 사전 요구사항

- **Python**: 3.8 이상
- **pip**: 최신 버전
- **virtualenv** (권장)

### 설치 및 실행

#### 1. 가상환경 생성 및 활성화

```bash
cd back

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

#### 3. 환경 변수 설정

```bash
# .env 파일 생성 및 API 키 입력
cp .env.example .env
# .env 파일 편집
```

#### 4. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

#### 5. 슈퍼유저 생성 (관리자 페이지 접근용)

```bash
python manage.py createsuperuser
```

#### 6. 개발 서버 실행

```bash
python manage.py runserver
```

서버가 [http://127.0.0.1:8000](http://127.0.0.1:8000)에서 실행됩니다.

### 초기 데이터 수집

```bash
# 1. 공연 데이터 수집 (최근 1년)
python manage.py collect_performances \
    --start-date 2024-01-01 \
    --end-date 2024-12-31

# 2. 공연 상세 정보 수집
python manage.py collect_performance_detail

# 3. 박스오피스 랭킹 수집
python manage.py collect_boxoffice --date 20241223 --period week

# 4. 임베딩 생성 (AI 검색용)
python manage.py generate_embeddings --batch-size 10
```

### 개발 워크플로우

#### 1. 새 앱 추가

```bash
python manage.py startapp myapp

# settings.py의 INSTALLED_APPS에 추가
INSTALLED_APPS = [
    ...
    'myapp',
]
```

#### 2. 모델 생성 및 마이그레이션

```python
# myapp/models.py
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Serializer 작성

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

#### 4. ViewSet 작성

```python
# myapp/views/api_views.py
from rest_framework import viewsets
from ..models import MyModel
from ..serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

#### 5. URL 라우팅

```python
# myapp/urls.py
from rest_framework.routers import DefaultRouter
from .views.api_views import MyModelViewSet

router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet)

urlpatterns = router.urls
```

```python
# mypjt/urls.py
urlpatterns = [
    ...
    path('api/myapp/', include('myapp.urls')),
]
```

### 테스트

```bash
# 모든 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test accounts

# 테스트 커버리지 (coverage 설치 필요)
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Django Admin 접근

```
URL: http://127.0.0.1:8000/admin/
Username: (createsuperuser로 생성한 계정)
Password: (설정한 비밀번호)
```

---

## 🚀 배포 가이드

### 프로덕션 설정 변경

#### 1. settings.py 수정

```python
# 보안 설정
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# SECRET_KEY 변경 (환경 변수 사용)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# 데이터베이스 (PostgreSQL 권장)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# HTTPS 설정
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS 프로덕션 설정
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

#### 2. 정적 파일 수집

```bash
python manage.py collectstatic --noinput
```

#### 3. Gunicorn 설치

```bash
pip install gunicorn
```

#### 4. Gunicorn으로 실행

```bash
gunicorn mypjt.wsgi:application --bind 0.0.0.0:8000
```

### Docker 배포

#### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 마이그레이션 및 정적 파일 수집
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Gunicorn 실행
CMD ["gunicorn", "mypjt.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: finalproject
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn mypjt.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/finalproject

volumes:
  postgres_data:
```

```bash
docker-compose up -d
```

### Nginx 설정

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

---

## 📊 성능 최적화

### 데이터베이스 최적화

```python
# 1. select_related (1:1, N:1)
Performance.objects.select_related('detail', 'embedding')

# 2. prefetch_related (M:N, 1:N 역참조)
Performance.objects.prefetch_related('intro_images', 'like_users')

# 3. only / defer
Performance.objects.only('mt20id', 'prfnm', 'poster')

# 4. 인덱스 활용
class Performance(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['prfstate']),
            models.Index(fields=['genrenm']),
        ]
```

### 캐싱 전략

```python
# 1. 추천 결과 캐시 (1시간)
RecommendationCache

# 2. YouTube 영상 캐시 (1시간)
YouTubeVideoCache

# 3. Django 캐시 프레임워크
from django.core.cache import cache

def get_boxoffice():
    cache_key = 'boxoffice:latest'
    result = cache.get(cache_key)

    if result is None:
        result = fetch_from_db()
        cache.set(cache_key, result, 3600)  # 1시간

    return result
```

### 배치 처리

```python
# bulk_create (대량 INSERT)
performances = [Performance(...) for _ in range(1000)]
Performance.objects.bulk_create(performances, batch_size=100)

# bulk_update (대량 UPDATE)
Performance.objects.bulk_update(performances, ['prfstate'], batch_size=100)
```

---

## 🔒 보안 고려사항

### 1. API 키 보호
- ✅ 환경 변수(.env) 사용
- ✅ .gitignore에 .env 추가
- ⚠️ 프로덕션: AWS Secrets Manager 사용 권장

### 2. SQL Injection 방지
- ✅ Django ORM 사용 (자동 이스케이핑)
- ⚠️ Raw SQL 사용 시 parameterized query 필수

### 3. CSRF 보호
- ✅ CSRF 미들웨어 활성화
- ✅ CSRF_TRUSTED_ORIGINS 설정

### 4. XSS 방지
- ✅ DRF Serializer 사용 (자동 검증)
- ✅ 사용자 입력 검증

### 5. 인증/인가
- ✅ JWT 토큰 기반 인증
- ✅ Permission Classes 활용
- ⚠️ Rate Limiting 추가 권장

---

## 📝 추가 개선 사항

### 향후 개선 방안

1. **테스트 코드 작성**
   - 단위 테스트 (Unit Test)
   - 통합 테스트 (Integration Test)
   - API 엔드포인트 테스트

2. **성능 개선**
   - Redis 캐시 도입
   - Celery 비동기 작업 (임베딩 생성, 데이터 수집)
   - DB 쿼리 최적화

3. **모니터링**
   - Sentry (에러 추적)
   - Django Debug Toolbar (개발)
   - Prometheus + Grafana (운영)

4. **추천 알고리즘 개선**
   - A/B 테스트 프레임워크
   - 추천 결과 피드백 수집
   - 강화학습 기반 추천

5. **확장성**
   - PostgreSQL 전환
   - 마이크로서비스 아키텍처 검토
   - CDN 활용 (이미지, 정적 파일)

---

## 📞 문제 해결

### 자주 발생하는 문제

#### 1. KOPIS API 호출 실패
```bash
# Rate Limit 에러
→ 0.15초 간격 준수 확인

# Timeout 에러
→ timeout 값 증가 (기본 10초)
```

#### 2. 임베딩 생성 실패
```bash
# OpenAI API 키 확인
→ .env 파일의 GMS_KEY 확인

# Rate Limit
→ batch_size 줄이기 (10 → 5)
```

#### 3. CORS 에러
```bash
# CORS_ALLOWED_ORIGINS 확인
→ settings.py의 프론트엔드 URL 확인

# 미들웨어 순서 확인
→ CorsMiddleware가 CommonMiddleware 앞에 있는지 확인
```

#### 4. 마이그레이션 충돌
```bash
# 마이그레이션 리셋
python manage.py migrate --fake <app_name> zero
python manage.py migrate <app_name>

# 데이터베이스 초기화 (주의!)
rm db.sqlite3
python manage.py migrate
```

---

## 📚 참고 자료

### 공식 문서
- [Django 공식 문서](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [KOPIS API 문서](https://www.kopis.or.kr/por/cs/openapi/openApiList.do)
- [OpenAI API 문서](https://platform.openai.com/docs/)

### 추가 학습 자료
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering)

---

## 📄 라이센스

본 프로젝트는 교육 목적으로 제작되었습니다.

---

## 👥 제작자

**Backend Developer:** 이재호
**프로젝트 기간:** 2025.12.13 - 2025.12.23

---

**🎉 이 문서는 프론트엔드 개발자와 협업하는 팀원, 그리고 향후 유지보수를 담당할 개발자를 위해 작성되었습니다.**
