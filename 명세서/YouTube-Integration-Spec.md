# YouTube 영상 통합 기능 명세서

## 📋 프로젝트 개요

**작업 날짜**: 2025-12-21
**작업자**: Claude (AI Assistant)
**프로젝트**: PlayPick - 공연 추천 커뮤니티 플랫폼
**기능**: YouTube 영상 통합 (메인 페이지 플레이리스트 & 공연 상세 영상)

---

## 🎯 기능 요구사항

### A. 메인 페이지: 플레이리스트 기반 영상 섹션

**목적**: 사용자에게 추천 공연 영상을 보여주어 시각적 경험 제공

**기능 상세**:
- YouTube 플레이리스트에서 영상 6개 가져오기
- 3개씩 2페이지로 구성 (페이지네이션)
- 16:9 비율 썸네일 카드
- 좌/우 화살표로 페이지 전환
- 카드 클릭 시 모달로 영상 재생
- 로딩/에러 상태 처리

**배치 위치**: 추천 섹션(RecommendationSection) 다음

### B. 공연 상세 페이지: 검색 기반 관련 영상

**목적**: 각 공연에 대한 예고편/하이라이트 영상 자동 제공

**기능 상세**:
- 공연명으로 YouTube 검색 ("공연명 예고편", "공연명 하이라이트")
- 영상 발견 시(FOUND): 썸네일 + 모달 재생
- 영상 없을 시(NONE): 폴백 UI
  - "공식 영상 없음" 메시지
  - YouTube 검색 링크 버튼
  - 추천 플레이리스트 링크 버튼

**배치 위치**: Info 탭, 소개 이미지 다음

---

## 🏗️ 기술 스택 & 구조

### 백엔드 (Django + DRF)

**언어/프레임워크**:
- Python 3.x
- Django 5.2.8
- Django REST Framework
- requests (HTTP 라이브러리)

**캐시 전략**:
- 플레이리스트: 1시간 캐시 (모델 기반)
- 공연별 영상: 24시간 캐시 (모델 기반)
- Django LocMemCache 사용

### 프론트엔드 (Vue 3)

**언어/프레임워크**:
- Vue 3 (Composition API + `<script setup>`)
- Pinia (상태 관리 - 사용 안 함, 단순 API 호출)
- Axios (HTTP 클라이언트)

**스타일링**:
- Scoped CSS
- Tailwind 팔레트 기반 색상
- 그라데이션 배경 (Indigo → Purple)
- 반응형 디자인 (모바일/태블릿 대응)

---

## 📂 파일 구조

### 백엔드 파일

```
back/
├── .env                                    # 환경 변수 (API 키 추가)
├── mypjt/
│   └── settings.py                         # CACHES 설정 추가
├── performances/
│   ├── models.py                           # YouTubeVideoCache 모델 추가
│   ├── api_views.py                        # YouTube 액션 2개 추가
│   ├── youtube_service.py                  # 신규: YouTube API 서비스 로직
│   └── migrations/
│       └── 0005_youtubevideocache.py       # 자동 생성된 마이그레이션
```

### 프론트엔드 파일

```
front/
├── src/
│   ├── api/
│   │   └── youtube.js                                      # 신규: YouTube API 모듈
│   ├── components/
│   │   ├── YouTube/
│   │   │   ├── YouTubeModal.vue                           # 신규: 영상 재생 모달
│   │   │   └── YouTubePlaylistSection.vue                 # 신규: 메인 페이지 섹션
│   │   └── PerformanceDetail/
│   │       └── YouTubeVideoSection.vue                    # 신규: 상세 페이지 섹션
│   └── views/
│       ├── LandingView.vue                                 # 수정: YouTube 섹션 추가
│       └── PerformanceDetailView.vue                       # 수정: YouTube 섹션 추가
```

---

## 🔧 구현 상세

### 1. 백엔드 구현

#### 1.1 환경 변수 (.env)

```env
# YouTube API 설정
YOUTUBE_API_KEY=AIzaSyDSW-NnRulNrCyGG0bnP1qEKa1nv7zeFQ4
YOUTUBE_PLAYLIST_ID_MAIN=PLv_Yl-rq-62pyQ0wKHHRsjPZ7KCWMqsxL
```

**보안 주의사항**:
- API 키는 절대 프론트엔드에 노출하지 않음
- .env 파일은 .gitignore에 포함되어야 함
- 배포 시 환경변수로 관리

#### 1.2 캐시 설정 (settings.py)

```python
# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'youtube-cache',
    }
}
```

**특징**:
- 개발 환경: LocMemCache (메모리 기반)
- 배포 환경: Redis로 교체 가능 (향후)

#### 1.3 데이터베이스 모델 (models.py)

```python
class YouTubeVideoCache(models.Model):
    """YouTube video cache for performances and playlists"""

    # For performance-specific videos (nullable)
    performance = models.OneToOneField(
        Performance,
        on_delete=models.CASCADE,
        related_name='youtube_cache',
        null=True,
        blank=True,
        verbose_name="공연"
    )

    # For playlist or other cached queries (e.g., "playlist:main")
    cache_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="캐시 키"
    )

    # Video status: FOUND or NONE
    status = models.CharField(
        max_length=10,
        choices=[('FOUND', '발견'), ('NONE', '없음')],
        verbose_name="상태"
    )

    # Video data JSON
    video_data = models.JSONField(
        verbose_name="영상 데이터",
        help_text="List of videos or single video object"
    )

    # Fallback data for NONE status
    fallback_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name="대체 데이터"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "YouTube 영상 캐시"
        verbose_name_plural = "YouTube 영상 캐시 목록"
        indexes = [
            models.Index(fields=['cache_key']),
            models.Index(fields=['updated_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(performance__isnull=False) | models.Q(cache_key__isnull=False),
                name='either_performance_or_cache_key'
            )
        ]

    def is_fresh(self, max_age_hours=24):
        """Check if cache is still valid"""
        from django.utils import timezone
        from datetime import timedelta
        age = timezone.now() - self.updated_at
        return age < timedelta(hours=max_age_hours)
```

**설계 특징**:
- `performance`와 `cache_key` 중 하나는 반드시 존재 (제약 조건)
- `performance`: 공연별 영상 캐시
- `cache_key`: 플레이리스트 등 공통 캐시 (예: "playlist:main")
- `is_fresh()`: 캐시 유효성 검사 메서드

#### 1.4 YouTube 서비스 로직 (youtube_service.py)

**주요 함수**:

##### `get_playlist_videos(max_results=6)`
- YouTube Playlist Items API 호출
- 1시간 캐시
- 실패 시 캐시된 데이터 반환

```python
def get_playlist_videos(max_results=6):
    """Fetch videos from YouTube playlist"""
    if not YOUTUBE_API_KEY or not YOUTUBE_PLAYLIST_ID:
        return []

    # Check cache (1 hour)
    cache_obj, created = YouTubeVideoCache.objects.get_or_create(
        cache_key='playlist:main',
        defaults={'status': 'NONE', 'video_data': {'videos': []}}
    )

    if not created and cache_obj.is_fresh(max_age_hours=1):
        return cache_obj.video_data.get('videos', [])

    # Call YouTube API...
```

##### `search_performance_video(performance_name)`
- YouTube Search API 호출
- 다중 검색 쿼리 시도:
  1. "{공연명} 예고편"
  2. "{공연명} 하이라이트"
  3. "{공연명} 공연"
- 필터: `videoEmbeddable=true`, `safeSearch=strict`

##### `get_performance_video(performance_id)`
- 공연별 영상 조회/캐싱
- 24시간 캐시
- FOUND/NONE 상태 반환

**API 응답 구조**:

```python
# Playlist 응답
{
    "success": True,
    "videos": [
        {
            "videoId": "Z22JuE3b2is",
            "title": "[킹키부츠] 강홍석 롤라...",
            "channelTitle": "Jaeho",
            "publishedAt": "2025-12-21T11:23:00Z",
            "thumbnailUrl": "https://i.ytimg.com/vi/.../hqdefault.jpg",
            "youtubeUrl": "https://www.youtube.com/watch?v=..."
        },
        # ... 5 more videos
    ],
    "count": 6
}

# Performance Video - FOUND
{
    "status": "FOUND",
    "videoId": "abc123",
    "title": "공연 예고편",
    "channelTitle": "공식채널",
    "thumbnailUrl": "https://...",
    "youtubeUrl": "https://..."
}

# Performance Video - NONE
{
    "status": "NONE",
    "youtubeSearchUrl": "https://www.youtube.com/results?search_query=...",
    "fallbackPlaylistUrl": "https://www.youtube.com/playlist?list=..."
}
```

#### 1.5 API 엔드포인트 (api_views.py)

```python
# PerformanceViewSet 클래스 내부에 추가

@action(detail=False, methods=['get'], url_path='youtube/playlist')
def youtube_playlist(self, request):
    """
    Get YouTube playlist videos for main page
    GET /api/performances/youtube/playlist/
    """
    from .youtube_service import get_playlist_videos

    videos = get_playlist_videos(max_results=6)

    return Response({
        'success': True,
        'videos': videos,
        'count': len(videos)
    })

@action(detail=True, methods=['get'], url_path='youtube')
def youtube_video(self, request, pk=None):
    """
    Get performance-related YouTube video
    GET /api/performances/{id}/youtube/
    """
    from .youtube_service import get_performance_video

    result = get_performance_video(pk)
    return Response(result)
```

**URL 패턴**:
- `GET /api/performances/youtube/playlist/` - 플레이리스트 조회
- `GET /api/performances/{id}/youtube/` - 공연별 영상 조회

**중요 버그 수정**:
- 초기에 `BoxOfficeRankingViewSet`에 잘못 추가되어 404 에러 발생
- `PerformanceViewSet`로 이동하여 해결

---

### 2. 프론트엔드 구현

#### 2.1 API 모듈 (youtube.js)

```javascript
import apiClient from './axios'

export default {
  getPlaylistVideos() {
    return apiClient.get('/performances/youtube/playlist/')
  },

  getPerformanceVideo(performanceId) {
    return apiClient.get(`/performances/${performanceId}/youtube/`)
  }
}
```

**특징**:
- axios 인스턴스 재사용 (JWT 자동 주입)
- 에러 처리는 컴포넌트에서 담당

#### 2.2 YouTube 모달 컴포넌트 (YouTubeModal.vue)

**기능**:
- Teleport를 사용한 body 레벨 모달
- YouTube iframe 자동재생
- ESC 키 / 외부 클릭으로 닫기
- 16:9 비율 유지

**주요 코드**:

```vue
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="modal-overlay" @click="handleClose">
        <div class="modal-container" @click.stop>
          <button class="close-button" @click="handleClose">
            <i class="fas fa-times"></i>
          </button>
          <div class="video-wrapper">
            <iframe
              :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  videoId: String
})

const emit = defineEmits(['close'])

// ESC key handler
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.show) {
    emit('close')
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})
</script>
```

#### 2.3 플레이리스트 섹션 (YouTubePlaylistSection.vue)

**레이아웃**:
- 3개 영상 × 2페이지 (총 6개)
- 좌우 화살표 네비게이션
- 반응형 그리드 (데스크탑 3열, 태블릿 2열, 모바일 1열)

**주요 기능**:

```vue
<script setup>
const videos = ref([])
const loading = ref(false)
const error = ref(null)

// Pagination
const currentPage = ref(0)
const itemsPerPage = 3

// Computed
const displayedVideos = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return videos.value.slice(start, end)
})

const canGoPrev = computed(() => currentPage.value > 0)
const canGoNext = computed(() => currentPage.value < totalPages.value - 1)

// Methods
const goToPrevPage = () => {
  if (canGoPrev.value) currentPage.value--
}

const goToNextPage = () => {
  if (canGoNext.value) currentPage.value++
}

const openModal = (videoId) => {
  selectedVideoId.value = videoId
  showModal.value = true
}

const loadVideos = async () => {
  loading.value = true
  try {
    const response = await youtubeAPI.getPlaylistVideos()
    videos.value = response.data.videos || []
  } catch (err) {
    error.value = '영상을 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>
```

**스타일 특징**:
- YouTube 빨간색 (#ff0000) 강조
- 호버 시 썸네일 확대 (scale 1.1)
- Play 오버레이 애니메이션

**커스터마이징**:
- 채널명 대신 **"PlayPick 추천"** 고정 텍스트 표시

#### 2.4 공연 영상 섹션 (YouTubeVideoSection.vue)

**조건부 렌더링**:
1. `loading`: 로딩 스피너
2. `status === 'FOUND'`: 영상 카드 + 재생 버튼
3. `status === 'NONE'`: 폴백 UI (검색 링크 + 플레이리스트 링크)

**폴백 UI**:

```vue
<div v-else-if="status === 'NONE'" class="no-video">
  <div class="no-video-icon">
    <i class="fas fa-video-slash"></i>
  </div>
  <p class="no-video-text">공식 영상이 없습니다</p>
  <div class="fallback-links">
    <a :href="fallbackData.youtubeSearchUrl" target="_blank" class="fallback-button">
      <i class="fab fa-youtube"></i>
      YouTube에서 검색
    </a>
    <a :href="fallbackData.fallbackPlaylistUrl" target="_blank" class="fallback-button secondary">
      <i class="fas fa-list"></i>
      추천 플레이리스트
    </a>
  </div>
</div>
```

#### 2.5 뷰 통합

**LandingView.vue**:
```vue
<div class="landing-content">
  <RecommendationSection />
  <YouTubePlaylistSection />  <!-- 추가됨 -->
  <AllRankingSection />
  <GenreRankingSection />
</div>

<script setup>
import YouTubePlaylistSection from '@/components/YouTube/YouTubePlaylistSection.vue'
</script>
```

**PerformanceDetailView.vue**:
```vue
<div v-show="activeTab === 'info'" class="tab-pane">
  <!-- 기존 정보들 -->
  <div v-if="currentPerformance.intro_images?.length" class="section-card">
    <!-- 소개 이미지 -->
  </div>

  <!-- YouTube 관련 영상 (추가됨) -->
  <YouTubeVideoSection :performanceId="route.params.id" />
</div>

<script setup>
import YouTubeVideoSection from '@/components/PerformanceDetail/YouTubeVideoSection.vue'
</script>
```

---

## 🐛 트러블슈팅

### 문제 1: 404 Not Found 에러

**증상**:
```
GET http://127.0.0.1:8000/api/performances/youtube/playlist/
Status: 404 Not Found
```

**원인**:
- YouTube 액션들이 `BoxOfficeRankingViewSet`에 잘못 추가됨
- 라우팅이 `/api/boxoffice/youtube/playlist/`로 연결됨

**해결**:
```python
# 잘못된 위치 (BoxOfficeRankingViewSet)
class BoxOfficeRankingViewSet(viewsets.ReadOnlyModelViewSet):
    @action(detail=False, methods=['get'], url_path='youtube/playlist')
    def youtube_playlist(self, request):
        # ...

# 올바른 위치 (PerformanceViewSet)
class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    @action(detail=False, methods=['get'], url_path='youtube/playlist')
    def youtube_playlist(self, request):
        # ...
```

**확인 방법**:
```bash
python -c "
from django.urls import get_resolver
resolver = get_resolver()
# URL 패턴 확인
"
```

### 문제 2: Vue 컴파일 에러 - Element is missing end tag

**증상**:
```
[plugin:vite-plugin-vue-inspector] Element is missing end tag.
PerformanceDetailView.vue
```

**원인**:
- 소개 이미지 section-card의 닫는 `</div>` 태그 누락
- YouTube 섹션 추가 시 HTML 구조가 깨짐

**해결**:
```vue
<!-- 수정 전 -->
          </div>

        <!-- YouTube 관련 영상 -->
        <YouTubeVideoSection :performanceId="route.params.id" />
          </div>

<!-- 수정 후 -->
          </div>
        </div>  <!-- section-card 닫는 태그 추가 -->

        <!-- YouTube 관련 영상 -->
        <YouTubeVideoSection :performanceId="route.params.id" />
          </div>
```

### 문제 3: 채널명 표시 이슈

**요구사항**:
- YouTube API에서 받은 `channelTitle` 대신 고정 텍스트 표시

**해결**:
```vue
<!-- 수정 전 -->
<p class="video-channel">{{ video.channelTitle }}</p>

<!-- 수정 후 -->
<p class="video-channel">PlayPick 추천</p>
```

**적용 파일**:
- `YouTubePlaylistSection.vue`
- `YouTubeVideoSection.vue`

---

## ✅ 테스트 체크리스트

### 백엔드 테스트

- [x] `.env`에 YouTube API 키가 올바르게 설정됨
- [x] 마이그레이션이 성공적으로 적용됨
- [x] `GET /api/performances/youtube/playlist/`가 6개 영상 반환
- [x] `GET /api/performances/{id}/youtube/`가 FOUND/NONE 상태 반환
- [x] 캐시가 정상 작동 (재요청 시 빠른 응답)
- [x] 플레이리스트 캐시 1시간 지속
- [x] 공연 영상 캐시 24시간 지속

### 프론트엔드 테스트

- [x] 메인 페이지에 YouTube 섹션 표시
- [x] 3개 영상 × 2페이지 네비게이션 작동
- [x] 영상 클릭 시 모달로 재생
- [x] 모달 닫기 (X 버튼, ESC, 외부 클릭) 작동
- [x] 공연 상세 페이지에 영상 섹션 표시
- [x] FOUND 상태: 썸네일 + 모달 재생
- [x] NONE 상태: 폴백 링크 표시
- [x] 콘솔 에러 없음
- [x] 반응형 디자인 작동 (모바일/태블릿)

### 엣지 케이스

- [x] API 키 없을 때: 빈 배열 반환
- [x] 플레이리스트 없을 때: 빈 상태 메시지
- [x] 네트워크 에러: 에러 메시지 표시
- [x] 잘못된 performance ID: NONE 상태 반환
- [x] 임베드 불가 영상: 검색 필터로 제외

---

## 📊 성능 최적화

### 캐싱 전략

**플레이리스트 (1시간)**:
- 이유: 자주 변경되지 않음, 모든 사용자가 동일한 데이터 조회
- 효과: API 쿼터 절약 (10,000/일 제한)

**공연별 영상 (24시간)**:
- 이유: 검색 결과가 자주 바뀌지 않음
- 효과: 각 공연당 1회만 검색

### API 쿼터 관리

**YouTube Data API v3 무료 할당량**: 10,000 units/day

**비용 계산**:
- Playlist items list: 1 unit
- Search: 100 units

**예상 사용량** (캐시 적용 시):
- 플레이리스트: 24회/일 (1시간마다) = 24 units
- 공연 검색: 공연당 1회/일, 100개 공연 가정 = 10,000 units
- **총합**: ~10,024 units (거의 한계치)

**권장사항**:
- 배포 환경에서는 Redis 캐시로 전환
- 캐시 TTL 조정 (플레이리스트: 12시간, 공연: 7일)
- 검색 쿼리 최적화 (한 번에 3개 시도 → 1개로 축소)

### 프론트엔드 최적화

**Lazy Loading**:
- 모달 iframe은 모달 열릴 때만 로드
- 썸네일 이미지만 미리 로드

**컴포넌트 분리**:
- YouTubeModal: 재사용 가능한 독립 컴포넌트
- 메인/상세 섹션: 독립적으로 로드 가능

---

## 🚀 배포 가이드

### 환경 변수 설정

**개발 환경** (.env):
```env
YOUTUBE_API_KEY=AIzaSy...
YOUTUBE_PLAYLIST_ID_MAIN=PLv_Yl-...
```

**배포 환경** (환경 변수):
```bash
export YOUTUBE_API_KEY="AIzaSy..."
export YOUTUBE_PLAYLIST_ID_MAIN="PLv_Yl-..."
```

### 데이터베이스 마이그레이션

```bash
# 개발 환경
cd back
python manage.py migrate

# 배포 환경
python manage.py migrate --no-input
```

### 캐시 설정 (Redis 사용 시)

**settings.py** (배포 환경):
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**requirements.txt**:
```
django-redis==5.2.0
redis==4.5.5
```

### 프론트엔드 빌드

```bash
cd front
npm run build
```

빌드 결과물: `front/dist/`

---

## 🔐 보안 고려사항

### API 키 보호

**✅ 올바른 방법**:
- 백엔드 .env 파일에만 저장
- 프론트엔드에 노출 금지
- Git에 커밋 금지 (.gitignore 확인)

**❌ 잘못된 방법**:
- 프론트엔드 환경 변수에 저장 (VITE_YOUTUBE_API_KEY 등)
- 클라이언트 사이드 코드에 하드코딩

### CORS 설정

현재 설정:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

배포 시:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

### Rate Limiting

**권장사항**:
- DRF Throttling 추가
- 플레이리스트: 100 requests/hour
- 공연 영상: 1000 requests/hour

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## 📈 향후 개선 사항

### 기능 확장

1. **자동 플레이리스트 큐레이션**
   - 장르별 플레이리스트 (뮤지컬, 연극, 콘서트 등)
   - 사용자 선호도 기반 추천

2. **영상 품질 선택**
   - 썸네일 해상도 옵션 (medium/high/maxres)
   - 재생 품질 설정

3. **영상 메타데이터 확장**
   - 조회수, 좋아요 수 표시
   - 업로드 날짜 표시

4. **소셜 기능**
   - 영상 공유 버튼
   - 영상에 대한 댓글/리뷰

### 성능 개선

1. **CDN 활용**
   - 썸네일 이미지 CDN 캐싱
   - YouTube 임베드 스크립트 최적화

2. **Progressive Loading**
   - 첫 페이지만 먼저 로드
   - 두 번째 페이지는 지연 로드

3. **에러 복구**
   - API 실패 시 재시도 로직
   - 폴백 썸네일 이미지

### 분석 & 모니터링

1. **사용자 행동 분석**
   - 어떤 영상이 많이 클릭되는지
   - 평균 재생 시간

2. **API 사용량 모니터링**
   - 일별 쿼터 사용량 추적
   - 알림 설정 (80% 도달 시)

3. **에러 로깅**
   - Sentry 통합
   - YouTube API 에러 추적

---

## 📞 문의 및 지원

### 문제 발생 시

1. **404 에러**: URL 라우팅 확인
2. **403 에러**: API 키 유효성 확인
3. **캐시 문제**: DB에서 YouTubeVideoCache 테이블 확인

### 디버깅 명령어

```bash
# URL 패턴 확인
python manage.py show_urls | grep youtube

# 캐시 확인
python manage.py shell
>>> from performances.models import YouTubeVideoCache
>>> YouTubeVideoCache.objects.all()

# API 테스트
curl http://127.0.0.1:8000/api/performances/youtube/playlist/
```

---

## 📝 변경 이력

| 날짜 | 버전 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 2025-12-21 | 1.0.0 | 초기 구현 완료 | Claude |
| 2025-12-21 | 1.0.1 | 404 에러 수정 (ViewSet 위치 변경) | Claude |
| 2025-12-21 | 1.0.2 | Vue 컴파일 에러 수정 (닫는 태그) | Claude |
| 2025-12-21 | 1.0.3 | 채널명 → "PlayPick 추천" 변경 | Claude |

---

## 🎓 학습 자료

### YouTube Data API v3

- [공식 문서](https://developers.google.com/youtube/v3/docs)
- [Playlist Items API](https://developers.google.com/youtube/v3/docs/playlistItems/list)
- [Search API](https://developers.google.com/youtube/v3/docs/search/list)

### Vue 3 Composition API

- [공식 가이드](https://vuejs.org/guide/introduction.html)
- [Script Setup](https://vuejs.org/api/sfc-script-setup.html)
- [Teleport](https://vuejs.org/guide/built-ins/teleport.html)

### Django REST Framework

- [공식 문서](https://www.django-rest-framework.org/)
- [ViewSet Actions](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)
- [Routers](https://www.django-rest-framework.org/api-guide/routers/)

---

**작성일**: 2025-12-21
**마지막 업데이트**: 2025-12-21
**문서 버전**: 1.0.3
