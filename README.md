# 🎭 공연 정보 플랫폼: Vue 3 + Django REST Framework

## 1. 개요
Vue 3와 Django REST Framework를 활용한 공연 정보 및 커뮤니티 플랫폼입니다. 프론트엔드와 백엔드를 완전히 분리한 SPA(Single Page Application) 아키텍처를 채택하였으며, KOPIS API 연동, AI 기반 검색, 하이브리드 추천 시스템, Tinder 스타일 온보딩을 제공합니다.

## 2. 목적 및 목표
- **프론트엔드/백엔드 분리**: Vue 3와 Django를 독립적으로 개발하고 API로 통신하는 현대적인 웹 아키텍처 구현
- **RESTful API 설계**: Django REST Framework의 ViewSet과 Router를 활용한 체계적인 API 엔드포인트 설계
- **AI 기반 검색**: OpenAI 임베딩을 활용한 의미 기반 공연 검색 시스템 구축
- **하이브리드 추천**: 7개 점수 함수를 조합한 개인화 추천 알고리즘 구현
- **컴포넌트 기반 개발**: Vue 3 Best Practices에 따른 재사용 가능한 컴포넌트 분리 및 Composables 패턴 활용
- **상태 관리**: Pinia를 활용한 중앙 집중식 상태 관리 구현
- **JWT 인증**: Access/Refresh Token 자동 갱신 시스템 구축

## 3. 기여자

| 역할 | 이름 | 담당 업무 |
|:---:|:---:|:---|
| **Leader** | **이재호** | 프로젝트 총괄, 백엔드 API 설계, 추천 시스템, KOPIS 연동, UI/UX 디자인 |
| **Member** | **임경수** | 프론트엔드 개발, 컴포넌트 아키텍처, AI 검색, Composables 패턴 구현 |

## 4. 개발 기간
- **2024.12.13 - 2024.12.23**

## 5. 📂 프로젝트 구조

```bash
final-pjt/
├── back/                           # Django 백엔드
│   ├── accounts/                   # 사용자 인증 및 온보딩
│   │   ├── models.py              # User, UserPreference, UserPerformanceSignal
│   │   ├── views/
│   │   │   ├── api_views.py       # UserViewSet
│   │   │   └── onboarding_views.py # OnboardingViewSet
│   │   └── services/
│   │       └── onboarding_service.py # 온보딩 로직
│   ├── performances/               # 공연 정보 관리
│   │   ├── models.py              # Performance, BoxOfficeRanking, PerformanceEmbedding
│   │   ├── views/
│   │   │   ├── api_views.py       # PerformanceViewSet (AI 검색, 좋아요)
│   │   │   └── management_api_views.py # 데이터 수집 API
│   │   ├── services/
│   │   │   ├── ai_search.py       # AI 검색 엔진
│   │   │   └── youtube_service.py # YouTube API 클라이언트
│   │   └── management/commands/   # Django 관리 커맨드
│   │       ├── collect_performances.py    # KOPIS 공연 데이터 수집
│   │       ├── collect_boxoffice.py       # 박스오피스 랭킹 수집
│   │       ├── generate_embeddings.py     # OpenAI 임베딩 생성
│   │       └── ...
│   ├── community/                  # 커뮤니티 (리뷰, 댓글)
│   │   ├── models.py              # Article, Comment
│   │   └── views/api_views.py     # ArticleViewSet, CommentViewSet
│   ├── recommendations/            # 추천 시스템
│   │   ├── models.py              # UserLog, RecommendationCache
│   │   ├── views/api_views.py     # RecommendationViewSet
│   │   └── services/engine.py     # 하이브리드 추천 엔진
│   ├── mypjt/                     # Django 프로젝트 설정
│   │   ├── settings.py            # CORS, JWT, DRF 설정
│   │   └── urls.py                # API 라우터 설정
│   ├── tests/                     # 테스트 스크립트
│   ├── requirements.txt
│   └── manage.py
│
├── front/                          # Vue 3 프론트엔드
│   ├── src/
│   │   ├── api/                   # API 클라이언트 모듈
│   │   │   ├── axios.js           # Axios 인스턴스 (JWT 인터셉터)
│   │   │   ├── performances.js    # 공연 API
│   │   │   ├── community.js       # 커뮤니티 API
│   │   │   ├── onboarding.js      # 온보딩 API
│   │   │   └── recommendations.js # 추천 API
│   │   ├── components/            # 재사용 가능한 컴포넌트
│   │   │   ├── AISearch/          # AI 검색
│   │   │   ├── BoxOffice/         # 박스오피스 (11개 컴포넌트)
│   │   │   ├── Common/            # 공통 컴포넌트
│   │   │   ├── Community/         # 커뮤니티 (12개 컴포넌트)
│   │   │   ├── Performance/       # 공연 목록
│   │   │   ├── PerformanceDetail/ # 공연 상세 (6개 컴포넌트)
│   │   │   ├── Recommendation/    # 추천
│   │   │   ├── User/              # 마이페이지 (9개 컴포넌트)
│   │   │   └── YouTube/           # YouTube 연동
│   │   ├── composables/           # Composition API 재사용 로직
│   │   │   ├── usePerformanceDetail.js
│   │   │   ├── useKakaoMap.js
│   │   │   ├── useArticleForm.js
│   │   │   └── ...
│   │   ├── stores/                # Pinia 스토어
│   │   │   ├── authStore.js       # 인증 (JWT 토큰 관리)
│   │   │   ├── performanceStore.js # 공연 데이터
│   │   │   ├── communityStore.js   # 커뮤니티
│   │   │   ├── aiSearchStore.js    # AI 검색 결과
│   │   │   ├── onboardingStore.js  # 온보딩 상태
│   │   │   ├── recommendationStore.js # 추천 데이터
│   │   │   └── themeStore.js       # 다크모드
│   │   ├── views/                 # 페이지 컴포넌트
│   │   │   ├── Auth/              # 인증 (로그인, 회원가입, 온보딩)
│   │   │   ├── Performance/       # 공연 (목록, 상세)
│   │   │   ├── Community/         # 커뮤니티 (리뷰, 베스트)
│   │   │   ├── Ranking/           # 랭킹 (전체, 장르별)
│   │   │   ├── User/              # 마이페이지
│   │   │   ├── LandingView.vue    # 홈 (박스오피스, 추천)
│   │   │   └── RecommandsView.vue # 추천 페이지
│   │   ├── router/index.js        # Vue Router (네비게이션 가드)
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
│
├── docs/                           # 프로젝트 문서
│   └── final-submission/
│       └── 01-프로젝트-개요/
│           ├── 02-백엔드-개요.md   # 백엔드 상세 문서
│           └── 03-프론트엔드-개요.md # 프론트엔드 상세 문서
│
└── README.md
```

## 6. 기술 스택

### Backend
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django 5.2-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/django rest framework-ff1709?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">

### Frontend
<img src="https://img.shields.io/badge/vue.js 3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"> <img src="https://img.shields.io/badge/vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"> <img src="https://img.shields.io/badge/pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black"> <img src="https://img.shields.io/badge/tailwind css-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white">

### AI & ML
<img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"> <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white">

### APIs & Libraries
<img src="https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white"> <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white"> <img src="https://img.shields.io/badge/KOPIS-00599C?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/YouTube API-FF0000?style=for-the-badge&logo=youtube&logoColor=white">

### Tools
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">

## ✨ 핵심 기능

### 1. AI 기반 공연 검색
* **의미 기반 검색**: OpenAI text-embedding-3-small 모델을 사용한 1536차원 벡터 검색
* **자연어 쿼리**: "감동적이고 웅장한 뮤지컬" 같은 자연어로 공연 검색
* **AI 코멘트**: GPT를 활용한 검색 결과 설명 자동 생성
* **임베딩 생성**: 공연명, 장르, 출연진, 줄거리를 결합한 임베딩
* **구현 위치**: `back/performances/services/ai_search.py`, `front/src/stores/aiSearchStore.js`

### 2. 하이브리드 추천 시스템
* **7개 점수 함수 조합**:
  - f1: 클릭/관심 로그 (10%)
  - f2: 취향 매칭 (15%)
  - f3: 위치 근접성 (25%)
  - f4: 대중성/박스오피스 (10%)
  - f5: 최신성 (10%)
  - f6: 협업 필터링 (10%)
  - f7: 임베딩 유사도 (20%)
* **캐싱 전략**: 1시간 유효 RecommendationCache
* **추천 이유 제공**: "🏠 거주 지역 근처에서 공연해요!" 등 개인화 메시지
* **구현 위치**: `back/recommendations/services/engine.py`

### 3. Tinder 스타일 온보딩
* **16개 후보 공연**: balanced 전략 (인기 8개 + 최신 4개 + 다양 장르 4개)
* **스와이프 인터페이스**: 보고싶어요(1.5), 모르겠어요(0.0), 안보고싶어요(-1.0)
* **선호도 벡터 생성**: 가중합 계산 후 L2 정규화로 1536차원 벡터 생성
* **온보딩 강제**: 미완료 시 자동 리다이렉트 (Vue Router 가드)
* **구현 위치**: `back/accounts/services/onboarding_service.py`, `front/src/views/Auth/OnboardingView.vue`

### 4. JWT 기반 인증 시스템
* **토큰 관리**: Access Token (1시간) + Refresh Token (7일)
* **자동 갱신**: Axios 인터셉터를 통한 401 에러 감지 및 자동 토큰 갱신
* **토큰 회전**: ROTATE_REFRESH_TOKENS=True로 보안 강화
* **구현 위치**: `back/mypjt/settings.py` (JWT 설정), `front/src/api/axios.js` (인터셉터)

### 5. 공연 정보 시스템
* **KOPIS API 연동**: 공연예술통합전산망 실시간 데이터 수집
* **박스오피스 랭킹**: 5개 장르별 주간/월간 랭킹 (연극, 뮤지컬, 클래식, 무용, 대중음악)
* **공연 상세 정보**: 포스터, 기간, 장소, 가격, 출연진, 줄거리, Kakao Map 연동
* **YouTube 연동**: 공연명으로 관련 영상 자동 검색 (캐시 1시간)
* **찜하기/관람함**: 낙관적 업데이트로 즉각적인 UI 반응
* **구현 위치**: `back/performances/`, `front/src/views/Performance/`

### 6. 커뮤니티 시스템
* **리뷰 CRUD**: 공연별 리뷰 작성, 수정, 삭제
* **별점 평가**: 1-5점 별점 시스템
* **베스트 리뷰**: 14일 이내 좋아요 많은 순 자동 선정
* **댓글 시스템**: 리뷰별 댓글 작성 및 관리
* **좋아요 토글**: 실시간 카운트 업데이트
* **구현 위치**: `back/community/`, `front/src/views/Community/`

### 7. Vue 3 Composables 패턴
* **로직 재사용**: usePerformanceDetail, useKakaoMap, useArticleForm 등 11개 composable
* **관심사 분리**: 컴포넌트에서 비즈니스 로직 분리
* **테스트 용이**: 독립적으로 테스트 가능한 함수형 로직
* **구현 위치**: `front/src/composables/`

### 8. 다크모드 & UX
* **전역 테마 토글**: localStorage 동기화
* **반응형 디자인**: Tailwind CSS 기반 모바일/태블릿/데스크톱 대응
* **로딩 상태 관리**: Pinia 스토어별 loading state
* **플로팅 액션 버튼**: 맨 위로 스크롤, 다크모드 토글
* **구현 위치**: `front/src/stores/themeStore.js`, `front/src/assets/styles/dark-mode.css`

## 📊 주요 API 엔드포인트

### 인증 & 온보딩
```
POST   /api/accounts/register/                  → 회원가입
POST   /api/accounts/token/                     → 로그인 (JWT 발급)
POST   /api/accounts/token/refresh/             → Access Token 갱신
GET    /api/accounts/onboarding/candidates/    → 온보딩 후보 공연 (16개)
POST   /api/accounts/onboarding/signals/       → 사용자 선호도 신호 저장
POST   /api/accounts/onboarding/complete/      → 온보딩 완료
```

### 공연 정보
```
GET    /api/performances/                       → 공연 목록 (필터링, 검색, 페이지네이션)
GET    /api/performances/<mt20id>/              → 공연 상세
POST   /api/performances/ai-search/             → AI 의미 기반 검색
POST   /api/performances/<mt20id>/like/         → 찜하기/취소 토글
GET    /api/performances/boxoffice-genre/       → 장르별 박스오피스
GET    /api/performances/boxoffice-all/         → 전체 박스오피스 Top 10
```

### 커뮤니티
```
GET    /api/community/articles/                 → 게시글 목록
POST   /api/community/articles/                 → 게시글 작성
GET    /api/community/articles/best-reviews/    → 베스트 리뷰 (14일 이내)
POST   /api/community/articles/<id>/like/       → 게시글 좋아요
GET    /api/community/comments/                 → 댓글 목록
POST   /api/community/comments/                 → 댓글 작성
```

### 추천 시스템
```
GET    /api/recommendations/                    → 개인화 추천 (Top-N)
POST   /api/recommendations/log/                → 행동 로그 저장 (view, like, search)
POST   /api/recommendations/refresh/            → 추천 캐시 강제 갱신
```

## 🔄 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                     Vue 3 Frontend                           │
│                  (localhost:5173)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Components  │  │   Stores    │  │ Composables │         │
│  │  (60+ 개)   │→ │   (Pinia)   │→ │  (11개)     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            ↓                                 │
│                    ┌──────────────┐                          │
│                    │ Axios Client │ (JWT Interceptor)        │
│                    └──────────────┘                          │
└─────────────────────────│────────────────────────────────────┘
                          │ HTTP + JWT
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              Django REST Framework Backend                   │
│                   (127.0.0.1:8000)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   ViewSets   │→ │ Serializers  │→ │    Models    │      │
│  │              │  │              │  │              │      │
│  │ - Performance│  │ - Performance│  │ - Performance│      │
│  │ - Article    │  │ - Article    │  │ - User       │      │
│  │ - User       │  │ - User       │  │ - Article    │      │
│  │ - Recommend  │  │ - Recommend  │  │ - Embedding  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                                      │             │
│         ↓                                      ↓             │
│  ┌──────────────┐                      ┌─────────────┐      │
│  │   Services   │                      │  SQLite DB  │      │
│  │              │                      │  (113 MB)   │      │
│  │ - AI Search  │                      └─────────────┘      │
│  │ - Recommend  │                                           │
│  │ - Onboarding │                                           │
│  │ - YouTube    │                                           │
│  └──────────────┘                                           │
│         │                                                    │
│         ↓                                                    │
│  ┌──────────────────────────────────────────┐               │
│  │         External APIs                    │               │
│  │  - OpenAI (Embedding, GPT)               │               │
│  │  - KOPIS (공연 데이터)                     │               │
│  │  - YouTube (영상)                         │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 실행 방법

### 1. 백엔드 설정 및 실행

```bash
cd back

# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env_ .env
# .env 파일에 API 키 입력 (KOPIS_API, GMS_KEY, YOUTUBE_API_KEY)

# 데이터베이스 마이그레이션
python manage.py migrate

# 슈퍼유저 생성 (관리자 페이지 접근용)
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

### 2. 프론트엔드 설정 및 실행

```bash
cd front

# 의존성 설치 (최초 1회)
npm install

# 환경 변수 설정 (선택사항)
cp .env.production .env
# .env 파일에 Kakao Map API 키 입력

# 개발 서버 실행
npm run dev
```

### 3. 접속

- **프론트엔드**: http://localhost:5173
- **백엔드 API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

### 4. 초기 데이터 수집 (선택사항)

```bash
cd back

# 1. 공연 데이터 수집 (최근 1년)
python manage.py collect_performances --start-date 2024-01-01 --end-date 2024-12-31

# 2. 공연 상세 정보 수집
python manage.py collect_performance_detail

# 3. 박스오피스 랭킹 수집
python manage.py collect_boxoffice --date 20241223 --period week

# 4. AI 검색용 임베딩 생성
python manage.py generate_embeddings --batch-size 10
```

## 📚 문서

- **백엔드 상세 문서**: [docs/final-submission/01-프로젝트-개요/02-백엔드-개요.md](docs/final-submission/01-프로젝트-개요/02-백엔드-개요.md)
- **프론트엔드 상세 문서**: [docs/final-submission/01-프로젝트-개요/03-프론트엔드-개요.md](docs/final-submission/01-프로젝트-개요/03-프론트엔드-개요.md)
- **백엔드 README**: [back/README.md](back/README.md)
- **프론트엔드 README**: [front/README.md](front/README.md)

## 🎓 주요 학습 성과

### 백엔드
1. **Django REST Framework 심화**: ViewSet, Serializer, Permission, Filter 활용
2. **AI/ML 통합**: OpenAI API 연동, 벡터 검색, 임베딩 생성
3. **추천 알고리즘**: 7개 점수 함수를 조합한 하이브리드 추천 시스템 설계
4. **외부 API 연동**: KOPIS, YouTube, OpenAI API Rate Limiting 및 에러 핸들링
5. **Django 관리 커맨드**: 데이터 수집 자동화 스크립트 작성
6. **캐싱 전략**: DB 쿼리 최적화 및 API 응답 캐싱

### 프론트엔드
1. **Vue 3 Composition API**: `<script setup>` 문법, 반응형 상태 관리
2. **Composables 패턴**: 로직 재사용을 위한 함수형 프로그래밍 접근
3. **Pinia 상태 관리**: 모듈화된 스토어 설계, localStorage 동기화
4. **컴포넌트 아키텍처**: 60+ 컴포넌트를 단일 책임 원칙에 따라 분리
5. **Axios 인터셉터**: JWT 자동 갱신, 에러 핸들링
6. **Tailwind CSS**: 유틸리티 우선 CSS, 다크모드 구현
7. **Vue Router**: 네비게이션 가드, 온보딩 강제 리다이렉트

## 🔮 향후 개선 방안

### 기능 확장
1. **실시간 기능**: WebSocket을 활용한 실시간 알림 및 채팅
2. **소셜 기능**: 사용자 간 팔로우, 리뷰 공유, 활동 피드
3. **공연 일정 알림**: 찜한 공연의 티켓 오픈 알림
4. **티켓 예매 연동**: 예매처 API 연동

### 기술 개선
1. **테스트 코드**: Vitest (프론트엔드), pytest (백엔드)
2. **성능 최적화**: Redis 캐시, Celery 비동기 작업
3. **모니터링**: Sentry (에러 추적), Prometheus (메트릭)
4. **CI/CD**: GitHub Actions 자동 배포
5. **PostgreSQL 전환**: SQLite → PostgreSQL 마이그레이션
6. **CDN 활용**: 이미지, 정적 파일 CDN 제공

## 📄 라이센스
데이터 KOPIS제공  
본 프로젝트는 교육 목적으로 제작되었습니다.

---

**🎉 SSAFY 12기 1학기 관통 프로젝트 - 공연 정보 플랫폼**
