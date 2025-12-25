# 🎭 Final-PJT Frontend Documentation

## 📑 목차
1. [개요](#-개요)
2. [기술 스택](#-기술-스택)
3. [프로젝트 구조](#-프로젝트-구조)
4. [핵심 기능](#-핵심-기능)
5. [상태 관리](#-상태-관리-pinia)
6. [API 통신](#-api-통신)
7. [라우팅](#-라우팅)
8. [컴포넌트 아키텍처](#-컴포넌트-아키텍처)
9. [Composables 패턴](#-composables-패턴)
10. [스타일링](#-스타일링)
11. [환경 설정](#-환경-설정)
12. [개발 가이드](#-개발-가이드)
13. [빌드 및 배포](#-빌드-및-배포)

---

## 🎯 개요

본 프로젝트는 **Vue 3 Composition API**를 기반으로 한 공연 정보 및 커뮤니티 플랫폼의 프론트엔드 애플리케이션입니다. 사용자 맞춤형 공연 추천, AI 기반 검색, 박스오피스 랭킹, 커뮤니티 리뷰 시스템 등을 제공합니다.

### 주요 특징
- ✅ **Vue 3 Composition API** 기반의 현대적인 프론트엔드 아키텍처
- ✅ **Pinia**를 활용한 체계적인 상태 관리
- ✅ **JWT 자동 갱신** 기능이 포함된 Axios 인터셉터
- ✅ **Composables 패턴**을 통한 로직 재사용
- ✅ **Tailwind CSS**를 활용한 유틸리티 우선 스타일링
- ✅ **다크모드** 지원
- ✅ **Tinder 스타일 온보딩** UX
- ✅ **반응형 디자인** (모바일/태블릿/데스크톱)

---

## 🛠 기술 스택

### Core Framework
| 기술 | 버전 | 용도 |
|------|------|------|
| **Vue** | ^3.5.25 | UI 프레임워크 |
| **Vite** | ^7.2.4 | 빌드 도구 및 개발 서버 |
| **Node.js** | ^20.19.0 또는 >=22.12.0 | 런타임 환경 |

### State Management & Routing
| 기술 | 버전 | 용도 |
|------|------|------|
| **Pinia** | ^3.0.4 | 상태 관리 라이브러리 |
| **Vue Router** | ^4.6.3 | 클라이언트 사이드 라우팅 |

### HTTP & API
| 기술 | 버전 | 용도 |
|------|------|------|
| **Axios** | ^1.13.2 | HTTP 클라이언트 (JWT 인터셉터 포함) |

### Styling
| 기술 | 버전 | 용도 |
|------|------|------|
| **Tailwind CSS** | ^3.4.0 | 유틸리티 우선 CSS 프레임워크 |
| **PostCSS** | ^8.5.6 | CSS 후처리 |
| **Autoprefixer** | ^10.4.22 | CSS 벤더 프리픽스 자동 추가 |

### Development Tools
| 기술 | 버전 | 용도 |
|------|------|------|
| **@vitejs/plugin-vue** | ^6.0.2 | Vite Vue 플러그인 |
| **vite-plugin-vue-devtools** | ^8.0.5 | Vue DevTools 통합 |

---

## 📂 프로젝트 구조

```
front/
├── public/                          # 정적 파일
│   ├── favicon.ico                  # 파비콘
│   └── no_poster.png               # 포스터 없을 때 대체 이미지
│
├── src/
│   ├── api/                         # API 통신 모듈
│   │   ├── axios.js                # Axios 인스턴스 및 인터셉터 설정
│   │   ├── auth.js                 # 인증 API (로그인, 회원가입, 토큰 갱신)
│   │   ├── performances.js         # 공연 API (목록, 상세, 검색, 좋아요)
│   │   ├── community.js            # 커뮤니티 API (게시글, 댓글)
│   │   ├── users.js                # 사용자 API (프로필, 계정 관리)
│   │   ├── onboarding.js           # 온보딩 API (Tinder 스타일)
│   │   ├── watched.js              # 관람함 API
│   │   ├── wishlist.js             # 찜 API
│   │   ├── youtube.js              # YouTube API
│   │   └── recommendations.js      # 추천 API
│   │
│   ├── components/                  # Vue 컴포넌트
│   │   ├── AISearch/               # AI 검색 관련
│   │   │   └── AISearchCard.vue
│   │   │
│   │   ├── BoxOffice/              # 박스오피스/랭킹 (11개 컴포넌트)
│   │   │   ├── BoxOfficeCard.vue           # 박스오피스 카드
│   │   │   ├── BoxOfficeCarousel.vue       # 박스오피스 캐러셀
│   │   │   ├── HighlightCarousel.vue       # 하이라이트 캐러셀
│   │   │   ├── AllRankingSection.vue       # 전체 랭킹 섹션
│   │   │   ├── AllRankingDetail.vue        # 전체 랭킹 상세
│   │   │   ├── RankingCard.vue             # 랭킹 카드
│   │   │   ├── RankingListItem.vue         # 랭킹 목록 아이템
│   │   │   ├── GenreRankingSection.vue     # 장르 랭킹 섹션
│   │   │   ├── GenreRankingDetail.vue      # 장르 랭킹 상세
│   │   │   ├── GenreTab.vue                # 장르 탭
│   │   │   └── RankBadge.vue               # 순위 뱃지
│   │   │
│   │   ├── Common/                 # 공통 컴포넌트
│   │   │   ├── BasePerformanceCard.vue     # 공연 카드 베이스
│   │   │   ├── DarkModeToggle.vue          # 다크모드 토글
│   │   │   ├── FloatingActionButtons.vue   # 플로팅 액션 버튼
│   │   │   └── ScrollToTop.vue             # 맨 위로 스크롤
│   │   │
│   │   ├── Community/              # 커뮤니티 (12개 컴포넌트)
│   │   │   ├── ArticleCard.vue             # 게시글 카드
│   │   │   ├── ArticleCreateModal.vue      # 게시글 작성 모달
│   │   │   ├── ArticleFormFields.vue       # 게시글 폼 필드
│   │   │   ├── ArticleHeader.vue           # 게시글 헤더
│   │   │   ├── ArticleList.vue             # 게시글 목록
│   │   │   ├── BestReviewSection.vue       # 베스트 리뷰 섹션
│   │   │   ├── CategoryDisplay.vue         # 카테고리 표시
│   │   │   ├── CommentForm.vue             # 댓글 폼
│   │   │   ├── CommentList.vue             # 댓글 목록
│   │   │   ├── FilterButton.vue            # 필터 버튼
│   │   │   ├── PerformanceSelectCard.vue   # 공연 선택 카드
│   │   │   └── StarRating.vue              # 별점 평가
│   │   │
│   │   ├── Performance/            # 공연 목록 관련
│   │   │   └── (목록 컴포넌트)
│   │   │
│   │   ├── PerformanceDetail/      # 공연 상세 (6개 컴포넌트)
│   │   │   ├── HeaderSection.vue           # 헤더 정보 섹션
│   │   │   ├── MapModal.vue                # Kakao 지도 모달
│   │   │   ├── RatingChart.vue             # 평점 차트
│   │   │   ├── ReviewForm.vue              # 리뷰 작성 폼
│   │   │   ├── ReviewList.vue              # 리뷰 목록
│   │   │   └── YouTubeVideoSection.vue     # YouTube 영상 섹션
│   │   │
│   │   ├── Recommendation/         # 추천 관련
│   │   │   ├── RecommendationCard.vue
│   │   │   └── RecommendationSection.vue
│   │   │
│   │   ├── User/                   # 마이페이지/사용자 (9개 컴포넌트)
│   │   │   ├── ProfileSection.vue          # 프로필 섹션
│   │   │   ├── BasicInfoForm.vue           # 기본 정보 폼
│   │   │   ├── AccountInfoForm.vue         # 계정 정보 폼
│   │   │   ├── PasswordChangeForm.vue      # 비밀번호 변경 폼
│   │   │   ├── PasswordVerifyModal.vue     # 비밀번호 확인 모달
│   │   │   ├── PreferenceForm.vue          # 선호도 폼
│   │   │   ├── WatchedSection.vue          # 관람함 섹션
│   │   │   ├── WishlistSection.vue         # 찜 섹션
│   │   │   ├── ArticlesCommentsTab.vue     # 게시글/댓글 탭
│   │   │   └── DeleteAccountModal.vue      # 계정 삭제 모달
│   │   │
│   │   ├── YouTube/                # YouTube 관련
│   │   │   ├── YouTubeModal.vue
│   │   │   └── YouTubePlaylistSection.vue
│   │   │
│   │   └── WelcomeOverlay.vue      # 웰컴 오버레이
│   │
│   ├── composables/                 # Composition API 재사용 로직
│   │   ├── common/
│   │   │   └── useCategoryLabels.js        # 카테고리 라벨 관리
│   │   ├── community/
│   │   │   ├── useArticleDetail.js         # 게시글 상세 로직
│   │   │   └── useArticleForm.js           # 게시글 폼 로직
│   │   ├── useAllRanking.js                # 전체 랭킹 로직
│   │   ├── useBoxOffice.js                 # 박스오피스 로직
│   │   ├── useEditAccount.js               # 계정 수정 로직
│   │   ├── useKakaoMap.js                  # Kakao 지도 로직
│   │   ├── useMyPage.js                    # 마이페이지 로직
│   │   ├── usePerformanceDetail.js         # 공연 상세 로직
│   │   ├── usePerformanceList.js           # 공연 목록 로직
│   │   ├── useUserTracking.js              # 사용자 추적 로직
│   │   └── index.js                        # Composables 내보내기
│   │
│   ├── stores/                      # Pinia 상태 관리
│   │   ├── authStore.js            # 인증 상태 (토큰, 로그인/로그아웃)
│   │   ├── themeStore.js           # 테마/다크모드
│   │   ├── performanceStore.js     # 공연 데이터 (목록, 상세, 장르, 랭킹)
│   │   ├── communityStore.js       # 커뮤니티 (게시글, 댓글, 필터)
│   │   ├── onboardingStore.js      # 온보딩 상태 (Tinder 카드)
│   │   ├── aiSearchStore.js        # AI 검색 결과 (localStorage 지속)
│   │   ├── watchedStore.js         # 관람함 목록
│   │   ├── wishlistStore.js        # 찜 목록
│   │   ├── welcomeStore.js         # 웰컴 오버레이 상태
│   │   ├── userStore.js            # 사용자 정보
│   │   ├── recommendationStore.js  # 추천 데이터
│   │   └── counter.js              # (예제용)
│   │
│   ├── views/                       # 페이지 컴포넌트
│   │   ├── Auth/                   # 인증 관련 페이지
│   │   │   ├── LoginView.vue               # 로그인
│   │   │   ├── RegisterView.vue            # 회원가입
│   │   │   └── OnboardingView.vue          # 온보딩 (Tinder 스타일)
│   │   │
│   │   ├── Community/              # 커뮤니티 페이지
│   │   │   ├── CommunityView.vue           # 커뮤니티 메인
│   │   │   ├── CommunityBestView.vue       # 베스트 리뷰
│   │   │   ├── CommunityWriteView.vue      # 게시글 작성
│   │   │   ├── ArticleDetailView.vue       # 게시글 상세
│   │   │   └── EditArticleView.vue         # 게시글 수정
│   │   │
│   │   ├── Performance/            # 공연 페이지
│   │   │   ├── PerformanceListView.vue     # 공연 목록
│   │   │   └── PerformanceDetailView.vue   # 공연 상세
│   │   │
│   │   ├── Ranking/                # 랭킹 페이지
│   │   │   ├── RankingsView.vue            # 랭킹 메인
│   │   │   ├── RankingAllView.vue          # 전체 랭킹
│   │   │   └── RankingGenreView.vue        # 장르별 랭킹
│   │   │
│   │   ├── User/                   # 사용자 페이지
│   │   │   ├── MyPageView.vue              # 마이페이지
│   │   │   └── EditAccountView.vue         # 계정 수정
│   │   │
│   │   ├── Admin/                  # 어드민 페이지
│   │   │   └── AdminDashboardView.vue      # 어드민 대시보드
│   │   │
│   │   ├── LandingView.vue         # 홈/랜딩 페이지
│   │   ├── RecommandsView.vue      # 추천 페이지
│   │   └── TestAPIView.vue         # API 테스트 페이지
│   │
│   ├── router/
│   │   └── index.js                # Vue Router 설정 및 네비게이션 가드
│   │
│   ├── assets/
│   │   ├── main.css                # 글로벌 CSS (Tailwind 지시어 포함)
│   │   ├── styles/
│   │   │   └── dark-mode.css       # 다크모드 스타일
│   │   └── images/                 # 로고 및 이미지
│   │
│   ├── App.vue                     # 루트 컴포넌트
│   └── main.js                     # 애플리케이션 진입점
│
├── .vscode/
│   └── extensions.json             # VSCode 권장 확장 (Vue Volar)
│
├── index.html                      # HTML 진입점
├── vite.config.js                  # Vite 설정
├── jsconfig.json                   # JavaScript 설정 (@ alias)
├── tailwind.config.js              # Tailwind CSS 설정
├── postcss.config.js               # PostCSS 설정
├── package.json                    # 프로젝트 의존성
├── package-lock.json
├── .env_                          # 환경 변수 템플릿
├── .gitignore
└── FRONTEND_REFACTORING_TODO.md
```

---

## ✨ 핵심 기능

### 1. 사용자 인증 및 온보딩
- **JWT 기반 인증**: Access Token & Refresh Token 자동 관리
- **Tinder 스타일 온보딩**: 공연 카드 스와이프로 선호도 수집
- **자동 토큰 갱신**: Axios 인터셉터를 통한 무중단 토큰 갱신
- **온보딩 강제**: 로그인 후 온보딩 미완료시 자동 리다이렉트

**관련 파일:**
- [src/views/Auth/LoginView.vue](src/views/Auth/LoginView.vue)
- [src/views/Auth/RegisterView.vue](src/views/Auth/RegisterView.vue)
- [src/views/Auth/OnboardingView.vue](src/views/Auth/OnboardingView.vue)
- [src/stores/authStore.js](src/stores/authStore.js)
- [src/stores/onboardingStore.js](src/stores/onboardingStore.js)
- [src/api/axios.js](src/api/axios.js) (인터셉터)

### 2. AI 기반 공연 검색
- **의미 기반 검색**: 자연어 쿼리로 공연 검색
- **AI 코멘트**: 검색 결과에 대한 AI 설명 제공
- **localStorage 지속성**: 마지막 검색 결과 캐싱

**관련 파일:**
- [src/stores/aiSearchStore.js](src/stores/aiSearchStore.js)
- [src/api/performances.js](src/api/performances.js) (`aiSearch` 함수)
- [src/components/AISearch/AISearchCard.vue](src/components/AISearch/AISearchCard.vue)

### 3. 박스오피스 랭킹 시스템
- **장르별 랭킹**: 뮤지컬, 연극, 클래식 등 장르별 순위
- **전체 랭킹**: 모든 장르 통합 순위
- **하이라이트 캐러셀**: 상위 랭크 공연 자동 순환 표시

**관련 파일:**
- [src/components/BoxOffice/](src/components/BoxOffice/) (11개 컴포넌트)
- [src/views/Ranking/RankingsView.vue](src/views/Ranking/RankingsView.vue)
- [src/composables/useBoxOffice.js](src/composables/useBoxOffice.js)
- [src/composables/useAllRanking.js](src/composables/useAllRanking.js)

### 4. 공연 정보 시스템
- **공연 목록**: 장르, 지역, 상태별 필터링
- **공연 상세**: 포스터, 기간, 장소, 가격, 시놀시스, 평점 차트
- **Kakao 지도 연동**: 공연장 위치 시각화
- **YouTube 연동**: 관련 영상 자동 추천
- **찜하기/관람함**: 공연 북마크 및 관람 기록

**관련 파일:**
- [src/views/Performance/PerformanceListView.vue](src/views/Performance/PerformanceListView.vue)
- [src/views/Performance/PerformanceDetailView.vue](src/views/Performance/PerformanceDetailView.vue)
- [src/composables/usePerformanceList.js](src/composables/usePerformanceList.js)
- [src/composables/usePerformanceDetail.js](src/composables/usePerformanceDetail.js)
- [src/composables/useKakaoMap.js](src/composables/useKakaoMap.js)

### 5. 커뮤니티 시스템
- **리뷰 CRUD**: 공연에 대한 리뷰 작성/수정/삭제
- **별점 평가**: 5점 만점 별점 시스템
- **댓글 기능**: 리뷰에 대한 댓글 작성
- **좋아요**: 리뷰 좋아요/취소 토글
- **베스트 리뷰**: 높은 평가를 받은 리뷰 하이라이트
- **카테고리 필터**: 장르, 정렬 기준별 필터링

**관련 파일:**
- [src/views/Community/](src/views/Community/) (5개 페이지)
- [src/components/Community/](src/components/Community/) (12개 컴포넌트)
- [src/stores/communityStore.js](src/stores/communityStore.js)
- [src/composables/community/](src/composables/community/)

### 6. 마이페이지
- **프로필 관리**: 기본 정보, 선호 장르 설정
- **계정 관리**: 비밀번호 변경, 계정 삭제
- **관람함**: 봤던 공연 목록 및 관리
- **찜 목록**: 관심 공연 북마크
- **내 활동**: 작성한 게시글 및 댓글 목록

**관련 파일:**
- [src/views/User/MyPageView.vue](src/views/User/MyPageView.vue)
- [src/views/User/EditAccountView.vue](src/views/User/EditAccountView.vue)
- [src/components/User/](src/components/User/) (9개 컴포넌트)
- [src/composables/useMyPage.js](src/composables/useMyPage.js)
- [src/composables/useEditAccount.js](src/composables/useEditAccount.js)

### 7. 추천 시스템
- **개인화 추천**: 온보딩 및 관람 이력 기반 추천
- **협업 필터링**: 유사 사용자 선호도 기반 추천

**관련 파일:**
- [src/views/RecommandsView.vue](src/views/RecommandsView.vue)
- [src/stores/recommendationStore.js](src/stores/recommendationStore.js)
- [src/components/Recommendation/](src/components/Recommendation/)

### 8. 다크모드
- **자동 지속성**: localStorage에 테마 설정 저장
- **전역 토글**: 모든 페이지에서 일관된 다크모드 적용

**관련 파일:**
- [src/stores/themeStore.js](src/stores/themeStore.js)
- [src/components/Common/DarkModeToggle.vue](src/components/Common/DarkModeToggle.vue)
- [src/assets/styles/dark-mode.css](src/assets/styles/dark-mode.css)

---

## 🗄 상태 관리 (Pinia)

### 스토어 구조

프로젝트는 **Pinia**를 사용하여 모듈화된 상태 관리를 구현합니다. 각 스토어는 **Composition API 패턴**으로 작성되었습니다.

```javascript
// Composition API 패턴 예시
export const useAuthStore = defineStore('auth', () => {
  // State (ref)
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))

  // Computed (computed)
  const isAuthenticated = computed(() => !!accessToken.value)

  // Actions (함수)
  const login = async (credentials) => {
    // 로그인 로직
  }

  return { user, accessToken, isAuthenticated, login }
})
```

### 스토어 목록

| 스토어 | 파일 | 용도 | 주요 상태/액션 |
|-------|------|------|-------------|
| **authStore** | [authStore.js](src/stores/authStore.js) | 인증 관리 | `user`, `accessToken`, `refreshToken`, `login()`, `logout()`, `isAuthenticated`, `isAdmin` |
| **themeStore** | [themeStore.js](src/stores/themeStore.js) | 테마/다크모드 | `theme`, `isDarkMode`, `toggleTheme()`, localStorage 동기화 |
| **performanceStore** | [performanceStore.js](src/stores/performanceStore.js) | 공연 데이터 | `performances`, `currentPerformance`, `genres`, `boxOfficeRankings`, `fetchPerformances()` |
| **communityStore** | [communityStore.js](src/stores/communityStore.js) | 커뮤니티 | `articles`, `currentArticle`, `comments`, `filters`, `bestReviews`, `likeArticle()` |
| **onboardingStore** | [onboardingStore.js](src/stores/onboardingStore.js) | 온보딩 프로세스 | `candidates`, `currentIndex`, `likes`, `dislikes`, `swipe()`, `saveSignals()` |
| **aiSearchStore** | [aiSearchStore.js](src/stores/aiSearchStore.js) | AI 검색 | `searchResults`, `aiComment`, `lastQuery`, localStorage 지속성 |
| **watchedStore** | [watchedStore.js](src/stores/watchedStore.js) | 관람함 | `items`, `isWatched()`, `addWatched()`, 낙관적 업데이트 |
| **wishlistStore** | [wishlistStore.js](src/stores/wishlistStore.js) | 찜 목록 | `items`, `removeFromWishlist()`, 낙관적 업데이트 |
| **welcomeStore** | [welcomeStore.js](src/stores/welcomeStore.js) | 웰컴 오버레이 | `showWelcomeOverlay`, `welcomeData` |
| **userStore** | [userStore.js](src/stores/userStore.js) | 사용자 정보 | 사용자 프로필 및 설정 |
| **recommendationStore** | [recommendationStore.js](src/stores/recommendationStore.js) | 추천 데이터 | 추천 공연 목록 |

### 주요 특징

#### 1. localStorage 동기화
```javascript
// themeStore.js 예시
const theme = ref(localStorage.getItem('theme') || 'light')

watch(theme, (newTheme) => {
  localStorage.setItem('theme', newTheme)
  document.documentElement.classList.toggle('dark', newTheme === 'dark')
})
```

#### 2. 낙관적 업데이트 (Optimistic Updates)
```javascript
// watchedStore.js 예시
const addWatched = async (performanceId) => {
  // 1. UI 즉시 업데이트
  items.value.push(performanceId)

  try {
    // 2. 서버에 요청
    await addWatchedAPI(performanceId)
  } catch (error) {
    // 3. 실패 시 롤백
    items.value = items.value.filter(id => id !== performanceId)
    throw error
  }
}
```

#### 3. 양방향 동기화
온보딩에서 선호도 업데이트 시 여러 스토어를 동시에 반영하여 일관성 유지

---

## 🌐 API 통신

### Axios 설정

**파일:** [src/api/axios.js](src/api/axios.js)

#### 기본 설정
```javascript
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  withCredentials: true,  // CORS 쿠키 포함
})
```

#### 요청 인터셉터
```javascript
// Access Token 자동 첨부
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  }
)
```

#### 응답 인터셉터 (자동 토큰 갱신)
```javascript
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh Token으로 Access Token 갱신
      const refreshToken = localStorage.getItem('refresh_token')
      const response = await axios.post('/accounts/token/refresh/', { refresh: refreshToken })

      // 새 토큰 저장
      localStorage.setItem('access_token', response.data.access)

      // 원래 요청 재시도
      error.config.headers.Authorization = `Bearer ${response.data.access}`
      return apiClient.request(error.config)
    }
    return Promise.reject(error)
  }
)
```

### API 모듈

#### 1. 인증 API ([auth.js](src/api/auth.js))
| 함수 | 메서드 | 엔드포인트 | 용도 |
|-----|--------|----------|------|
| `register(data)` | POST | `/accounts/register/` | 회원가입 |
| `login(credentials)` | POST | `/accounts/token/` | 로그인 (토큰 발급) |
| `refreshToken(refresh)` | POST | `/accounts/token/refresh/` | Access Token 갱신 |
| `logout()` | - | - | 클라이언트 측 토큰 삭제 |
| `getCurrentUser()` | GET | `/accounts/users/me/` | 현재 사용자 정보 |
| `updateProfile(data)` | PATCH | `/users/update_profile/` | 프로필 업데이트 |
| `deleteAccount(password)` | DELETE | `/users/delete_account/` | 계정 삭제 |
| `verifyPassword(password)` | POST | `/accounts/users/verify_password/` | 비밀번호 확인 |

#### 2. 공연 API ([performances.js](src/api/performances.js))
| 함수 | 메서드 | 엔드포인트 | 용도 |
|-----|--------|----------|------|
| `getPerformances(params)` | GET | `/performances/` | 공연 목록 (필터링 지원) |
| `getPerformance(id)` | GET | `/performances/{id}/` | 공연 상세 |
| `getGenres()` | GET | `/performances/genres/` | 장르 목록 |
| `getBoxOffice(params)` | GET | `/boxoffice/` | 박스오피스 목록 |
| `getLatestBoxOfficeByGenre(genreCode)` | GET | `/boxoffice/latest_by_genre/` | 장르별 최신 박스오피스 |
| `getBoxOfficeByGenre(genre)` | GET | `/performances/boxoffice-genre/` | 장르별 박스오피스 |
| `getBoxOfficeAll()` | GET | `/performances/boxoffice-all/` | 전체 박스오피스 |
| `getBoxOfficeHighlight()` | GET | `/performances/boxoffice-highlight/` | 하이라이트 박스오피스 |
| `toggleLike(performanceId)` | POST | `/performances/{id}/like/` | 공연 좋아요 토글 |
| `aiSearch(query)` | POST | `/performances/ai-search/` | AI 의미 기반 검색 |

#### 3. 커뮤니티 API ([community.js](src/api/community.js))
| 함수 | 메서드 | 엔드포인트 | 용도 |
|-----|--------|----------|------|
| `getArticles(params)` | GET | `/community/articles/` | 게시글 목록 |
| `getArticle(id)` | GET | `/community/articles/{id}/` | 게시글 상세 |
| `createArticle(data)` | POST | `/community/articles/` | 게시글 작성 |
| `updateArticle(id, data)` | PUT | `/community/articles/{id}/` | 게시글 수정 |
| `deleteArticle(id)` | DELETE | `/community/articles/{id}/` | 게시글 삭제 |
| `likeArticle(id)` | POST | `/community/articles/{id}/like/` | 게시글 좋아요 |
| `getBestReviews(limit)` | GET | `/community/articles/best-reviews/` | 베스트 리뷰 목록 |
| `getComments(articleId)` | GET | `/community/comments/` | 댓글 목록 |
| `createComment(data)` | POST | `/community/comments/` | 댓글 작성 |
| `updateComment(id, data)` | PATCH | `/community/comments/{id}/` | 댓글 수정 |
| `deleteComment(id)` | DELETE | `/community/comments/{id}/` | 댓글 삭제 |

#### 4. 온보딩 API ([onboarding.js](src/api/onboarding.js))
| 함수 | 메서드 | 엔드포인트 | 용도 |
|-----|--------|----------|------|
| `getCandidates(strategy, excludeIds)` | GET | `/accounts/onboarding/candidates/` | 온보딩 후보 공연 |
| `saveSignals(signals)` | POST | `/accounts/onboarding/signals/` | 선호도 신호 저장 |
| `completeOnboarding()` | POST | `/accounts/onboarding/complete/` | 온보딩 완료 |

#### 5. 관람함/찜 API
- **watched.js**: `fetchWatched()`, `addWatched()`, `removeWatched()`
- **wishlist.js**: `fetchWishlist()`, `removeWishlist()`, `toggleWishlist()`

#### 6. 사용자 API ([users.js](src/api/users.js))
| 함수 | 메서드 | 엔드포인트 | 용도 |
|-----|--------|----------|------|
| `getUsers()` | GET | `/accounts/users/` | 사용자 목록 |
| `getUser(id)` | GET | `/accounts/users/{id}/` | 사용자 상세 |
| `getCurrentUser()` | GET | `/accounts/users/me/` | 현재 사용자 |

---

## 🚏 라우팅

**파일:** [src/router/index.js](src/router/index.js)

### 라우팅 기능

#### 1. 메타 라우트
```javascript
{
  path: '/mypage',
  component: MyPageView,
  meta: { requiresAuth: true }  // 로그인 필요
}

{
  path: '/admin',
  component: AdminDashboardView,
  meta: { requiresAuth: true, requiresAdmin: true }  // 관리자 권한 필요
}
```

#### 2. 전역 네비게이션 가드
```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 인증 필요한 페이지 체크
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  // 관리자 권한 체크
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next('/')
  }

  // 온보딩 강제
  if (authStore.isAuthenticated && !authStore.user.onboarding_completed) {
    if (to.path !== '/onboarding') {
      return next('/onboarding')
    }
  }

  next()
})
```

#### 3. 스크롤 동작
```javascript
scrollBehavior(to, from, savedPosition) {
  if (savedPosition) {
    return savedPosition  // 뒤로가기: 이전 위치 복원
  } else if (to.hash) {
    return { el: to.hash, behavior: 'smooth' }  // 앵커 링크
  } else {
    return { top: 0 }  // 최상단으로 스크롤
  }
}
```

#### 4. 지연 로딩 (Code Splitting)
```javascript
{
  path: '/performances/:id',
  component: () => import('@/views/Performance/PerformanceDetailView.vue')
}
```

### 라우트 목록

| 경로 | 컴포넌트 | 설명 | 인증 필요 | 관리자 필요 |
|------|---------|------|----------|-----------|
| `/` | [LandingView.vue](src/views/LandingView.vue) | 홈/랜딩 페이지 | ❌ | ❌ |
| `/performances` | [PerformanceListView.vue](src/views/Performance/PerformanceListView.vue) | 공연 목록 | ❌ | ❌ |
| `/performances/:id` | [PerformanceDetailView.vue](src/views/Performance/PerformanceDetailView.vue) | 공연 상세 | ❌ | ❌ |
| `/community` | [CommunityView.vue](src/views/Community/CommunityView.vue) | 커뮤니티 메인 | ❌ | ❌ |
| `/community/best` | [CommunityBestView.vue](src/views/Community/CommunityBestView.vue) | 베스트 리뷰 | ❌ | ❌ |
| `/community/write` | [CommunityWriteView.vue](src/views/Community/CommunityWriteView.vue) | 게시글 작성 | ✅ | ❌ |
| `/community/:id` | [ArticleDetailView.vue](src/views/Community/ArticleDetailView.vue) | 게시글 상세 | ❌ | ❌ |
| `/community/:id/edit` | [EditArticleView.vue](src/views/Community/EditArticleView.vue) | 게시글 수정 | ✅ | ❌ |
| `/login` | [LoginView.vue](src/views/Auth/LoginView.vue) | 로그인 | ❌ | ❌ |
| `/register` | [RegisterView.vue](src/views/Auth/RegisterView.vue) | 회원가입 | ❌ | ❌ |
| `/onboarding` | [OnboardingView.vue](src/views/Auth/OnboardingView.vue) | 온보딩 | ✅ | ❌ |
| `/mypage` | [MyPageView.vue](src/views/User/MyPageView.vue) | 마이페이지 | ✅ | ❌ |
| `/edit-account` | [EditAccountView.vue](src/views/User/EditAccountView.vue) | 계정 수정 | ✅ | ❌ |
| `/admin` | [AdminDashboardView.vue](src/views/Admin/AdminDashboardView.vue) | 어드민 대시보드 | ✅ | ✅ |
| `/rankings` | [RankingsView.vue](src/views/Ranking/RankingsView.vue) | 랭킹 메인 | ❌ | ❌ |
| `/rankings/all` | [RankingAllView.vue](src/views/Ranking/RankingAllView.vue) | 전체 랭킹 | ❌ | ❌ |
| `/rankings/genre` | [RankingGenreView.vue](src/views/Ranking/RankingGenreView.vue) | 장르별 랭킹 | ❌ | ❌ |
| `/recommands` | [RecommandsView.vue](src/views/RecommandsView.vue) | 추천 페이지 | ❌ | ❌ |
| `/test-api` | [TestAPIView.vue](src/views/TestAPIView.vue) | API 테스트 | ❌ | ❌ |

---

## 🧩 컴포넌트 아키텍처

### 설계 원칙

1. **단일 책임 원칙 (SRP)**: 각 컴포넌트는 하나의 기능만 담당
2. **Props Down, Events Up**: 부모-자식 간 명확한 데이터 흐름
3. **Composition API**: `<script setup>` 문법으로 간결한 코드
4. **재사용성**: 공통 로직은 Composables로 추출

### 컴포넌트 계층 구조

```
App.vue (루트)
│
├── LandingView.vue (홈)
│   ├── BoxOfficeCarousel.vue
│   │   ├── BoxOfficeCard.vue
│   │   └── GenreTab.vue
│   ├── HighlightCarousel.vue
│   └── RecommendationSection.vue
│       └── RecommendationCard.vue
│
├── PerformanceListView.vue (공연 목록)
│   └── BasePerformanceCard.vue (x N)
│
├── PerformanceDetailView.vue (공연 상세)
│   ├── HeaderSection.vue
│   ├── RatingChart.vue
│   ├── YouTubeVideoSection.vue
│   ├── MapModal.vue
│   ├── ReviewForm.vue
│   └── ReviewList.vue
│
├── CommunityView.vue (커뮤니티)
│   ├── FilterButton.vue (x N)
│   ├── BestReviewSection.vue
│   └── ArticleList.vue
│       └── ArticleCard.vue (x N)
│
├── MyPageView.vue (마이페이지)
│   ├── ProfileSection.vue
│   ├── WatchedSection.vue
│   ├── WishlistSection.vue
│   └── ArticlesCommentsTab.vue
│
└── Common Components
    ├── DarkModeToggle.vue
    ├── FloatingActionButtons.vue
    └── ScrollToTop.vue
```

### Props/Events 패턴 예시

```vue
<!-- 부모 컴포넌트 -->
<template>
  <BoxOfficeCard
    :performance="performance"
    :rank="index + 1"
    @click="handleCardClick"
  />
</template>

<script setup>
const emit = defineEmits(['click'])

const handleCardClick = (performanceId) => {
  emit('click', performanceId)
}
</script>
```

```vue
<!-- 자식 컴포넌트 (BoxOfficeCard.vue) -->
<script setup>
const props = defineProps({
  performance: {
    type: Object,
    required: true
  },
  rank: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['click'])
</script>
```

---

## 🔄 Composables 패턴

### 개념

**Composables**는 Vue 3 Composition API의 재사용 가능한 로직 단위입니다. 컴포넌트 간 공통 로직을 추출하여 중복을 줄이고 코드 구조화를 개선합니다.

### 주요 Composables

#### 1. usePerformanceDetail ([usePerformanceDetail.js](src/composables/usePerformanceDetail.js))

**용도:** 공연 상세 페이지 로직 관리

```javascript
export function usePerformanceDetail(performanceId) {
  const performance = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchPerformance = async () => {
    loading.value = true
    try {
      const response = await getPerformance(performanceId)
      performance.value = response.data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchPerformance()
  })

  return {
    performance,
    loading,
    error,
    fetchPerformance
  }
}
```

**사용 예시:**
```vue
<script setup>
import { usePerformanceDetail } from '@/composables/usePerformanceDetail'

const route = useRoute()
const { performance, loading, error } = usePerformanceDetail(route.params.id)
</script>
```

#### 2. useKakaoMap ([useKakaoMap.js](src/composables/useKakaoMap.js))

**용도:** Kakao Map API 통합

```javascript
export function useKakaoMap(lat, lng, placeName) {
  const mapContainer = ref(null)

  const initMap = () => {
    const options = {
      center: new kakao.maps.LatLng(lat, lng),
      level: 3
    }
    const map = new kakao.maps.Map(mapContainer.value, options)

    // 마커 생성
    const marker = new kakao.maps.Marker({
      position: new kakao.maps.LatLng(lat, lng)
    })
    marker.setMap(map)
  }

  onMounted(() => {
    initMap()
  })

  return { mapContainer }
}
```

#### 3. useArticleForm ([useArticleForm.js](src/composables/community/useArticleForm.js))

**용도:** 게시글 작성/수정 폼 로직

```javascript
export function useArticleForm(initialData = null) {
  const form = reactive({
    title: initialData?.title || '',
    content: initialData?.content || '',
    category: initialData?.category || '',
    rating: initialData?.rating || 0
  })

  const validate = () => {
    if (!form.title) return '제목을 입력하세요'
    if (!form.content) return '내용을 입력하세요'
    return null
  }

  const submit = async () => {
    const error = validate()
    if (error) throw new Error(error)

    if (initialData) {
      await updateArticle(initialData.id, form)
    } else {
      await createArticle(form)
    }
  }

  return { form, submit }
}
```

#### 4. useCategoryLabels ([useCategoryLabels.js](src/composables/common/useCategoryLabels.js))

**용도:** 카테고리 코드를 한글 라벨로 변환

```javascript
export function useCategoryLabels() {
  const categoryMap = {
    'AAAA': '연극',
    'BBBB': '뮤지컬',
    'CCCC': '클래식',
    // ...
  }

  const getCategoryLabel = (code) => categoryMap[code] || code

  return { getCategoryLabel, categoryMap }
}
```

### Composables 목록

| Composable | 파일 | 용도 |
|-----------|------|------|
| **usePerformanceList** | [usePerformanceList.js](src/composables/usePerformanceList.js) | 공연 목록 필터링 및 페이지네이션 |
| **usePerformanceDetail** | [usePerformanceDetail.js](src/composables/usePerformanceDetail.js) | 공연 상세 정보 및 리뷰 관리 |
| **useBoxOffice** | [useBoxOffice.js](src/composables/useBoxOffice.js) | 박스오피스 데이터 및 장르 탭 |
| **useAllRanking** | [useAllRanking.js](src/composables/useAllRanking.js) | 전체 랭킹 로직 |
| **useKakaoMap** | [useKakaoMap.js](src/composables/useKakaoMap.js) | Kakao Map API 통합 |
| **useMyPage** | [useMyPage.js](src/composables/useMyPage.js) | 마이페이지 데이터 관리 |
| **useEditAccount** | [useEditAccount.js](src/composables/useEditAccount.js) | 계정 수정 로직 |
| **useUserTracking** | [useUserTracking.js](src/composables/useUserTracking.js) | 사용자 행동 추적 |
| **useArticleDetail** | [community/useArticleDetail.js](src/composables/community/useArticleDetail.js) | 게시글 상세 및 댓글 |
| **useArticleForm** | [community/useArticleForm.js](src/composables/community/useArticleForm.js) | 게시글 폼 검증 및 제출 |
| **useCategoryLabels** | [common/useCategoryLabels.js](src/composables/common/useCategoryLabels.js) | 카테고리 라벨 변환 |

---

## 🎨 스타일링

### Tailwind CSS

**설정 파일:** [tailwind.config.js](tailwind.config.js)

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**사용 예시:**
```vue
<template>
  <div class="container mx-auto px-4">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
      제목
    </h1>
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
      버튼
    </button>
  </div>
</template>
```

### 글로벌 CSS

**파일:** [src/assets/main.css](src/assets/main.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* CSS 변수 정의 */
:root {
  --primary-color: #3b82f6;
  --secondary-color: #8b5cf6;
  --background-color: #ffffff;
  --text-color: #1f2937;
}

/* 커스텀 유틸리티 클래스 */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

/* 글로벌 컴포넌트 스타일 */
.card {
  @apply bg-white rounded-lg shadow-md p-6;
}

.btn-primary {
  @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}
```

### 다크모드

**파일:** [src/assets/styles/dark-mode.css](src/assets/styles/dark-mode.css)

```css
:root.dark {
  --background-color: #1f2937;
  --text-color: #f9fafb;
}

.dark .card {
  @apply bg-gray-800 text-white;
}

.dark .btn-primary {
  @apply bg-blue-600 hover:bg-blue-800;
}
```

**다크모드 토글:**
```javascript
// themeStore.js
export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem('theme') || 'light')

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
  }

  return { theme, toggleTheme }
})
```

### Font Awesome

**HTML 진입점:** [index.html](index.html)

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

**사용 예시:**
```vue
<i class="fas fa-heart"></i>  <!-- 하트 아이콘 -->
<i class="fas fa-star"></i>   <!-- 별 아이콘 -->
```

---

## ⚙ 환경 설정

### 환경 변수

**파일:** `.env_` (템플릿)

```env
VITE_KAKAO_MAP_API_KEY=your_kakao_map_api_key_here
```

**실제 사용:**
1. `.env_`를 `.env`로 복사
2. Kakao Map API 키 발급 ([Kakao Developers](https://developers.kakao.com/))
3. `.env` 파일에 키 입력

**코드에서 접근:**
```javascript
const kakaoMapKey = import.meta.env.VITE_KAKAO_MAP_API_KEY
```

### jsconfig.json

**파일:** [jsconfig.json](jsconfig.json)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "exclude": ["node_modules", "dist"]
}
```

**효과:** `@` alias로 절대 경로 사용 가능

```javascript
// 상대 경로 (X)
import MyComponent from '../../../components/MyComponent.vue'

// 절대 경로 (O)
import MyComponent from '@/components/MyComponent.vue'
```

### Vite 설정

**파일:** [vite.config.js](vite.config.js)

```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
```

### PostCSS 설정

**파일:** [postcss.config.js](postcss.config.js)

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### VSCode 권장 확장

**파일:** [.vscode/extensions.json](.vscode/extensions.json)

```json
{
  "recommendations": ["Vue.volar"]
}
```

---

## 👨‍💻 개발 가이드

### 사전 요구사항

- **Node.js**: ^20.19.0 또는 >=22.12.0
- **npm**: (Node.js와 함께 설치됨)
- **Git**: 버전 관리

### 설치 및 실행

#### 1. 저장소 클론
```bash
git clone <repository-url>
cd final-pjt/front
```

#### 2. 의존성 설치
```bash
npm install
```

#### 3. 환경 변수 설정
```bash
# .env_ 파일을 .env로 복사
cp .env_ .env

# .env 파일에 Kakao Map API 키 입력
# VITE_KAKAO_MAP_API_KEY=your_key_here
```

#### 4. 개발 서버 실행
```bash
npm run dev
```

개발 서버가 [http://localhost:5173](http://localhost:5173)에서 실행됩니다.

### 개발 워크플로우

#### 1. 컴포넌트 생성
```vue
<!-- src/components/MyComponent.vue -->
<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: String
})

const emit = defineEmits(['click'])
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
    <button @click="emit('click')">클릭</button>
  </div>
</template>

<style scoped>
/* 컴포넌트 전용 스타일 */
</style>
```

#### 2. Composable 생성
```javascript
// src/composables/useMyFeature.js
import { ref, onMounted } from 'vue'

export function useMyFeature() {
  const data = ref(null)

  const fetchData = async () => {
    // 데이터 페칭 로직
  }

  onMounted(() => {
    fetchData()
  })

  return { data, fetchData }
}
```

#### 3. Pinia 스토어 추가
```javascript
// src/stores/myStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMyStore = defineStore('my', () => {
  // State
  const items = ref([])

  // Computed
  const itemCount = computed(() => items.value.length)

  // Actions
  const addItem = (item) => {
    items.value.push(item)
  }

  return { items, itemCount, addItem }
})
```

#### 4. API 모듈 추가
```javascript
// src/api/myApi.js
import apiClient from './axios'

export const getMyData = () => apiClient.get('/my-endpoint/')
export const createMyData = (data) => apiClient.post('/my-endpoint/', data)
```

### 디버깅

#### Vue DevTools
```bash
# 이미 vite-plugin-vue-devtools가 설치되어 있음
# 개발 서버 실행 시 자동으로 활성화됨
```

#### Console Logging
```javascript
console.log('데이터:', data)
console.error('에러:', error)
console.warn('경고:', warning)
```

#### Network 탭
브라우저 개발자 도구의 Network 탭에서 API 요청/응답 확인

---

## 🚀 빌드 및 배포

### 프로덕션 빌드

```bash
npm run build
```

**빌드 결과:**
- 최적화된 파일이 `dist/` 폴더에 생성됨
- JavaScript 번들 최소화 (minification)
- CSS 최적화 및 추출
- 정적 에셋 처리

### 빌드 미리보기

```bash
npm run preview
```

로컬에서 프로덕션 빌드를 미리 확인할 수 있습니다.

### 배포 준비사항

#### 1. 환경 변수 설정
```env
# .env.production
VITE_API_BASE_URL=https://api.your-domain.com
VITE_KAKAO_MAP_API_KEY=your_production_key
```

#### 2. API 엔드포인트 변경
```javascript
// src/api/axios.js
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  // ...
})
```

#### 3. 정적 파일 호스팅
빌드된 `dist/` 폴더를 다음 플랫폼에 배포:
- **Vercel**: `vercel deploy`
- **Netlify**: `netlify deploy --prod`
- **GitHub Pages**: Actions를 통한 자동 배포
- **AWS S3 + CloudFront**: S3 버킷에 업로드 후 CDN 연결

### 성능 최적화

#### 1. 코드 스플리팅 (이미 적용됨)
```javascript
// 라우트별 지연 로딩
{
  path: '/performances/:id',
  component: () => import('@/views/Performance/PerformanceDetailView.vue')
}
```

#### 2. 이미지 최적화
- 적절한 이미지 포맷 사용 (WebP, AVIF)
- Lazy Loading 적용
- CDN을 통한 이미지 제공

#### 3. Bundle 분석
```bash
npm install -D rollup-plugin-visualizer

# vite.config.js에 추가
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    vue(),
    visualizer()
  ]
})
```

---

## 📊 데이터 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                      (Vue Components)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 1. 컴포넌트에서 스토어 액션 호출
                       │    예: onMounted(() => performanceStore.fetchPerformances())
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                     Pinia Store Layer                        │
│  (performanceStore, communityStore, authStore, ...)          │
│  - 상태 관리 (ref, computed)                                  │
│  - 비즈니스 로직                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 2. API 모듈 함수 호출
                       │    예: await getPerformances(params)
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Module Layer                        │
│  (performances.js, community.js, auth.js, ...)               │
│  - API 엔드포인트별 함수 정의                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 3. Axios 인스턴스 사용
                       │    예: apiClient.get('/performances/')
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   Axios Client (axios.js)                    │
│  - Request Interceptor: JWT 토큰 자동 첨부                    │
│  - Response Interceptor: 401 에러 시 토큰 자동 갱신           │
│  - baseURL: http://127.0.0.1:8000/api                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 4. HTTP Request (CORS + JWT)
                       │    예: GET /api/performances/
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                      Django Backend                          │
│                   (http://127.0.0.1:8000)                    │
│  - CORS 처리 (django-cors-headers)                           │
│  - JWT 인증 검증 (djangorestframework-simplejwt)             │
│  - API ViewSet 라우팅                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 5. JSON Response
                       │    예: { "results": [...], "count": 100 }
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   Response Processing                        │
│  - Axios 인터셉터: 에러 처리, 토큰 갱신                        │
│  - API 모듈: response.data 반환                               │
│  - Pinia 스토어: 상태 업데이트                                 │
│  - Vue 컴포넌트: 반응형 UI 자동 업데이트                        │
└─────────────────────────────────────────────────────────────┘
```

### 주요 특징

1. **단방향 데이터 흐름**: User Action → Store → API → Backend → Store → UI Update
2. **자동 토큰 관리**: 401 에러 발생 시 Axios 인터셉터가 자동으로 토큰 갱신 후 요청 재시도
3. **반응형 상태**: Pinia의 반응형 상태 덕분에 스토어 업데이트 시 컴포넌트 자동 리렌더링
4. **낙관적 업데이트**: 찜/관람함 등에서 UI 즉시 업데이트 후 서버 요청 (실패 시 롤백)

---

## 🔐 보안 고려사항

### 1. JWT 토큰 관리
- ✅ Access Token은 localStorage에 저장 (XSS 취약점 주의)
- ✅ Refresh Token으로 자동 갱신
- ✅ 로그아웃 시 토큰 완전 삭제
- ⚠️ **개선 방안**: HttpOnly 쿠키로 Refresh Token 저장 고려

### 2. CORS 설정
- ✅ `withCredentials: true` 설정
- ✅ 백엔드에서 허용된 오리진만 접근 가능

### 3. 사용자 입력 검증
- ✅ 폼 검증 (Composables에서 처리)
- ✅ XSS 방지 (Vue의 자동 이스케이핑)

### 4. 환경 변수 보호
- ✅ `.env` 파일은 `.gitignore`에 포함
- ✅ API 키는 환경 변수로 관리

---

## 🧪 테스트 (향후 개선)

### 권장 테스트 프레임워크
- **Vitest**: Vite 네이티브 테스트 러너
- **Vue Test Utils**: Vue 컴포넌트 테스트
- **Cypress**: E2E 테스트

### 테스트 예시
```javascript
// MyComponent.spec.js
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: { title: 'Hello' }
    })
    expect(wrapper.text()).toContain('Hello')
  })
})
```

---

## 📝 추가 문서

프로젝트의 다른 중요 문서:
- **Backend README**: 백엔드 API 및 Django 설정 (별도 작성 예정)
- **Full README**: 프론트엔드 + 백엔드 통합 문서 (병합 예정)

---

## 🤝 기여 가이드

### Branch 규칙
- `master`: 최종 배포 버전
- `develop`: 개발 브랜치
- `feature/<feature-name>`: 기능 개발 브랜치

### Commit 규칙
```
<type>: <subject>

<body> (선택사항)
```

**Type 종류:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `style`: 코드 포맷팅
- `docs`: 문서 수정
- `test`: 테스트 추가/수정
- `chore`: 빌드/패키지 관리

**예시:**
```
feat: AI 검색 기능 추가
fix: 공연 상세 페이지 무한 로딩 버그 수정
refactor: Composables 패턴으로 로직 분리
docs: README에 API 문서 추가
```

---

## 📞 문제 해결

### 자주 발생하는 문제

#### 1. Node 버전 불일치
```bash
# Node 버전 확인
node -v

# nvm 사용 시
nvm install 20.19.0
nvm use 20.19.0
```

#### 2. 의존성 설치 실패
```bash
# node_modules 및 package-lock.json 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

#### 3. CORS 에러
- 백엔드 CORS 설정 확인 (`django-cors-headers`)
- API baseURL 확인 ([src/api/axios.js](src/api/axios.js))

#### 4. 토큰 갱신 실패
- Refresh Token 만료 확인
- 로그아웃 후 재로그인

#### 5. Kakao Map 로드 실패
- `.env` 파일에 API 키 입력 확인
- Kakao Developers 콘솔에서 도메인 등록 확인

---

## 📚 참고 자료

### 공식 문서
- [Vue 3 공식 문서](https://vuejs.org/)
- [Pinia 공식 문서](https://pinia.vuejs.org/)
- [Vue Router 공식 문서](https://router.vuejs.org/)
- [Vite 공식 문서](https://vitejs.dev/)
- [Tailwind CSS 공식 문서](https://tailwindcss.com/)
- [Axios 공식 문서](https://axios-http.com/)

### 추가 학습 자료
- [Vue 3 Composition API RFC](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0013-composition-api.md)
- [Vue 3 Best Practices](https://vuejs.org/guide/best-practices/production-deployment.html)
- [Kakao Map API 문서](https://apis.map.kakao.com/)

---

## 📄 라이센스

본 프로젝트는 교육 목적으로 제작되었습니다.

---

## 👥 제작자

**Frontend Developer:** 임경수
**프로젝트 기간:** 2025.12.13 - 2025.12.23

---

**🎉 이 문서는 프론트엔드 개발자와 협업하는 백엔드 개발자, 그리고 향후 유지보수를 담당할 개발자를 위해 작성되었습니다.**
