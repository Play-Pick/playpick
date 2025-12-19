# 11-pjt: Vue 3 + Django REST Framework 영화 추천 커뮤니티 서비스

## 1. 개요
본 프로젝트는 Vue 3와 Django REST Framework를 활용하여 영화 추천 및 커뮤니티 서비스를 구현했습니다. 프론트엔드와 백엔드를 완전히 분리한 SPA(Single Page Application) 아키텍처를 채택하였으며, RESTful API 통신, JWT 인증, 그리고 Vue 3 Composition API와 Pinia를 통한 상태 관리를 구현했습니다.

## 2. 목적 및 목표
- **프론트엔드/백엔드 분리**: Vue 3와 Django를 독립적으로 개발하고 API로 통신하는 현대적인 웹 아키텍처 구현
- **RESTful API 설계**: Django REST Framework의 ViewSet과 Router를 활용한 체계적인 API 엔드포인트 설계
- **컴포넌트 기반 개발**: Vue 3 Best Practices에 따른 재사용 가능한 컴포넌트 분리 및 구성
- **상태 관리**: Pinia를 활용한 중앙 집중식 상태 관리 구현
- **JWT 인증**: 토큰 기반 인증 시스템 구축

## 3. 기여자

| 역할 | 이름 | 담당 업무 |
|:---:|:---:|:---|
| **Leader** | **이재호** | 프로젝트 총괄, 백엔드 API 설계, 공연 정보 시스템 구축 |
| **Member** | **임경수** | 프론트엔드 개발, 컴포넌트 리팩토링, UI/UX 디자인 |

## 4. 개발 기간
- 2025.12.13 - 2025.12.14

## 5. 📂 File Structure

```bash
11-pjt/
├── back/                           # Django 백엔드
│   ├── accounts/                   # 사용자 인증 및 관리
│   │   ├── models.py              # User 모델
│   │   ├── serializers.py         # User, Register 시리얼라이저
│   │   ├── api_views.py           # UserViewSet (팔로우, 프로필)
│   │   └── urls.py
│   ├── community/                  # 커뮤니티 (리뷰, 댓글)
│   │   ├── models.py              # Review, Comment 모델
│   │   ├── serializers.py         # Review, Comment 시리얼라이저
│   │   ├── api_views.py           # ReviewViewSet, CommentViewSet
│   │   └── urls.py
│   ├── performances/               # 공연 정보 관리
│   │   ├── models.py              # Performance, BoxOfficeRanking 모델
│   │   ├── serializers.py         # Performance, BoxOffice 시리얼라이저
│   │   ├── api_views.py           # PerformanceViewSet, BoxOfficeViewSet
│   │   └── urls.py
│   ├── mypjt/                     # Django 프로젝트 설정
│   │   ├── settings.py            # CORS, JWT, DRF 설정
│   │   └── urls.py                # API 라우터 설정
│   ├── requirements.txt
│   └── manage.py
│
├── front/                          # Vue 3 프론트엔드
│   ├── src/
│   │   ├── api/                   # API 클라이언트 모듈
│   │   │   ├── axios.js           # Axios 인스턴스 설정
│   │   │   ├── performances.js    # 공연 API
│   │   │   ├── community.js       # 커뮤니티 API
│   │   │   └── users.js           # 사용자 API
│   │   ├── components/            # 재사용 가능한 컴포넌트
│   │   │   ├── BoxOffice/         # 박스오피스 관련
│   │   │   │   ├── BoxOfficeCard.vue
│   │   │   │   ├── BoxOfficeCarousel.vue
│   │   │   │   ├── GenreTab.vue
│   │   │   │   └── RankBadge.vue
│   │   │   ├── Performance/       # 공연 목록 관련
│   │   │   │   ├── PerformanceCard.vue
│   │   │   │   ├── PerformanceFilters.vue
│   │   │   │   └── PerformanceGrid.vue
│   │   │   └── PerformanceDetail/ # 공연 상세 관련
│   │   │       ├── HeaderSection.vue
│   │   │       └── MapModal.vue
│   │   ├── views/                 # 페이지 뷰
│   │   │   ├── LandingView.vue    # 랜딩 페이지
│   │   │   ├── HomeView.vue       # 홈 (박스오피스)
│   │   │   ├── PerformanceListView.vue  # 공연 목록
│   │   │   ├── PerformanceDetailView.vue # 공연 상세
│   │   │   ├── CommunityView.vue  # 커뮤니티
│   │   │   ├── LoginView.vue      # 로그인
│   │   │   └── RegisterView.vue   # 회원가입
│   │   ├── stores/                # Pinia 스토어
│   │   │   ├── performanceStore.js
│   │   │   ├── communityStore.js
│   │   │   └── userStore.js
│   │   ├── router/                # Vue Router
│   │   │   └── index.js
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── PROJECT_STRUCTURE.md            # 프로젝트 구조 및 동작 방식 설명
├── SETUP.md                        # 설치 및 실행 가이드
├── JWT_AUTH_GUIDE.md              # JWT 인증 가이드
└── JWT_IMPLEMENTATION_GUIDE.md    # JWT 구현 상세 가이드
```

## 6. 기술 스택

### Backend
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/django rest framework-ff1709?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">

### Frontend
<img src="https://img.shields.io/badge/vue.js 3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"> <img src="https://img.shields.io/badge/vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"> <img src="https://img.shields.io/badge/pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black"> <img src="https://img.shields.io/badge/tailwind css-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white">

### APIs & Libraries
<img src="https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white"> <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">

### Tools
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">

## ✨ Key Features

### 1. 프론트엔드/백엔드 완전 분리 아키텍처
* **독립적인 개발 환경**: Vue 개발 서버(localhost:5173)와 Django 서버(127.0.0.1:8000) 분리 운영
* **RESTful API 통신**: Django REST Framework의 ViewSet과 Router를 활용한 체계적인 엔드포인트 구성
* **CORS 설정**: django-cors-headers를 통한 안전한 크로스 오리진 요청 처리
* **구현 위치**:
  - Backend: `back/mypjt/settings.py` (CORS 설정)
  - Frontend: `front/src/api/axios.js` (Axios 인스턴스)

### 2. JWT 기반 인증 시스템
* **토큰 기반 인증**: djangorestframework-simplejwt를 활용한 Access/Refresh 토큰 발급
* **자동 토큰 관리**: Axios 인터셉터를 통한 요청 시 자동 토큰 첨부
* **토큰 갱신**: Refresh 토큰을 활용한 자동 토큰 갱신 메커니즘
* **구현 위치**:
  - Backend: `back/accounts/api_views.py` (토큰 발급)
  - Frontend: `front/src/stores/userStore.js` (토큰 저장/관리)
  - Frontend: `front/src/api/axios.js` (인터셉터)

### 3. Vue 3 컴포넌트 기반 아키텍처
* **단일 책임 원칙**: 각 컴포넌트가 하나의 기능만 담당하도록 분리
* **컴포넌트 계층 구조**:
  - `BoxOffice/`: 박스오피스 랭킹 표시 (카드, 캐러셀, 장르 탭, 순위 뱃지)
  - `Performance/`: 공연 목록 표시 (카드, 필터, 그리드)
  - `PerformanceDetail/`: 공연 상세 정보 (헤더, 지도 모달)
* **Props/Events 패턴**: 부모-자식 컴포넌트 간 명확한 데이터 흐름
* **Composition API**: `<script setup>` 문법을 활용한 간결한 코드 작성
* **구현 위치**:
  - `front/src/components/` (모든 재사용 컴포넌트)
  - `front/src/views/` (페이지 레벨 뷰 컴포넌트)

### 4. Pinia를 활용한 중앙 집중식 상태 관리
* **모듈화된 스토어**:
  - `performanceStore`: 공연 목록, 상세 정보, 장르 필터링
  - `communityStore`: 리뷰 목록, 댓글, 좋아요
  - `userStore`: 사용자 인증, 프로필, 팔로우
* **API 통신 로직 분리**: 컴포넌트에서 API 직접 호출 방지
* **반응형 상태**: Vue의 반응성 시스템을 활용한 자동 UI 업데이트
* **구현 위치**:
  - `front/src/stores/performanceStore.js`
  - `front/src/stores/communityStore.js`
  - `front/src/stores/userStore.js`

### 5. 공연 정보 시스템
* **박스오피스 랭킹**: 장르별 주간 박스오피스 순위 표시
* **공연 목록 필터링**: 장르, 지역, 상태별 필터링 기능
* **공연 상세 정보**: 포스터, 기간, 장소, 가격, 시놀시스 등 상세 정보 제공
* **구현 위치**:
  - Backend: `back/performances/api_views.py`
  - Frontend: `front/src/views/PerformanceListView.vue`

### 6. 커뮤니티 기능
* **리뷰 CRUD**: 공연에 대한 리뷰 작성, 조회, 수정, 삭제
* **댓글 시스템**: 리뷰에 대한 댓글 작성 및 관리
* **좋아요 기능**: 리뷰 좋아요/취소 토글 (실시간 카운트 업데이트)
* **구현 위치**:
  - Backend: `back/community/api_views.py`
  - Frontend: `front/src/views/CommunityView.vue`

### 7. 사용자 상호작용
* **팔로우 시스템**: 사용자 간 팔로우/언팔로우 기능
* **프로필 페이지**: 사용자 정보, 작성한 리뷰, 팔로워/팔로잉 목록
* **구현 위치**:
  - Backend: `back/accounts/api_views.py` (UserViewSet.follow)
  - Frontend: `front/src/stores/userStore.js`

## 📊 API 엔드포인트

### 공연 관련
```
GET    /api/performances/              → 공연 목록
GET    /api/performances/{id}/         → 공연 상세
GET    /api/performances/genres/       → 장르 목록
GET    /api/boxoffice/                 → 박스오피스 목록
GET    /api/boxoffice/latest_by_genre/ → 장르별 최신 랭킹
```

### 커뮤니티 관련
```
GET    /api/reviews/           → 리뷰 목록
POST   /api/reviews/           → 리뷰 생성
GET    /api/reviews/{id}/      → 리뷰 상세
PUT    /api/reviews/{id}/      → 리뷰 수정
DELETE /api/reviews/{id}/      → 리뷰 삭제
POST   /api/reviews/{id}/like/ → 좋아요/취소

GET    /api/comments/?review={id}  → 댓글 목록
POST   /api/comments/              → 댓글 생성
DELETE /api/comments/{id}/          → 댓글 삭제
```

### 사용자 관련
```
POST   /api/auth/register/      → 회원가입
POST   /api/auth/login/         → 로그인
GET    /api/users/              → 사용자 목록
GET    /api/users/{id}/         → 사용자 상세
GET    /api/users/me/           → 현재 사용자 정보
POST   /api/users/{id}/follow/  → 팔로우/언팔로우
```

## 🔄 데이터 흐름도

```
┌─────────────────┐
│  Vue Component  │  ← 사용자 인터페이스
└────────┬────────┘
         │
         │ 1. 스토어 액션 호출
         ↓
┌─────────────────┐
│  Pinia Store    │  ← 상태 관리 (performanceStore, communityStore, userStore)
└────────┬────────┘
         │
         │ 2. API 함수 호출
         ↓
┌─────────────────┐
│  API Module     │  ← API 요청 함수 (performances.js, community.js, users.js)
└────────┬────────┘
         │
         │ 3. Axios 인스턴스 사용
         ↓
┌─────────────────┐
│  Axios Client   │  ← HTTP 요청 (인터셉터, 토큰 자동 첨부)
└────────┬────────┘
         │
         │ 4. HTTP 요청 (CORS + JWT)
         ↓
┌─────────────────┐
│  Django Server  │  ← 백엔드 서버
│  127.0.0.1:8000 │
└────────┬────────┘
         │
         │ 5. Router → ViewSet
         ↓
┌─────────────────┐
│  ViewSet        │  ← API 로직 처리 (PerformanceViewSet, ReviewViewSet 등)
└────────┬────────┘
         │
         │ 6. Serializer → Model
         ↓
┌─────────────────┐
│  Database       │  ← SQLite 데이터 저장소
└─────────────────┘
```

## 🚀 실행 방법

### 1. 백엔드 실행
```bash
cd back
# 가상환경 활성화 (Windows)
venv\Scripts\activate
# 서버 실행
python manage.py runserver
```

### 2. 프론트엔드 실행
```bash
cd front
# 의존성 설치 (최초 1회)
npm install
# 개발 서버 실행
npm run dev
```

### 3. 접속
- 프론트엔드: http://localhost:5173
- 백엔드 API: http://127.0.0.1:8000/api/

## Branch 규칙

### 1. `master` 브랜치
- **목적**: 최종 검증된 배포 버전 유지
- **특징**: 항상 안정적이고 배포 가능한 상태 유지

### 2. `develop` 브랜치
- **목적**: 개발 브랜치로 기능 개발 및 버그 수정
- **파생**: `master`에서 파생, 모든 `feature` 브랜치는 `develop`에 병합

### 3. `feature` 브랜치
- **목적**: 새로운 기능 개발
- **명명 규칙**: `feature/<app_name>` 또는 `feature/<feature-name>`
  - 예시: `feature/jwt-auth`, `feature/performance-list`
- **파생**: `develop` 브랜치에서 파생하여 개발 완료 후 `develop`에 병합

## Commit 규칙

### 1. 커밋 메시지 형식
```
<type>: <subject>

<body> (선택사항)
```

### 2. Type 종류
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드 업무, 패키지 관리 등

### 3. 예시
```
feat: JWT 인증 시스템 구현
fix: 공연 상세 페이지 API 호출 오류 수정
refactor: Vue 3 best practices에 따른 컴포넌트 분리
docs: README 파일 업데이트
```

## 주요 개선 사항 (리팩토링)

### 컴포넌트 분리 (f614088)
기존의 단일 컴포넌트를 Vue 3 Best Practices에 따라 다음과 같이 분리:

1. **BoxOffice 모듈**
   - `BoxOfficeCard.vue`: 개별 공연 카드 UI
   - `BoxOfficeCarousel.vue`: 캐러셀 컨테이너
   - `GenreTab.vue`: 장르 탭 네비게이션
   - `RankBadge.vue`: 순위 뱃지

2. **Performance 모듈**
   - `PerformanceCard.vue`: 공연 카드 UI
   - `PerformanceFilters.vue`: 필터 컨트롤
   - `PerformanceGrid.vue`: 그리드 레이아웃

3. **PerformanceDetail 모듈**
   - `HeaderSection.vue`: 헤더 정보
   - `MapModal.vue`: 지도 모달

**효과**: 코드 재사용성 향상, 유지보수 용이, 테스트 가능성 증가

## 느낀점 및 발전 방안

### 느낀점
Vue 3와 Django REST Framework를 활용하여 프론트엔드와 백엔드를 완전히 분리한 현대적인 웹 애플리케이션 개발 경험을 쌓았습니다. 특히 다음과 같은 학습 성과를 얻었습니다:

1. **아키텍처 이해**: SPA 아키텍처와 RESTful API 설계 원칙에 대한 깊은 이해
2. **상태 관리**: Pinia를 활용한 중앙 집중식 상태 관리의 중요성 체득
3. **컴포넌트 설계**: Vue 3 Composition API와 단일 책임 원칙을 적용한 컴포넌트 분리
4. **Composables 패턴**: Composables를 학습하여 적용. 로직 재사용성과 코드 구조화에 있어 Vue 3의 진정한 강점을 체감할 수 있었음
5. **인증 시스템**: JWT 기반 토큰 인증의 동작 원리와 보안 고려사항 학습
6. **API 통신**: Axios 인터셉터를 활용한 효율적인 HTTP 통신 관리

이전 프로젝트(09-pjt)에서 Django 템플릿과 AJAX를 사용했던 경험을 바탕으로, 이번에는 완전한 프론트엔드/백엔드 분리를 통해 더욱 확장 가능하고 유지보수가 용이한 아키텍처를 구현할 수 있었습니다. 특히 공식 문서와 Best Practices를 직접 탐구하며 Composables 패턴을 도입한 것은 교육 과정을 넘어선 자기주도 학습의 성과였습니다.

### 발전 방안
1. **테스트 코드 작성**: Vitest를 활용한 컴포넌트 및 API 테스트
2. **실시간 기능 추가**: WebSocket을 활용한 실시간 알림 및 채팅 기능
3. **사용자 경험 개선**:
   - 로딩 스켈레톤 UI
   - 에러 바운더리 및 사용자 친화적인 에러 메시지
   - 반응형 디자인 최적화
4. **추천 알고리즘**: 사용자 선호도 기반 공연 추천 시스템 개발.
