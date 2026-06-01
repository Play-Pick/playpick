<div align="center">

# PlayPick

<img src="front/src/assets/images/logo-light.png" width="180" alt="PlayPick logo" />

**공연 데이터를 수집하고, 사용자의 취향을 학습해 AI 검색과 개인화 추천으로 공연 발견을 돕는 커뮤니티 플랫폼**

<br>

![Vue](https://img.shields.io/badge/Vue_3.5-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Vite](https://img.shields.io/badge/Vite_7-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia_3-FFD859?style=for-the-badge&logo=pinia&logoColor=111111)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS_3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF_3.16-A30000?style=for-the-badge&logo=django&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_Embedding-412991?style=for-the-badge&logo=openai&logoColor=white)
![KOPIS](https://img.shields.io/badge/KOPIS_API-1F2937?style=for-the-badge)

</div>

---

## 프로젝트 소개

PlayPick은 공연을 고를 때 생기는 정보 탐색 비용을 줄이기 위한 공연 큐레이션 서비스입니다.

공연 정보는 KOPIS 데이터를 기반으로 수집하고, 사용자는 장르, 배우, 지역, 관람 이력, 찜, 조회 로그, 온보딩 반응을 통해 자신의 취향을 서비스에 남깁니다. PlayPick은 이 데이터를 기반으로 자연어 의미 검색, 임베딩 유사도, 박스오피스 랭킹, 지역/취향/행동 로그를 함께 고려한 추천 결과를 제공합니다.

서비스는 다음 흐름을 목표로 합니다.

1. 사용자가 온보딩에서 보고 싶은 공연과 보고 싶지 않은 공연을 선택한다.
2. 선택 신호를 1536차원 선호도 벡터로 변환한다.
3. 공연 목록, 랭킹, 지도, YouTube 영상으로 공연 정보를 탐색한다.
4. AI 검색과 하이브리드 추천으로 취향에 맞는 공연을 발견한다.
5. 찜, 관람함, 리뷰, 댓글, 팔로우로 공연 경험을 기록하고 공유한다.

---

## 핵심 기능

### AI 의미 기반 공연 검색

- OpenAI `text-embedding-3-small` 임베딩으로 자연어 질의를 벡터화한다.
- 공연명, 장르, 출연진, 줄거리 기반 공연 임베딩과 코사인 유사도를 계산한다.
- "우울할 때 위로가 되는 공연", "아이와 보기 좋은 뮤지컬" 같은 문장형 검색을 지원한다.
- 검색 결과 상위 공연에는 LLM 기반 추천 문구를 생성한다.
- 구현 위치: `back/performances/services/ai_search.py`, `front/src/stores/aiSearchStore.js`

### 하이브리드 개인화 추천

PlayPick의 추천 엔진은 단일 기준이 아니라 7개 점수 함수를 가중 합산해 공연을 추천합니다.

| 점수 함수 | 가중치 | 기준 |
|---|---:|---|
| `f1_click` | 20% | 최근 조회, 찜, 검색 로그와 시간 감쇠 |
| `f2_preference` | 15% | 선호 장르/태그, 선호 배우 매칭 |
| `f3_location` | 10% | 사용자 지역과 공연 지역 일치 |
| `f4_popularity` | 15% | 박스오피스와 사전 계산된 대중성 지표 |
| `f5_recency` | 10% | 공연 시작일 기준 최신성/임박도 |
| `f6_collaborative` | 10% | 찜한 공연과 유사한 공연 |
| `f7_embedding` | 20% | 사용자 선호도 벡터와 공연 임베딩 유사도 |

- 추천 결과는 `RecommendationCache`에 저장해 반복 계산 비용을 줄인다.
- 추천 사유는 가장 높은 점수를 만든 요인을 기준으로 생성한다.
- 구현 위치: `back/recommendations/services/engine.py`, `front/src/components/Recommendation/`

### Tinder 스타일 온보딩

- 온보딩 후보는 인기 공연, 최신 공연, 다양한 장르 샘플을 섞어 구성한다.
- 사용자는 공연 카드에 대해 `보고싶어요(1.5)`, `모르겠어요(0.0)`, `안보고싶어요(-1.0)` 신호를 남긴다.
- 각 공연의 임베딩에 사용자 반응 가중치를 곱해 합산하고 L2 정규화해 선호도 벡터를 만든다.
- 온보딩을 끝내지 않은 사용자는 주요 화면 진입 전 온보딩으로 유도된다.
- 구현 위치: `back/accounts/services/onboarding_service.py`, `front/src/views/Auth/OnboardingView.vue`

### 공연 정보, 랭킹, 외부 API 연동

- KOPIS API로 공연 목록, 공연 상세, 박스오피스 데이터를 수집한다.
- 장르별/전체 박스오피스 랭킹과 하이라이트 캐러셀을 제공한다.
- Kakao Map으로 공연장 위치를 표시한다.
- YouTube Data API로 공연 관련 영상과 추천 플레이리스트를 제공하고, DB 캐시로 호출 비용을 줄인다.
- 구현 위치: `back/performances/`, `front/src/views/Performance/`, `front/src/views/Ranking/`

### 커뮤니티와 사용자 활동

- 공연글과 일반글을 구분해 후기, 기대평, Q&A, 자유글, 정보공유 카테고리를 제공한다.
- 게시글 CRUD, 댓글, 좋아요, 별점, 베스트 리뷰를 지원한다.
- 찜한 공연, 관람한 공연, 작성 글/댓글, 선호도 수정, 팔로우를 마이페이지에서 관리한다.
- 구현 위치: `back/community/`, `front/src/views/Community/`, `front/src/views/User/`

### Vue 3 프론트엔드 구조

- Vue 3 Composition API와 Pinia 기반으로 화면 상태와 API 호출을 분리했다.
- `usePerformanceDetail`, `useKakaoMap`, `useArticleForm`, `useMyPage` 같은 composable로 화면 로직을 재사용한다.
- 다크모드, 반응형 레이아웃, 낙관적 UI 업데이트를 적용했다.
- 구현 위치: `front/src/components/`, `front/src/composables/`, `front/src/stores/`

---

## 시스템 아키텍처

```text
User Browser
    |
    | Vue 3 + Vite
    | - Vue Router
    | - Pinia Store
    | - Composables
    | - Axios JWT Interceptor
    v
Django REST Framework API
    |
    +--> accounts
    |     +--> JWT Auth
    |     +--> Onboarding Signal
    |     +--> User Preference Vector
    |
    +--> performances
    |     +--> KOPIS Data Collection
    |     +--> Performance / Detail / Ranking
    |     +--> AI Semantic Search
    |     +--> YouTube Cache
    |
    +--> recommendations
    |     +--> UserLog
    |     +--> Hybrid Recommendation Engine
    |     +--> RecommendationCache
    |
    +--> community
          +--> Article / Comment / Like

Data & External Services
    |
    +--> SQLite / PostgreSQL-compatible Django ORM
    +--> KOPIS API
    +--> OpenAI-compatible GMS API
    +--> Kakao Maps API
    +--> YouTube Data API
```

### 데이터 흐름

```text
사용자 행동
  -> Vue Component
  -> Pinia Store / Composable
  -> Axios API Module
  -> Django ViewSet
  -> Serializer / Service
  -> Model / External API
  -> 추천, 검색, 랭킹, 커뮤니티 UI 갱신
```

---

## 기술 스택

| 구분 | 스택 |
|---|---|
| Frontend | Vue 3.5.25, Vite 7.2.4, Pinia 3.0.4, Vue Router 4.6.3, Axios 1.13.2 |
| Styling | Tailwind CSS 3.4.0, PostCSS, Autoprefixer |
| Backend | Python, Django 5.2.8, Django REST Framework 3.16.1 |
| Auth | djangorestframework-simplejwt 5.5.1, JWT Access/Refresh Token |
| Data / ML | SQLite, NumPy 2.3.5, scikit-learn 1.8.0, SciPy 1.16.3 |
| AI | OpenAI SDK 2.14.0, `text-embedding-3-small`, GPT 기반 추천 문구 생성 |
| External API | KOPIS API, Kakao Maps API, YouTube Data API |
| Deploy | Gunicorn, WhiteNoise, AWS EC2 배포 문서 |

---

## 모듈별 역할

| 모듈 | 주요 역할 | 핵심 파일 |
|---|---|---|
| `front/` | Vue SPA, 화면, 상태 관리, API 클라이언트 | `src/router`, `src/stores`, `src/components` |
| `back/accounts/` | 사용자, JWT 인증, 온보딩, 선호도 벡터, 관람함 | `models.py`, `views/`, `services/onboarding_service.py` |
| `back/performances/` | 공연 데이터, 랭킹, 찜, AI 검색, YouTube 캐시, KOPIS 수집 | `models.py`, `views/`, `services/`, `management/commands/` |
| `back/recommendations/` | 행동 로그, 추천 캐시, 하이브리드 추천 엔진 | `models.py`, `services/engine.py` |
| `back/community/` | 게시글, 댓글, 좋아요, 베스트 리뷰 | `models.py`, `views/api_views.py` |
| `docs/final-submission/` | 최종 제출용 프로젝트 개요, 기술 문서, 기능 명세, API 문서, 배포 가이드 | 제출 문서 모음 |
| `docs/development-archive/` | 개발 중 작성한 가이드, 리팩토링 기록, 테스트/실험 문서 | 개발 아카이브 |

---

## 주요 API

| 영역 | 엔드포인트 | 설명 |
|---|---|---|
| Auth | `POST /api/accounts/register/` | 회원가입 |
| Auth | `POST /api/accounts/token/` | JWT 로그인 |
| Auth | `POST /api/accounts/token/refresh/` | Access Token 갱신 |
| User | `GET /api/accounts/users/me/` | 내 정보 조회 |
| User | `PATCH /api/accounts/users/update_profile/` | 프로필 수정 |
| User | `POST /api/accounts/users/{id}/follow/` | 팔로우/언팔로우 |
| Onboarding | `GET /api/accounts/onboarding/candidates/` | 온보딩 후보 공연 조회 |
| Onboarding | `POST /api/accounts/onboarding/signals/` | 온보딩 반응 저장 |
| Onboarding | `POST /api/accounts/onboarding/complete/` | 선호도 벡터 생성 및 온보딩 완료 |
| Performance | `GET /api/performances/` | 공연 목록 조회 |
| Performance | `GET /api/performances/{id}/` | 공연 상세 조회 |
| Performance | `POST /api/performances/{id}/like/` | 공연 찜하기/취소 |
| Performance | `POST /api/performances/ai-search/` | AI 의미 검색 |
| Performance | `GET /api/performances/youtube/playlist/` | YouTube 추천 영상 목록 |
| Ranking | `GET /api/performances/boxoffice-all/` | 전체 박스오피스 랭킹 |
| Ranking | `GET /api/performances/boxoffice-genre/` | 장르별 박스오피스 랭킹 |
| Community | `GET /api/community/articles/` | 게시글 목록 |
| Community | `POST /api/community/articles/` | 게시글 작성 |
| Community | `POST /api/community/articles/{id}/like/` | 게시글 좋아요/취소 |
| Community | `GET /api/community/articles/best-reviews/` | 베스트 리뷰 |
| Recommendation | `GET /api/recommendations/` | 개인화 추천 목록 |
| Recommendation | `POST /api/recommendations/log/` | 사용자 행동 로그 저장 |

---

## 저장소 구조

```text
final-pjt/
├── back/
│   ├── accounts/                 # 사용자, 인증, 온보딩, 선호도 벡터
│   ├── community/                # 게시글, 댓글, 좋아요
│   ├── performances/             # 공연, 랭킹, AI 검색, KOPIS/YouTube 연동
│   │   ├── management/commands/   # 데이터 수집과 임베딩 생성 커맨드
│   │   ├── services/              # ai_search, youtube_service
│   │   └── views/                 # 공연 API, 관리자 수집 API
│   ├── recommendations/          # 추천 로그, 캐시, 추천 엔진
│   ├── mypjt/                    # Django 설정
│   ├── fixtures/                 # 초기/테스트 데이터
│   ├── embeddings/               # 임베딩 파일
│   ├── manage.py
│   └── requirements.txt
├── front/
│   ├── public/
│   ├── src/
│   │   ├── api/                  # Axios API 모듈
│   │   ├── assets/               # 로고, 스타일
│   │   ├── components/           # 기능별 재사용 컴포넌트
│   │   ├── composables/          # Composition API 재사용 로직
│   │   ├── router/               # Vue Router와 가드
│   │   ├── stores/               # Pinia 상태 관리
│   │   └── views/                # 화면 단위 페이지
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── final-submission/         # 최종 제출 문서
│   ├── development-archive/      # 개발 과정 문서
│   └── project-files/            # 제출용 첨부 파일
├── back/README.md
├── front/README.md
└── README.md
```

---

## 실행 방법

### 사전 준비

- Python 3.x
- Node.js `^20.19.0` 또는 `>=22.12.0`
- KOPIS API Key
- GMS/OpenAI-compatible API Key
- Kakao Maps JavaScript API Key
- YouTube Data API Key

### 백엔드 실행

```bash
cd back
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

기본 API 주소는 `http://127.0.0.1:8000/api/`입니다.

### 프론트엔드 실행

```bash
cd front
npm install
npm run dev
```

기본 프론트엔드 주소는 `http://localhost:5173`입니다.

### 환경 변수

| 위치 | 변수 |
|---|---|
| `back/.env` | `SECRET_KEY`, `KOPIS_API`, `KOPIS_URL`, `GMS_KEY`, `YOUTUBE_API_KEY`, `YOUTUBE_PLAYLIST_ID_MAIN` |
| `front/.env` | `VITE_API_BASE_URL`, `VITE_KAKAO_MAP_API_KEY` |
| `front/.env.production` | `VITE_API_BASE_URL` |

### 데이터 수집과 임베딩 생성

```bash
cd back
python manage.py collect_performances
python manage.py collect_performance_detail
python manage.py collect_boxoffice
python manage.py generate_embeddings
```

초기 데이터 로드와 배포 서버 실행 방법은 [AWS 배포 실행방법](docs/final-submission/05-배포-가이드/01-AWS-배포-실행방법.md)을 참고합니다.

---

## 주요 문서

| 문서 | 설명 |
|---|---|
| [프로젝트 종합문서](docs/final-submission/01-프로젝트-개요/01-프로젝트-종합문서.md) | 전체 기능, 구조, API, 데이터베이스 설명 |
| [백엔드 개요](docs/final-submission/01-프로젝트-개요/02-백엔드-개요.md) | Django 백엔드 상세 문서 |
| [프론트엔드 개요](docs/final-submission/01-프로젝트-개요/03-프론트엔드-개요.md) | Vue 프론트엔드 상세 문서 |
| [AWS 배포 실행방법](docs/final-submission/05-배포-가이드/01-AWS-배포-실행방법.md) | AWS 배포 서버 실행과 데이터 로드 가이드 |
| [추천 알고리즘](docs/final-submission/02-기술-문서/01-추천알고리즘.md) | 추천 알고리즘 설계 |
| [AI 검색 엔진](docs/final-submission/02-기술-문서/02-AI-검색엔진.md) | AI 검색 구현 정리 |
| [온보딩 시스템](docs/final-submission/03-기능-명세/01-온보딩시스템.md) | 온보딩 기능 명세 |
| [YouTube 연동](docs/final-submission/02-기술-문서/05-YouTube-연동.md) | YouTube 연동 명세 |
| [백엔드 README](back/README.md) | 백엔드 실행/구조 요약 |
| [프론트엔드 README](front/README.md) | 프론트엔드 실행/구조 요약 |

---

## 협업 방식

### 브랜치 전략

| 브랜치 | 역할 |
|---|---|
| `master` | 최종 검증된 배포 버전 |
| `develop` | 기능 통합과 QA 기준 브랜치 |
| `feature/<feature-name>` | 기능 단위 개발 브랜치 |

### 커밋 타입

```text
<type>: <subject>
```

| 타입 | 용도 |
|---|---|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `refactor` | 리팩토링 |
| `docs` | 문서 수정 |
| `style` | 포맷팅, 스타일 수정 |
| `test` | 테스트 코드 |
| `chore` | 빌드, 설정, 기타 작업 |

---

## 팀원

<table>
  <tr>
    <td align="center" width="180">
      <strong>이재호</strong><br>
      <sub>팀장</sub><br><br>
      <img src="https://img.shields.io/badge/FrontEnd-2F80ED?style=flat-square&logo=vue.js&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/Design-FF4D8D?style=flat-square&logo=figma&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/Docs-1F5F8B?style=flat-square&logo=readthedocs&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/발표-8E24AA?style=flat-square" />
    </td>
    <td align="center" width="180">
      <strong>임경수</strong><br>
      <sub>팀원</sub><br><br>
      <img src="https://img.shields.io/badge/Backend-43A047?style=flat-square&logo=django&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/AI-1565C0?style=flat-square&logo=openai&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/Infra-F9A825?style=flat-square&logo=amazonaws&logoColor=white" /><br>
      <img src="https://img.shields.io/badge/FullStack-37474F?style=flat-square" />
    </td>
  </tr>
</table>

| 이름 | 주요 담당 |
|---|---|
| 이재호 | 프론트엔드 화면 구현, UI/UX 디자인, 발표 자료 및 발표, 커뮤니티 페이지, 온보딩/YouTube/마이페이지 연동, 문서 정리 |
| 임경수 | Django API, KOPIS 데이터 수집, AI 검색/추천 시스템, 임베딩 테이블 분리, 배포 설정, 프론트엔드 리팩토링 |

## 프로젝트 기간

2025.12.13 - 2025.12.23
