# 공연 정보 & 커뮤니티 플랫폼 - 프로젝트 문서

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [기술 스택](#기술-스택)
3. [주요 기능](#주요-기능)
4. [시스템 아키텍처](#시스템-아키텍처)
5. [프론트엔드 구조](#프론트엔드-구조)
6. [백엔드 구조](#백엔드-구조)
7. [데이터베이스 설계](#데이터베이스-설계)
8. [설치 및 실행](#설치-및-실행)
9. [주요 기능 상세](#주요-기능-상세)
10. [API 명세](#api-명세)

---

## 프로젝트 개요

### 프로젝트명
**공연 정보 & 추천 커뮤니티 플랫폼**

### 목적
- 공연 예술에 관심 있는 사용자에게 맞춤형 공연 정보 제공
- AI 기반 의미 검색으로 자연어 질의 지원
- 사용자 간 공연 후기/기대평 공유 커뮤니티 구축
- 박스오피스 랭킹 및 장르별 인기 공연 정보 제공

### 개발 기간
- 2025.12.13 - 2025.12.23

### 팀 구성
| 역할 | 이름 | 담당 |
|------|------|------|
| Leader | 이재호 | 백엔드 설계, 공연 API 통합, AI 검색 시스템 |
| Member | 임경수 | 프론트엔드 개발, UI/UX 설계, 컴포넌트 리팩토링 |

---

## 기술 스택

### Frontend
- **Framework**: Vue 3.5.25 (Composition API)
- **State Management**: Pinia 3.0.4
- **Routing**: Vue Router 4.6.3
- **Build Tool**: Vite 7.2.4
- **HTTP Client**: Axios 1.13.2
- **Styling**: Tailwind CSS 3.4.0, PostCSS

### Backend
- **Framework**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **Database**: SQLite (개발), PostgreSQL/MySQL (프로덕션 권장)
- **CORS**: django-cors-headers 4.9.0
- **Filtering**: django-filter 25.2

### AI & Machine Learning
- **OpenAI API**: 의미 기반 검색 (임베딩 생성)
- **scikit-learn**: 코사인 유사도 계산
- **Numpy**: 벡터 연산

### External APIs
- **KOPIS API**: 공연 정보 제공
- **Kakao Maps API**: 공연장 위치 표시
- **YouTube Data API**: 공연 관련 영상

---

## 주요 기능

### 1. 공연 정보 시스템
- ✅ 공연 목록 조회 (필터링: 장르, 지역, 기간, 검색어)
- ✅ 공연 상세 정보 (포스터, 출연진, 시설, 가격, 시놀시스)
- ✅ 박스오피스 랭킹 (장르별, 전체)
- ✅ 하이라이트 공연 캐러셀
- ✅ 공연 찜하기/취소
- ✅ 카카오 지도 연동 (공연장 위치)
- ✅ YouTube 공연 영상 재생

### 2. 커뮤니티
- ✅ 게시글 CRUD (공연별, 일반)
- ✅ 카테고리: 후기(REVIEW), 기대평(EXPECTATION), Q&A, 자유게시판, 정보공유
- ✅ 댓글 시스템
- ✅ 좋아요 기능 (게시글, 댓글)
- ✅ 베스트 리뷰 (좋아요 많은 순)
- ✅ 정렬 (최신순, 인기순)
- ✅ 검색 (제목, 내용)

### 3. 사용자 인증 & 프로필
- ✅ 회원가입/로그인 (JWT)
- ✅ 온보딩 시스템 (선호 장르, 배우, 지역)
- ✅ 마이페이지 (프로필, 작성글, 찜, 관람이력)
- ✅ 팔로우 시스템
- ✅ 회원 탈퇴

### 4. AI 추천 시스템
- ✅ 자연어 의미 검색 (예: "우울할 때 위로가 되는 뮤지컬")
- ✅ 코사인 유사도 기반 Top-N 추천
- ✅ LLM 기반 추천 사유 생성
- ✅ 사용자 선호도 기반 맞춤 추천

### 5. 랭킹 시스템
- ✅ 장르별 박스오피스 Top 10
- ✅ 전체 박스오피스 Top 10
- ✅ 순위 변동 추적
- ✅ 좌석수/공연횟수 기준 정렬

---

## 시스템 아키텍처

### 전체 구조
```
┌─────────────────────────────────────────────────────────┐
│                     Vue 3 Frontend                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Router     │  │    Pinia     │  │ Composables  │  │
│  │  (Routes)    │  │   (Stores)   │  │   (Logic)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Components (53개)                     │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Axios HTTP Client                      │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/JSON (REST API)
                       │
┌──────────────────────▼──────────────────────────────────┐
│                Django REST Framework                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  ViewSets    │  │ Serializers  │  │    Models    │  │
│  │  (API Logic) │  │  (Validate)  │  │  (Database)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  JWT Authentication (simplejwt)                  │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           │           │           │
      ┌────▼───┐  ┌───▼────┐  ┌──▼─────┐
      │ SQLite │  │ OpenAI │  │ KOPIS  │
      │   DB   │  │  API   │  │  API   │
      └────────┘  └────────┘  └────────┘
```

### 데이터 흐름
```
User Action (Vue Component)
    ↓
Pinia Store Action
    ↓
API Module (Axios)
    ↓
Django REST API ViewSet
    ↓
Serializer (Validation)
    ↓
Model (Database ORM)
    ↓
SQLite Database
```

---

## 프론트엔드 구조

### 디렉토리 구조
```
front/src/
├── api/                    # API 통신 모듈 (10개)
│   ├── axios.js           # Axios 인스턴스 + 인터셉터
│   ├── auth.js            # 인증 API
│   ├── performances.js    # 공연 API
│   ├── community.js       # 커뮤니티 API
│   └── ...
├── assets/                # 정적 리소스
├── components/            # 재사용 컴포넌트 (53개)
│   ├── Common/           # 공통 컴포넌트 (4개)
│   ├── BoxOffice/        # 박스오피스 (11개)
│   ├── Community/        # 커뮤니티 (12개)
│   ├── Performance/      # 공연 (3개)
│   ├── PerformanceDetail/# 공연 상세 (6개)
│   ├── Recommendation/   # 추천 (2개)
│   ├── User/             # 사용자 (10개)
│   └── YouTube/          # YouTube (2개)
├── composables/           # 재사용 로직 (9개)
│   ├── useBoxOffice.js
│   ├── usePerformanceDetail.js
│   └── ...
├── router/                # Vue Router 설정
│   └── index.js
├── stores/                # Pinia 상태 관리 (12개)
│   ├── authStore.js
│   ├── performanceStore.js
│   ├── communityStore.js
│   └── ...
├── views/                 # 페이지 컴포넌트 (20+개)
│   ├── LandingView.vue
│   ├── Performance/
│   ├── Community/
│   ├── Auth/
│   ├── User/
│   ├── Ranking/
│   └── Admin/
├── App.vue
└── main.js
```

### 주요 라우트
| Path | 컴포넌트 | 설명 | 인증 필요 |
|------|---------|------|----------|
| `/` | LandingView | 홈/랜딩 페이지 | ❌ |
| `/performances` | PerformanceListView | 공연 목록 | ❌ |
| `/performances/:id` | PerformanceDetailView | 공연 상세 | ❌ |
| `/community` | CommunityView | 커뮤니티 | ❌ |
| `/community/:id` | ArticleDetailView | 게시글 상세 | ❌ |
| `/community/write` | CommunityWriteView | 글쓰기 | ✅ |
| `/login` | LoginView | 로그인 | ❌ |
| `/register` | RegisterView | 회원가입 | ❌ |
| `/onboarding` | OnboardingView | 온보딩 | ✅ |
| `/mypage` | MyPageView | 마이페이지 | ✅ |
| `/rankings` | RankingsView | 랭킹 | ❌ |
| `/recommands` | RecommandsView | AI 추천 | ❌ |

### 주요 Store

**authStore.js**
```javascript
- State: user, accessToken, refreshToken, loading
- Actions: login, logout, register, fetchCurrentUser, initialize
- Getters: isAuthenticated, username, isAdmin
```

**performanceStore.js**
```javascript
- State: performances, currentPerformance, boxOfficeRankings
- Actions: fetchPerformances, fetchPerformance, toggleLike
- 특징: 전역 찜 상태 동기화
```

**communityStore.js**
```javascript
- State: articles, comments, filters, bestReviews
- Actions: CRUD, 좋아요, 필터링
- Filters: board_type, category, search, ordering
```

### 컴포넌트 재사용 패턴

**BasePerformanceCard.vue**
- 모든 공연 카드의 기본 컴포넌트
- 3개의 Named Slot 제공: `#badge`, `#info`, `#footer`
- Props: performance, showLikeButton, cardClass, clickable

**사용 예시:**
```vue
<BasePerformanceCard :performance="perf" card-class="boxoffice-card">
  <template #badge>
    <div class="rank-badge">{{ perf.rank }}위</div>
  </template>
  <template #footer>
    <span class="genre-tag">{{ perf.genrenm }}</span>
  </template>
</BasePerformanceCard>
```

---

## 백엔드 구조

### 디렉토리 구조
```
back/
├── mypjt/                 # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              # 사용자 인증
│   ├── models.py
│   ├── serializers.py
│   ├── views/
│   │   └── api_views.py
│   └── urls.py
├── performances/          # 공연 정보
│   ├── models.py
│   ├── serializers.py
│   ├── views/
│   │   └── api_views.py
│   └── urls.py
├── community/             # 커뮤니티
│   ├── models.py
│   ├── serializers.py
│   ├── views/
│   │   └── api_views.py
│   └── urls.py
├── recommendations/       # AI 추천
│   ├── models.py
│   ├── serializers.py
│   ├── views/
│   │   └── api_views.py
│   └── urls.py
├── db.sqlite3
└── manage.py
```

### 주요 모델

**User (accounts/models.py)**
```python
class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    preference_tags = models.JSONField(default=list)
    favorite_actors = models.JSONField(default=list)
    birth_date = models.DateField(null=True, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    has_onboarded = models.BooleanField(default=False)
    onboarded_at = models.DateTimeField(null=True, blank=True)
```

**Performance (performances/models.py)**
```python
class Performance(models.Model):
    mt20id = models.CharField(max_length=50, primary_key=True)
    prfnm = models.CharField(max_length=255)
    prfpdfrom = models.DateField()
    prfpdto = models.DateField()
    fcltynm = models.CharField(max_length=255)
    poster = models.URLField()
    area = models.CharField(max_length=50, null=True, blank=True)
    genrenm = models.CharField(max_length=50, null=True, blank=True)
    prfstate = models.CharField(max_length=50)
    like_users = models.ManyToManyField(User, related_name='favorite_performances')
```

**BoxOfficeRanking (performances/models.py)**
```python
class BoxOfficeRanking(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    rank = models.IntegerField()
    genre_code = models.CharField(max_length=10)
    ranking_date = models.DateField()
    period_type = models.CharField(max_length=10)
    seat_count = models.IntegerField(default=0)
    performance_count = models.IntegerField(default=0)
```

**Article (community/models.py)**
```python
class Article(models.Model):
    BOARD_TYPE_CHOICES = [
        ('PERFORMANCE', 'Performance'),
        ('GENERAL', 'General')
    ]
    CATEGORY_CHOICES = [
        ('REVIEW', 'Review'),
        ('EXPECTATION', 'Expectation'),
        ('QNA', 'QnA'),
        ('FREE', 'Free'),
        ('INFO', 'Info')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_type = models.CharField(max_length=20, choices=BOARD_TYPE_CHOICES)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    like_users = models.ManyToManyField(User, related_name='like_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ViewSet 구조

**PerformanceViewSet**
```python
class PerformanceViewSet(ReadOnlyModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genrenm', 'area', 'prfstate']
    search_fields = ['prfnm', 'fcltynm', 'cast_search_text']

    @action(detail=False, methods=['GET'])
    def boxoffice_genre(self, request):
        # 장르별 박스오피스 Top 10

    @action(detail=False, methods=['GET'])
    def boxoffice_all(self, request):
        # 전체 박스오피스 Top 10

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        # 찜하기/취소 토글

    @action(detail=False, methods=['POST'])
    def ai_search(self, request):
        # AI 의미 기반 검색
```

**ArticleViewSet**
```python
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['board_type', 'category', 'performance__mt20id']
    search_fields = ['title', 'content']

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        # 좋아요 토글

    @action(detail=False, methods=['GET'])
    def best_reviews(self, request):
        # 베스트 리뷰 (좋아요 많은 순 Top 10)
```

---

## 데이터베이스 설계

### ERD
```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ nickname        │
│ region          │
│ preference_tags │
│ favorite_actors │
│ has_onboarded   │
└─────────────────┘
       │ 1
       │
       │ N
┌─────────────────┐      N  ┌─────────────────┐
│    Article      │─────────│  Performance    │
├─────────────────┤    M2M  ├─────────────────┤
│ id (PK)         │         │ mt20id (PK)     │
│ user_id (FK)    │◄────────│ prfnm           │
│ performance (FK)│    like │ prfpdfrom       │
│ board_type      │         │ prfpdto         │
│ category        │         │ fcltynm         │
│ title           │         │ poster          │
│ content         │         │ genrenm         │
│ rank            │         │ area            │
│ created_at      │         └─────────────────┘
└─────────────────┘                │ 1
       │ 1                         │
       │                           │ N
       │ N                  ┌──────────────────┐
┌─────────────────┐         │BoxOfficeRanking  │
│    Comment      │         ├──────────────────┤
├─────────────────┤         │ id (PK)          │
│ id (PK)         │         │ performance (FK) │
│ article_id (FK) │         │ rank             │
│ user_id (FK)    │         │ genre_code       │
│ content         │         │ ranking_date     │
│ created_at      │         │ seat_count       │
└─────────────────┘         │ performance_count│
                            └──────────────────┘
```

### 인덱스 설정
```python
# Performance
indexes = [
    models.Index(fields=['prfstate']),
    models.Index(fields=['genrenm']),
    models.Index(fields=['prfpdfrom', 'prfpdto']),
    models.Index(fields=['area']),
]

# BoxOfficeRanking
indexes = [
    models.Index(fields=['ranking_date', 'rank']),
    models.Index(fields=['genre_code']),
]

# Article
indexes = [
    models.Index(fields=['board_type', 'category']),
    models.Index(fields=['-created_at']),
    models.Index(fields=['-like_count']),
]
```

---

## 설치 및 실행

### 사전 요구사항
- Python 3.10+
- Node.js 18+
- npm 9+

### 백엔드 설치 및 실행

```bash
# 1. 프로젝트 클론
git clone <repository-url>
cd final-pjt/back

# 2. 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정 (.env 파일 생성)
# OPENAI_API_KEY=<your-openai-api-key>
# KOPIS_API_KEY=<your-kopis-api-key>

# 5. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 6. 슈퍼유저 생성 (선택)
python manage.py createsuperuser

# 7. 개발 서버 실행
python manage.py runserver
```

### 프론트엔드 설치 및 실행

```bash
# 1. 프론트엔드 디렉토리 이동
cd final-pjt/front

# 2. 의존성 설치
npm install

# 3. 개발 서버 실행
npm run dev

# 4. 프로덕션 빌드
npm run build
```

### 접속 정보
- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

## 주요 기능 상세

### 1. 공연 정보 시스템

#### 공연 목록 조회
- **경로**: `/performances`
- **기능**:
  - 장르별 필터링 (뮤지컬, 연극, 콘서트 등)
  - 지역별 필터링 (서울, 경기, 부산 등)
  - 공연 상태 필터링 (공연중, 공연예정, 공연완료)
  - 제목/시설명/출연진 검색
  - 무한 스크롤 페이지네이션

#### 공연 상세 정보
- **경로**: `/performances/:id`
- **포함 정보**:
  - 기본 정보 (제목, 기간, 장소, 가격, 출연진, 제작진)
  - 포스터 이미지
  - 시놀시스
  - 카카오 지도 (공연장 위치)
  - YouTube 공연 영상
  - 평점 차트 (별점 분포)
  - 리뷰 목록 (최신순, 좋아요순)

#### 박스오피스 랭킹
- **장르별 Top 10**: 뮤지컬, 연극, 클래식, 무용, 대중콘서트
- **전체 Top 10**: 모든 장르 통합 랭킹
- **순위 변동**: 실시간 순위 업데이트
- **지표**: 좌석수, 공연횟수

### 2. 커뮤니티 시스템

#### 게시판 구조
```
PERFORMANCE (공연 게시판)
├── REVIEW (후기) - 별점 필수
├── EXPECTATION (기대평) - 별점 자동 2.5
└── QNA (질문)

GENERAL (일반 게시판)
├── FREE (자유게시판)
└── INFO (정보공유)
```

#### 게시글 작성
- **모달 기반 3단계 작성**:
  1. 게시판 선택 (PERFORMANCE / GENERAL)
  2. 공연 검색 (PERFORMANCE만 해당)
  3. 카테고리 선택 + 내용 작성

- **별점 로직**:
  - REVIEW: 별점 입력 필수 (0.5 단위)
  - EXPECTATION: 별점 자동 2.5점
  - 기타: 별점 없음

#### 게시글 상세
- 작성자 정보 (닉네임, 프로필 이미지)
- 공연 정보 카드 (PERFORMANCE 타입만)
- 카테고리 배지 (그라디언트 스타일)
- 별점 표시 (별 아이콘)
- 좋아요/댓글 수
- 댓글 목록 (페이지네이션)
- 댓글 작성 (로그인 필요)

#### 베스트 리뷰
- 좋아요 10개 이상 게시글
- 좋아요 많은 순 정렬
- 카드 형식 그리드 레이아웃

### 3. 사용자 인증 시스템

#### 회원가입
- **필수 정보**: username, nickname, email, password
- **선택 정보**: 거주 지역, 생년월일
- **검증**:
  - 닉네임 중복 체크 (실시간)
  - 비밀번호 강도 검증
  - 이메일 형식 검증

#### 로그인
- JWT 토큰 기반 (Access + Refresh)
- 자동 로그인 (localStorage)
- 로그인 후 리다이렉트 (이전 페이지)

#### 온보딩 시스템
- **1단계**: 선호 장르 선택 (다중 선택)
  - 뮤지컬, 연극, 콘서트, 클래식, 무용, 국악, 오페라, 복합, 서커스/마술
- **2단계**: 선호 배우 입력 (쉼표 구분)
- **3단계**: 거주 지역 선택
- **강제 유도**: 로그인 후 온보딩 미완료 시 자동 리다이렉트
- **다시 보지 않기**: 사용자별 스킵 옵션

#### 마이페이지
- **프로필 섹션**:
  - 프로필 이미지 업로드
  - 닉네임, 생년월일 수정
  - 팔로워/팔로잉 수

- **탭 메뉴**:
  - 찜한 공연 (grid 레이아웃)
  - 관람한 공연 (시간순 정렬)
  - 작성한 게시글/댓글

- **계정 설정**:
  - 비밀번호 변경 (현재 비밀번호 확인)
  - 회원 탈퇴

### 4. AI 추천 시스템

#### 의미 기반 검색
- **입력**: 자연어 질의
  - 예시: "우울할 때 위로가 되는 뮤지컬"
  - 예시: "가족과 함께 볼 수 있는 재미있는 공연"

- **처리 과정**:
  1. OpenAI API로 쿼리 임베딩 생성
  2. 공연 정보 임베딩과 코사인 유사도 계산
  3. Top-N 공연 추출
  4. LLM이 추천 사유 생성

- **결과**: 추천 공연 카드 + 추천 이유

#### 맞춤 추천
- 사용자 온보딩 데이터 활용
- 선호 장르 가중치
- 거주 지역 근접성
- 선호 배우 출연 여부

### 5. 랭킹 시스템

#### 전체 랭킹
- 모든 장르 통합 Top 10
- 좌석수 기준 정렬
- 순위 배지 (금/은/동 그라디언트)
- 캐러셀 UI (5개씩 페이지네이션)

#### 장르별 랭킹
- 장르 탭: 대중콘서트, 뮤지컬, 클래식, 무용, 연극, 기타
- 각 장르 Top 10
- 장르별 더보기 페이지
- 실시간 순위 업데이트

---

## API 명세

### Authentication

#### 회원가입
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "user123",
  "nickname": "닉네임",
  "email": "user@example.com",
  "password": "password123",
  "region": "서울",
  "birth_date": "1990-01-01"
}
```

#### 로그인
```http
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "user123",
    "nickname": "닉네임",
    "email": "user@example.com"
  }
}
```

#### 토큰 갱신
```http
POST /api/accounts/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Performances

#### 공연 목록 조회
```http
GET /api/performances/?genrenm=뮤지컬&area=서울&search=레미제라블
Authorization: Bearer <access_token>
```

#### 공연 상세 조회
```http
GET /api/performances/PF275646/
Authorization: Bearer <access_token>
```

#### 박스오피스 (장르별)
```http
GET /api/performances/boxoffice-genre/?genre=BBBC
Authorization: Bearer <access_token>

# Response
{
  "success": true,
  "count": 10,
  "rankings": [
    {
      "rank": 1,
      "performance": {
        "mt20id": "PF275646",
        "prfnm": "공연명",
        "poster": "http://...",
        "genrenm": "뮤지컬",
        "is_liked": false,
        "like_count": 123
      },
      "seat_count": 15000,
      "performance_count": 50
    },
    ...
  ]
}
```

#### 박스오피스 (전체)
```http
GET /api/performances/boxoffice-all/
```

#### 찜하기/취소
```http
POST /api/performances/PF275646/like/
Authorization: Bearer <access_token>

# Response
{
  "success": true,
  "is_liked": true,
  "like_count": 124
}
```

#### AI 의미 검색
```http
POST /api/performances/ai-search/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "우울할 때 위로가 되는 뮤지컬",
  "top_n": 5
}

# Response
{
  "success": true,
  "query": "우울할 때 위로가 되는 뮤지컬",
  "recommendations": [
    {
      "performance": {...},
      "similarity": 0.85,
      "reason": "감동적인 스토리와 아름다운 음악으로..."
    },
    ...
  ]
}
```

### Community

#### 게시글 목록 조회
```http
GET /api/community/articles/?board_type=PERFORMANCE&category=REVIEW&ordering=-created_at
Authorization: Bearer <access_token>
```

#### 게시글 생성
```http
POST /api/community/articles/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "board_type": "PERFORMANCE",
  "performance": "PF275646",
  "category": "REVIEW",
  "title": "정말 감동적인 공연이었습니다",
  "content": "...",
  "rank": 4.5
}
```

#### 게시글 상세 조회
```http
GET /api/community/articles/123/
Authorization: Bearer <access_token>
```

#### 게시글 좋아요
```http
POST /api/community/articles/123/like/
Authorization: Bearer <access_token>

# Response
{
  "success": true,
  "is_liked": true,
  "like_count": 15
}
```

#### 베스트 리뷰
```http
GET /api/community/articles/best-reviews/
Authorization: Bearer <access_token>
```

#### 댓글 목록 조회
```http
GET /api/community/comments/?article=123
Authorization: Bearer <access_token>
```

#### 댓글 생성
```http
POST /api/community/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "article": 123,
  "content": "좋은 후기 감사합니다!"
}
```

### Users

#### 현재 사용자 정보
```http
GET /api/accounts/users/me/
Authorization: Bearer <access_token>
```

#### 팔로우/언팔로우
```http
POST /api/accounts/users/123/follow/
Authorization: Bearer <access_token>

# Response
{
  "success": true,
  "is_following": true
}
```

#### 비밀번호 확인
```http
POST /api/accounts/users/verify_password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "password": "current_password"
}
```

#### 프로필 수정
```http
PATCH /api/accounts/users/update_profile/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "nickname": "새로운닉네임",
  "birth_date": "1990-01-01",
  "profile_image": <file>
}
```

#### 회원 탈퇴
```http
DELETE /api/accounts/users/delete_account/
Authorization: Bearer <access_token>
```

---

## 보안 고려사항

### 1. JWT 토큰 관리
- Access Token 만료: 1시간
- Refresh Token 만료: 7일
- 자동 갱신 인터셉터
- Secure Storage (httpOnly 권장)

### 2. CORS 설정
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
```

### 3. SQL Injection 방지
- Django ORM 사용
- Parameterized Queries

### 4. XSS 방지
- Vue.js의 자동 이스케이핑
- v-html 사용 제한

### 5. CSRF 보호
- Django CSRF 토큰
- SameSite Cookie

---

## 성능 최적화

### 1. 백엔드
- **쿼리 최적화**: select_related, prefetch_related
- **인덱싱**: 자주 조회되는 필드
- **캐싱**: Django In-Memory Cache

### 2. 프론트엔드
- **코드 스플리팅**: Vue Router dynamic import
- **지연 로딩**: 이미지 lazy loading
- **번들 최적화**: Vite 자동 최적화
- **컴포넌트 재사용**: Slot 패턴

### 3. 데이터베이스
- **복합 인덱스**: (ranking_date, rank)
- **M2M 최적화**: through 테이블 인덱싱

---

## 배포 가이드

### 프론트엔드 (Vercel/Netlify)
```bash
npm run build
# dist 폴더를 배포
```

### 백엔드 (Heroku/AWS/DigitalOcean)
```bash
# 1. 정적 파일 수집
python manage.py collectstatic

# 2. 프로덕션 서버 실행 (gunicorn)
gunicorn mypjt.wsgi:application

# 3. 환경변수 설정
# - SECRET_KEY
# - DEBUG=False
# - ALLOWED_HOSTS
# - DATABASE_URL
# - OPENAI_API_KEY
```

---

## 트러블슈팅

### 1. CORS 에러
**증상**: 프론트엔드에서 API 호출 시 CORS 에러
**해결**: `settings.py`의 CORS_ALLOWED_ORIGINS에 프론트엔드 URL 추가

### 2. 토큰 만료
**증상**: 401 Unauthorized 에러
**해결**: Refresh 토큰으로 자동 갱신 (axios 인터셉터)

### 3. 찜하기 상태 불일치
**증상**: 찜하기 후 다른 페이지에서 상태 반영 안됨
**해결**: performanceStore의 전역 상태 동기화 로직

### 4. 온보딩 무한 리다이렉트
**증상**: 온보딩 완료 후에도 계속 온보딩 페이지로 이동
**해결**: localStorage에 스킵 플래그 저장

---

## 향후 개선 사항

### 1. 기능 추가
- [ ] 실시간 채팅 (WebSocket)
- [ ] 공연 알림 (관심 공연 오픈 시)
- [ ] 티켓 예매 연동
- [ ] 공연 리뷰 작성 시 이미지 업로드
- [ ] 사용자 간 메시지

### 2. 성능 개선
- [ ] Redis 캐싱
- [ ] CDN 적용 (이미지, 정적 파일)
- [ ] 무한 스크롤 최적화
- [ ] Server-Side Rendering (Nuxt.js)

### 3. UX 개선
- [ ] PWA 지원
- [ ] 다국어 지원 (i18n)
- [ ] 접근성 개선 (ARIA)
- [ ] 모바일 앱 (React Native)

---

## 라이선스
MIT License

---

## 문의
- Leader: 이재호
- Member: 임경수

---

**문서 작성일**: 2025-12-23
**최종 수정일**: 2025-12-23
