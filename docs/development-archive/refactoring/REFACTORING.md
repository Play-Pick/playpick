# 🔄 Vue 3 프로젝트 리팩토링 가이드

> 작성일: 2024-12-14
> 작업 내용: LandingView, PerformanceListView, PerformanceDetailView 리팩토링

---

## 📋 목차

1. [리팩토링 개요](#리팩토링-개요)
2. [변경 사항 상세](#변경-사항-상세)
3. [Composable vs Store 개념](#composable-vs-store-개념)
4. [개선 가능한 TODO 리스트](#개선-가능한-todo-리스트)

---

## 🎯 리팩토링 개요

### 목적
- Vue 3 권장 패턴인 **Composition API + SFC(Single File Component)** 구조로 전환
- 비즈니스 로직과 UI 분리로 **재사용성 및 유지보수성 향상**
- **관심사의 분리(Separation of Concerns)** 원칙 적용

### 핵심 원칙
1. **컴포넌트**: UI 렌더링만 담당
2. **Composable**: 재사용 가능한 로직
3. **API**: 서버 통신
4. **View**: 페이지 레벨 구성

---

## 📊 변경 사항 상세

### 1. LandingView 리팩토링

#### Before (253줄)
```vue
<template>
  <div class="landing-container">
    <!-- 장르 탭 직접 구현 -->
    <div class="genre-tabs-container">
      <div class="genre-tabs">
        <button v-for="genre in genres" ...>
          {{ genre.name }}
        </button>
      </div>
    </div>

    <!-- 공연 카드 직접 구현 -->
    <div class="performances-grid">
      <router-link v-for="perf in pageData" ...>
        <div class="card-poster">
          <img :src="perf.poster" ... />
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const currentGenre = ref('BBBC')
const allPerformances = ref([])
const currentPage = ref(0)
const loading = ref(false)
const error = ref(null)

// 모든 비즈니스 로직이 View에 섞여있음
const loadBoxOffice = async (genre) => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:8000/performances/boxoffice-genre/', {
      params: { genre }
    })
    // ...
  } catch (err) {
    error.value = '오류가 발생했습니다.'
  }
}

const changeGenre = (genre) => {
  currentGenre.value = genre
  currentPage.value = 0
  loadBoxOffice(genre)
}

const prevPage = () => { /* ... */ }
const nextPage = () => { /* ... */ }
</script>
```

#### After (55줄, **78% 감소**)
```vue
<template>
  <div class="landing-container">
    <div class="landing-content">
      <div class="header">
        <h1 class="title">
          <i class="fas fa-fire"></i> 인기 공연 랭킹
        </h1>
        <p class="subtitle">
          KOPIS 예매상황판 기준 <span class="date">{{ latestDate }}</span> 업데이트
        </p>
      </div>

      <!-- 장르 탭 컴포넌트 -->
      <GenreTab
        :genres="genres"
        :currentGenre="genre"
        @change="changeGenre"
      />

      <!-- 공연 캐러셀 컴포넌트 -->
      <BoxOfficeCarousel />

      <!-- 전체 공연 보기 버튼 -->
      <div class="view-all-container">
        <router-link to="/performances" class="view-all-button">
          <span>전체 공연 목록 보기</span>
          <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useBoxOffice } from '@/composables/useBoxOffice'
import BoxOfficeCarousel from '@/components/BoxOffice/BoxOfficeCarousel.vue'
import GenreTab from '@/components/BoxOffice/GenreTab.vue'

// 장르 목록
const genres = [
  { code: 'BBBC', name: '뮤지컬' },
  { code: 'AAAA', name: '연극' },
  // ...
]

// useBoxOffice composable 사용 (비즈니스 로직 분리)
const { genre, latestDate, changeGenre } = useBoxOffice()
</script>
```

#### 생성된 파일들

**1. components/BoxOffice/BoxOfficeCard.vue** (230줄)
- 개별 공연 카드 UI
- 순위 뱃지, 포스터 이미지, 공연 정보 표시
- 날짜 포맷팅, 이미지 에러 처리

**2. components/BoxOffice/BoxOfficeCarousel.vue** (229줄)
- 공연 목록 캐러셀
- 로딩/에러 상태 처리
- 좌우 네비게이션 화살표
- 페이지 인디케이터

**3. components/BoxOffice/GenreTab.vue** (83줄)
- 장르 선택 탭 UI
- 장르 변경 이벤트 emit

**4. composables/useBoxOffice.js** (93줄)
- 박스오피스 데이터 관리 로직
- 장르 선택, 페이지네이션
- API 호출 및 상태 관리

---

### 2. PerformanceListView 리팩토링

#### Before (156줄)
```vue
<template>
  <div class="performance-list">
    <h1>공연 목록</h1>

    <!-- 필터 UI 직접 구현 -->
    <div class="filters">
      <select v-model="selectedGenre" @change="filterPerformances">
        <option value="">전체 장르</option>
        <option v-for="genre in genres" :key="genre" :value="genre">
          {{ genre }}
        </option>
      </select>
      <input v-model="searchQuery" @input="filterPerformances" ... />
    </div>

    <!-- 공연 카드 직접 구현 -->
    <div class="performances-grid">
      <div
        v-for="performance in performances"
        :key="performance.mt20id"
        class="performance-card"
        @click="goToDetail(performance.mt20id)"
      >
        <img :src="performance.poster" ... />
        <h3>{{ performance.prfnm }}</h3>
        <p>{{ performance.fcltynm }}</p>
        <!-- ... -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePerformanceStore } from '@/stores/performanceStore'
import { storeToRefs } from 'pinia'

const router = useRouter()
const performanceStore = usePerformanceStore()
const { performances, genres, loading, error } = storeToRefs(performanceStore)

const selectedGenre = ref('')
const searchQuery = ref('')

const filterPerformances = async () => {
  const params = {}
  if (selectedGenre.value) params.genrenm = selectedGenre.value
  if (searchQuery.value) params.search = searchQuery.value
  await performanceStore.fetchPerformances(params)
}

const goToDetail = (id) => {
  router.push({ name: 'performance-detail', params: { id } })
}

onMounted(async () => {
  await performanceStore.fetchGenres()
  await performanceStore.fetchPerformances()
})
</script>
```

#### After (60줄, **61% 감소**)
```vue
<template>
  <div class="performance-list">
    <div class="header">
      <h1>
        <i class="fas fa-theater-masks"></i> 공연 목록
      </h1>
      <p class="subtitle">다양한 공연 정보를 확인하세요</p>
    </div>

    <!-- 필터 컴포넌트 -->
    <PerformanceFilters
      v-model:selectedGenre="selectedGenre"
      v-model:searchQuery="searchQuery"
      :genres="genres"
      @filter="filterPerformances"
    />

    <!-- 로딩 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <!-- 공연 목록 그리드 -->
    <PerformanceGrid
      v-else
      :performances="performances"
      @card-click="goToDetail"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { usePerformanceList } from '@/composables/usePerformanceList'
import PerformanceFilters from '@/components/Performance/PerformanceFilters.vue'
import PerformanceGrid from '@/components/Performance/PerformanceGrid.vue'

const router = useRouter()

const {
  performances,
  genres,
  loading,
  error,
  selectedGenre,
  searchQuery,
  filterPerformances
} = usePerformanceList()

const goToDetail = (id) => {
  router.push({ name: 'performance-detail', params: { id } })
}
</script>
```

#### 생성된 파일들

**1. components/Performance/PerformanceCard.vue** (94줄)
- 개별 공연 카드
- 포스터, 제목, 장소, 날짜 표시

**2. components/Performance/PerformanceFilters.vue** (94줄)
- 장르 선택, 검색 필터 UI
- v-model을 통한 양방향 바인딩

**3. components/Performance/PerformanceGrid.vue** (35줄)
- 공연 카드 그리드 레이아웃
- 카드 클릭 이벤트 처리

**4. composables/usePerformanceList.js** (44줄)
- 공연 목록 필터링 로직
- Pinia store와 연동

---

### 3. PerformanceDetailView 리팩토링

#### Before (699줄)
```vue
<template>
  <div class="performance-detail">
    <div v-else-if="currentPerformance" class="detail-content">
      <!-- 헤더 섹션 직접 구현 (100줄+) -->
      <div class="header-section">
        <img :src="currentPerformance.poster" ... />
        <div class="info-section">
          <h1>{{ currentPerformance.prfnm }}</h1>
          <div class="info-grid">
            <div v-if="currentPerformance.genrenm" class="info-item">
              <!-- ... 많은 정보 항목들 ... -->
            </div>
          </div>
          <div v-if="currentPerformance.detail?.relates?.length" class="booking-section">
            <!-- ... 예매 링크들 ... -->
          </div>
        </div>
      </div>

      <!-- 카카오맵 모달 직접 구현 (50줄+) -->
      <div v-if="showMapModal" class="map-modal" @click="closeMapModal">
        <div class="map-modal-content" @click.stop>
          <div class="modal-header">
            <h3>{{ currentPerformance?.fcltynm }}</h3>
            <button @click="closeMapModal" class="close-btn">×</button>
          </div>
          <div id="map" class="map-container"></div>
        </div>
      </div>

      <!-- ... 기타 상세 정보들 ... -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePerformanceStore } from '@/stores/performanceStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const performanceStore = usePerformanceStore()
const { currentPerformance, loading, error } = storeToRefs(performanceStore)

const showMapModal = ref(false)
let map = null
let geocoder = null

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY

// 카카오 맵 스크립트 로드 (40줄+)
const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&libraries=services&autoload=false`
    // ... 많은 설정 코드 ...
  })
}

// 지도 초기화 (60줄+)
const initMap = () => {
  const mapContainer = document.getElementById('map')
  const mapOption = {
    center: new window.kakao.maps.LatLng(37.5665, 126.978),
    level: 3,
  }
  map = new window.kakao.maps.Map(mapContainer, mapOption)
  geocoder = new window.kakao.maps.services.Geocoder()
  // ... 많은 지도 설정 코드 ...
}

const openMapModal = async () => { /* ... */ }
const closeMapModal = () => { /* ... */ }
const goBack = () => { /* ... */ }
const goHome = () => { /* ... */ }

onMounted(async () => {
  const id = route.params.id
  await performanceStore.fetchPerformance(id)
})
</script>
```

#### After (189줄, **73% 감소**)
```vue
<template>
  <div class="performance-detail">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <div v-else-if="currentPerformance" class="detail-content">
      <!-- 공연 기본 정보 (컴포넌트로 분리) -->
      <HeaderSection
        :performance="currentPerformance"
        @open-map="handleOpenMap"
      />

      <!-- 상세 정보들 (View에 유지) -->
      <div v-if="currentPerformance.detail">
        <div v-if="currentPerformance.detail.sty" class="section-card">
          <h2><i class="fas fa-book-open"></i> 줄거리</h2>
          <p class="description">{{ currentPerformance.detail.sty }}</p>
        </div>
        <!-- ... 기타 섹션들 ... -->
      </div>

      <!-- 액션 버튼 -->
      <div class="actions">
        <button @click="goBack" class="btn-back">
          <i class="fas fa-list"></i> 전체 공연 목록
        </button>
        <button @click="goHome" class="btn-home">
          <i class="fas fa-home"></i> 홈으로
        </button>
      </div>
    </div>

    <!-- 카카오맵 모달 (컴포넌트로 분리) -->
    <MapModal
      :show="showMapModal"
      :venueName="currentPerformance?.fcltynm"
      @close="closeMapModal"
    />
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { usePerformanceDetail } from '@/composables/usePerformanceDetail'
import { useKakaoMap } from '@/composables/useKakaoMap'
import HeaderSection from '@/components/PerformanceDetail/HeaderSection.vue'
import MapModal from '@/components/PerformanceDetail/MapModal.vue'

const { currentPerformance, loading, error, goBack, goHome } = usePerformanceDetail()
const { showMapModal, openMapModal, closeMapModal, initMap } = useKakaoMap()

const handleOpenMap = async () => {
  await openMapModal()
  setTimeout(() => {
    if (currentPerformance.value?.fcltynm) {
      initMap(currentPerformance.value.fcltynm)
    }
  }, 150)
}

// 맵 모달이 열릴 때 지도 초기화
watch(showMapModal, (newVal) => {
  if (newVal && currentPerformance.value?.fcltynm) {
    setTimeout(() => {
      initMap(currentPerformance.value.fcltynm)
    }, 150)
  }
})
</script>
```

#### 생성된 파일들

**1. components/PerformanceDetail/HeaderSection.vue** (295줄)
- 포스터 + 기본 정보 섹션
- 예매 링크 섹션
- 지도 열기 이벤트 emit

**2. components/PerformanceDetail/MapModal.vue** (90줄)
- 카카오맵 모달 UI
- 모달 열기/닫기 처리

**3. composables/usePerformanceDetail.js** (33줄)
- 공연 상세 데이터 로딩
- 네비게이션 함수 (goBack, goHome)

**4. composables/useKakaoMap.js** (130줄)
- 카카오맵 스크립트 로딩
- 지도 초기화 및 마커 표시
- 주소/키워드 검색

---

### 4. API 구조 통합

#### Before (중복된 구조)
```
src/
├── api/
│   ├── performances.js    # 기존 API
│   ├── auth.js
│   └── ...
└── services/              # 🔴 중복!
    └── performanceApi.js  # 같은 역할
```

#### After (통합된 구조)
```
src/
├── api/                   # ✅ 모든 API 통합
│   ├── axios.js          # axios 설정
│   ├── performances.js   # 공연 API (boxOffice 포함)
│   ├── auth.js           # 인증 API
│   ├── community.js      # 커뮤니티 API
│   └── users.js          # 유저 API
├── composables/          # 재사용 로직
├── components/           # UI 컴포넌트
└── views/                # 페이지
```

**변경 내용:**
1. `services/performanceApi.js` 삭제
2. `api/performances.js`에 `getBoxOfficeByGenre()` 추가
3. `useBoxOffice.js`의 import 경로 수정
   ```javascript
   // Before
   import { fetchBoxOfficeByGenre } from '@/services/performanceApi'

   // After
   import performanceApi from '@/api/performances'
   // 사용: performanceApi.getBoxOfficeByGenre(genre)
   ```

---

## 🧩 Composable vs Store 개념

### Composable이란?

**Composable**은 Vue 3 Composition API를 활용한 **재사용 가능한 로직**입니다.

```javascript
// composables/useCounter.js
import { ref } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return {
    count,
    increment,
    decrement
  }
}
```

**사용:**
```vue
<script setup>
import { useCounter } from '@/composables/useCounter'

// 각 컴포넌트마다 독립적인 인스턴스
const { count, increment, decrement } = useCounter(10)
</script>
```

### Store (Pinia)란?

**Store**는 **전역 상태 관리**를 위한 중앙 저장소입니다.

```javascript
// stores/counterStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return {
    count,
    increment,
    decrement
  }
})
```

**사용:**
```vue
<script setup>
import { useCounterStore } from '@/stores/counterStore'

// 모든 컴포넌트가 같은 상태 공유
const counterStore = useCounterStore()
</script>
```

### 핵심 차이점

| 특성 | Composable | Store (Pinia) |
|------|-----------|---------------|
| **상태 범위** | 컴포넌트 로컬 (독립적) | 전역 (공유됨) |
| **인스턴스** | 호출할 때마다 새 인스턴스 | 싱글톤 (단일 인스턴스) |
| **사용 목적** | 재사용 가능한 로직 | 전역 상태 관리 |
| **데이터 공유** | ❌ 공유 안 됨 | ✅ 모든 컴포넌트가 공유 |
| **DevTools** | ❌ 지원 안 됨 | ✅ Vue DevTools 지원 |
| **SSR** | ✅ 자동 지원 | ✅ 자동 지원 |

### 실제 예제: 같은 기능, 다른 동작

#### Composable 예제
```vue
<!-- ComponentA.vue -->
<script setup>
import { useCounter } from '@/composables/useCounter'
const { count, increment } = useCounter(0)
// count: 0
</script>

<!-- ComponentB.vue -->
<script setup>
import { useCounter } from '@/composables/useCounter'
const { count, increment } = useCounter(0)
// count: 0 (독립적인 상태!)
</script>
```
👉 각 컴포넌트가 **독립적인 counter**를 가짐

#### Store 예제
```vue
<!-- ComponentA.vue -->
<script setup>
import { useCounterStore } from '@/stores/counterStore'
const store = useCounterStore()
store.increment() // count: 1
</script>

<!-- ComponentB.vue -->
<script setup>
import { useCounterStore } from '@/stores/counterStore'
const store = useCounterStore()
console.log(store.count) // count: 1 (공유됨!)
</script>
```
👉 모든 컴포넌트가 **같은 counter**를 공유

### 언제 무엇을 사용할까?

#### ✅ Composable을 사용하는 경우

1. **컴포넌트별 독립적인 로직**
   ```javascript
   // 각 폼마다 독립적인 유효성 검사
   useFormValidation()
   ```

2. **재사용 가능한 기능**
   ```javascript
   // 마우스 위치 추적 (각 컴포넌트마다 다름)
   useMouse()
   ```

3. **UI 관련 로직**
   ```javascript
   // 모달 열기/닫기 (각 모달마다 독립적)
   useModal()
   ```

4. **API 호출 + 로컬 상태**
   ```javascript
   // 특정 페이지의 데이터 페칭
   useBoxOffice()  // 우리 프로젝트 예시
   usePerformanceDetail()
   ```

#### ✅ Store를 사용하는 경우

1. **전역으로 공유해야 하는 상태**
   ```javascript
   // 현재 로그인한 사용자 정보
   useUserStore()
   ```

2. **여러 컴포넌트에서 동시에 접근**
   ```javascript
   // 장바구니 (어디서든 접근)
   useCartStore()
   ```

3. **앱 전체 설정**
   ```javascript
   // 테마, 언어 설정
   useSettingsStore()
   ```

4. **복잡한 상태 관리가 필요한 경우**
   ```javascript
   // 공연 목록 (필터, 검색, 페이지네이션 등)
   usePerformanceStore()  // 우리 프로젝트 예시
   ```

### 우리 프로젝트 적용 사례

#### useBoxOffice (Composable)
```javascript
// composables/useBoxOffice.js
export function useBoxOffice() {
  // 🔹 각 LandingView마다 독립적인 상태
  const genre = ref('BBBC')
  const currentPage = ref(0)
  const allPerformances = ref([])

  // 페이지 전환 시 상태 초기화됨
  return { genre, currentPage, ... }
}
```
**이유:** LandingView만 사용하는 로직이므로 Composable이 적합

#### usePerformanceStore (Store)
```javascript
// stores/performanceStore.js
export const usePerformanceStore = defineStore('performance', () => {
  // 🔹 전역으로 공유되는 상태
  const performances = ref([])
  const genres = ref([])
  const currentPerformance = ref(null)

  // 여러 컴포넌트에서 접근
  return { performances, genres, currentPerformance, ... }
})
```
**이유:** 여러 페이지에서 공연 데이터를 공유하므로 Store가 적합

### 혼합 사용 패턴

우리 프로젝트처럼 **Composable과 Store를 함께** 사용할 수 있습니다:

```javascript
// composables/usePerformanceList.js
export function usePerformanceList() {
  // Store에서 전역 상태 가져오기
  const performanceStore = usePerformanceStore()
  const { performances, genres, loading } = storeToRefs(performanceStore)

  // 로컬 필터 상태 (Composable)
  const selectedGenre = ref('')
  const searchQuery = ref('')

  // 로컬 로직
  const filterPerformances = async () => {
    await performanceStore.fetchPerformances({ ... })
  }

  return {
    // Store 상태
    performances,
    genres,
    loading,
    // Composable 상태
    selectedGenre,
    searchQuery,
    filterPerformances
  }
}
```

---

## 📝 개선 가능한 TODO 리스트

### 🔴 우선순위 높음 (Critical)

#### 1. 에러 처리 개선
**현재 문제:**
```javascript
// composables/useBoxOffice.js
catch (e) {
  console.error('Error:', e)
  error.value = '오류가 발생했습니다.'  // 너무 일반적
}
```

**개선 방안:**
```javascript
// utils/errorHandler.js
export function handleApiError(error) {
  if (error.response) {
    switch (error.response.status) {
      case 404:
        return '요청한 데이터를 찾을 수 없습니다.'
      case 500:
        return '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      case 401:
        return '인증이 필요합니다. 다시 로그인해주세요.'
      default:
        return `오류가 발생했습니다. (${error.response.status})`
    }
  }
  if (error.request) {
    return '네트워크 연결을 확인해주세요.'
  }
  return '알 수 없는 오류가 발생했습니다.'
}

// composables/useBoxOffice.js
import { handleApiError } from '@/utils/errorHandler'

catch (e) {
  console.error('Error:', e)
  error.value = handleApiError(e)
}
```

#### 2. 로딩 상태 중복 제거
**현재 문제:**
- 모든 View에서 동일한 로딩 스피너 코드 중복

**개선 방안:**
```vue
<!-- components/common/LoadingSpinner.vue -->
<template>
  <div class="loading-container">
    <div class="spinner"></div>
    <p class="loading-text">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: '로딩 중...'
  }
})
</script>
```

**사용:**
```vue
<template>
  <LoadingSpinner v-if="loading" />
  <ErrorMessage v-else-if="error" :message="error" />
  <div v-else>{{ content }}</div>
</template>
```

#### 3. 환경변수 검증
**현재 문제:**
```javascript
// composables/useKakaoMap.js
const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY
// API 키가 없어도 에러 없이 진행됨
```

**개선 방안:**
```javascript
// config/env.js
export const config = {
  kakaoMapApiKey: import.meta.env.VITE_KAKAO_MAP_API_KEY,
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL
}

// 앱 시작 시 검증
export function validateEnv() {
  const required = ['kakaoMapApiKey', 'apiBaseUrl']
  const missing = required.filter(key => !config[key])

  if (missing.length > 0) {
    throw new Error(`Missing environment variables: ${missing.join(', ')}`)
  }
}

// main.js
import { validateEnv } from '@/config/env'
validateEnv()  // 앱 시작 시 검증
```

---

### 🟡 우선순위 중간 (Important)

#### 4. TypeScript 도입
**현재 문제:**
- 타입 안정성 부족
- API 응답 타입 불명확

**개선 방안:**
```typescript
// types/performance.ts
export interface Performance {
  mt20id: string
  prfnm: string
  poster: string
  genrenm: string
  prfpdfrom: string
  prfpdto: string
  fcltynm: string
  prfstate: '공연중' | '공연예정' | '공연완료'
  rank?: number
}

export interface BoxOfficeResponse {
  success: boolean
  data: Performance[]
}

// composables/useBoxOffice.ts
export function useBoxOffice() {
  const allPerformances = ref<Performance[]>([])
  const error = ref<string | null>(null)

  const load = async (): Promise<void> => {
    try {
      const { data } = await performanceApi.getBoxOfficeByGenre(genre.value)
      const response = data as BoxOfficeResponse

      if (response.success) {
        allPerformances.value = response.data
      }
    } catch (e) {
      error.value = handleApiError(e as Error)
    }
  }

  return { allPerformances, error, load }
}
```

#### 5. API 응답 캐싱
**현재 문제:**
- 같은 데이터를 반복적으로 요청

**개선 방안:**
```javascript
// utils/cache.js
const cache = new Map()
const CACHE_DURATION = 5 * 60 * 1000 // 5분

export function getCachedData(key) {
  const cached = cache.get(key)
  if (!cached) return null

  if (Date.now() - cached.timestamp > CACHE_DURATION) {
    cache.delete(key)
    return null
  }

  return cached.data
}

export function setCachedData(key, data) {
  cache.set(key, {
    data,
    timestamp: Date.now()
  })
}

// composables/useBoxOffice.js
import { getCachedData, setCachedData } from '@/utils/cache'

const load = async () => {
  const cacheKey = `boxoffice-${genre.value}`
  const cached = getCachedData(cacheKey)

  if (cached) {
    allPerformances.value = cached
    return
  }

  loading.value = true
  try {
    const { data } = await performanceApi.getBoxOfficeByGenre(genre.value)
    if (data.success) {
      allPerformances.value = data.data
      setCachedData(cacheKey, data.data)
    }
  } catch (e) {
    error.value = handleApiError(e)
  } finally {
    loading.value = false
  }
}
```

#### 6. 페이지네이션 URL 동기화
**현재 문제:**
- 페이지를 새로고침하면 첫 페이지로 돌아감

**개선 방안:**
```javascript
// composables/useBoxOffice.js
import { useRoute, useRouter } from 'vue-router'

export function useBoxOffice() {
  const route = useRoute()
  const router = useRouter()

  // URL에서 초기값 읽기
  const currentPage = ref(Number(route.query.page) || 0)
  const genre = ref(route.query.genre || 'BBBC')

  // 페이지 변경 시 URL 업데이트
  const changeGenre = async (nextGenre) => {
    genre.value = nextGenre
    currentPage.value = 0

    await router.push({
      query: { genre: nextGenre, page: 0 }
    })

    await load()
  }

  const nextPage = () => {
    if (currentPage.value < totalPages.value - 1) {
      currentPage.value++

      router.push({
        query: { ...route.query, page: currentPage.value }
      })

      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  return { currentPage, genre, changeGenre, nextPage }
}
```

---

### 🟢 우선순위 낮음 (Nice to have)

#### 7. 이미지 지연 로딩 (Lazy Loading)
**개선 방안:**
```vue
<!-- components/BoxOffice/BoxOfficeCard.vue -->
<template>
  <img
    :src="perf.poster"
    :alt="perf.prfnm"
    class="poster-image"
    loading="lazy"
    @error="handleImageError"
  >
</template>
```

또는 Intersection Observer 사용:
```javascript
// composables/useLazyImage.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useLazyImage(imageSrc) {
  const imgRef = ref(null)
  const isLoaded = ref(false)
  const actualSrc = ref('')

  onMounted(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !isLoaded.value) {
          actualSrc.value = imageSrc.value
          isLoaded.value = true
          observer.unobserve(entry.target)
        }
      })
    })

    if (imgRef.value) {
      observer.observe(imgRef.value)
    }
  })

  return { imgRef, actualSrc, isLoaded }
}
```

#### 8. 성능 최적화: Virtual Scrolling
**현재 문제:**
- 공연 목록이 많을 때 성능 저하

**개선 방안:**
```bash
npm install vue-virtual-scroller
```

```vue
<!-- components/Performance/PerformanceGrid.vue -->
<template>
  <RecycleScroller
    :items="performances"
    :item-size="320"
    key-field="mt20id"
    v-slot="{ item }"
  >
    <PerformanceCard :performance="item" @click="emit('card-click', item.mt20id)" />
  </RecycleScroller>
</template>

<script setup>
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
</script>
```

#### 9. 접근성 (a11y) 개선
**개선 방안:**
```vue
<!-- components/BoxOffice/GenreTab.vue -->
<template>
  <div class="genre-tabs-container">
    <div class="genre-tabs" role="tablist" aria-label="공연 장르 선택">
      <button
        v-for="genre in genres"
        :key="genre.code"
        @click="onClick(genre.code)"
        :class="['genre-tab', { active: currentGenre === genre.code }]"
        role="tab"
        :aria-selected="currentGenre === genre.code"
        :aria-label="`${genre.name} 장르`"
      >
        {{ genre.name }}
      </button>
    </div>
  </div>
</template>
```

#### 10. 스켈레톤 UI
**현재 문제:**
- 로딩 중 빈 화면 표시

**개선 방안:**
```vue
<!-- components/common/SkeletonCard.vue -->
<template>
  <div class="skeleton-card">
    <div class="skeleton-poster"></div>
    <div class="skeleton-title"></div>
    <div class="skeleton-text"></div>
    <div class="skeleton-text"></div>
  </div>
</template>

<style scoped>
.skeleton-card {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton-poster {
  width: 100%;
  height: 280px;
  background: #e5e7eb;
  border-radius: 0.5rem;
}

.skeleton-title {
  height: 24px;
  background: #e5e7eb;
  border-radius: 4px;
  margin-top: 1rem;
}

.skeleton-text {
  height: 16px;
  background: #e5e7eb;
  border-radius: 4px;
  margin-top: 0.5rem;
}
</style>
```

**사용:**
```vue
<template>
  <div v-if="loading" class="performances-grid">
    <SkeletonCard v-for="i in 5" :key="i" />
  </div>
  <PerformanceGrid v-else :performances="performances" />
</template>
```

---

### 🔵 장기 개선 (Long-term)

#### 11. 테스트 코드 작성
```javascript
// composables/__tests__/useBoxOffice.spec.js
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useBoxOffice } from '../useBoxOffice'
import performanceApi from '@/api/performances'

vi.mock('@/api/performances')

describe('useBoxOffice', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should load performances successfully', async () => {
    const mockData = {
      success: true,
      data: [
        { mt20id: '1', prfnm: '테스트 공연', rank: 1 }
      ]
    }

    performanceApi.getBoxOfficeByGenre.mockResolvedValue({
      data: mockData
    })

    const { allPerformances, load, loading } = useBoxOffice()

    await load()

    expect(loading.value).toBe(false)
    expect(allPerformances.value).toEqual(mockData.data)
  })

  it('should handle errors properly', async () => {
    performanceApi.getBoxOfficeByGenre.mockRejectedValue(
      new Error('Network error')
    )

    const { error, load } = useBoxOffice()

    await load()

    expect(error.value).toBeTruthy()
  })
})
```

#### 12. 상태 관리 최적화
**Pinia의 고급 기능 활용:**

```javascript
// stores/performanceStore.js
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const usePerformanceStore = defineStore('performance', () => {
  const performances = ref([])
  const currentPerformance = ref(null)

  // Getters with caching
  const performanceById = computed(() => {
    return (id) => performances.value.find(p => p.mt20id === id)
  })

  const performancesByGenre = computed(() => {
    return (genre) => performances.value.filter(p => p.genrenm === genre)
  })

  // Actions with loading state
  const fetchPerformances = async (params) => {
    const cacheKey = JSON.stringify(params)

    // ... fetch logic
  }

  // Reset state
  function $reset() {
    performances.value = []
    currentPerformance.value = null
  }

  return {
    performances,
    currentPerformance,
    performanceById,
    performancesByGenre,
    fetchPerformances,
    $reset
  }
}, {
  // Persist state
  persist: {
    key: 'performance-store',
    storage: sessionStorage,
    paths: ['performances']
  }
})
```

#### 13. 컴포넌트 문서화
**Storybook 도입:**

```bash
npm install -D @storybook/vue3 @storybook/addon-essentials
```

```javascript
// components/BoxOffice/BoxOfficeCard.stories.js
import BoxOfficeCard from './BoxOfficeCard.vue'

export default {
  title: 'Components/BoxOffice/BoxOfficeCard',
  component: BoxOfficeCard,
  argTypes: {
    perf: { control: 'object' }
  }
}

const Template = (args) => ({
  components: { BoxOfficeCard },
  setup() {
    return { args }
  },
  template: '<BoxOfficeCard v-bind="args" />'
})

export const Default = Template.bind({})
Default.args = {
  perf: {
    mt20id: '1',
    prfnm: '오페라의 유령',
    poster: 'https://example.com/poster.jpg',
    genrenm: '뮤지컬',
    fcltynm: '샤롯데씨어터',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    rank: 1
  }
}

export const GoldRank = Template.bind({})
GoldRank.args = {
  ...Default.args,
  rank: 1
}

export const SilverRank = Template.bind({})
SilverRank.args = {
  ...Default.args,
  rank: 2
}
```

---

## 📈 리팩토링 성과

### 코드 감소량
- **LandingView**: 253줄 → 55줄 (**78% ↓**)
- **PerformanceListView**: 156줄 → 60줄 (**61% ↓**)
- **PerformanceDetailView**: 699줄 → 189줄 (**73% ↓**)

### 구조 개선
- ✅ **관심사 분리**: UI, 로직, API 계층 분리
- ✅ **재사용성**: 컴포넌트와 composable 재사용 가능
- ✅ **유지보수성**: 각 파일의 책임이 명확
- ✅ **가독성**: View 파일이 간결하고 이해하기 쉬움
- ✅ **테스트 용이성**: 각 부분을 독립적으로 테스트 가능

### 파일 구조
```
src/
├── api/                          # API 레이어
│   ├── axios.js
│   └── performances.js
├── composables/                  # 비즈니스 로직
│   ├── useBoxOffice.js
│   ├── usePerformanceList.js
│   ├── usePerformanceDetail.js
│   └── useKakaoMap.js
├── components/                   # UI 컴포넌트
│   ├── BoxOffice/
│   │   ├── BoxOfficeCard.vue
│   │   ├── BoxOfficeCarousel.vue
│   │   └── GenreTab.vue
│   ├── Performance/
│   │   ├── PerformanceCard.vue
│   │   ├── PerformanceFilters.vue
│   │   └── PerformanceGrid.vue
│   └── PerformanceDetail/
│       ├── HeaderSection.vue
│       └── MapModal.vue
├── stores/                       # 전역 상태 관리
│   └── performanceStore.js
└── views/                        # 페이지
    ├── LandingView.vue
    ├── PerformanceListView.vue
    └── PerformanceDetailView.vue
```

---

## 🎓 참고 자료

- [Vue 3 Composition API 공식 문서](https://vuejs.org/guide/reusability/composables.html)
- [Pinia 공식 문서](https://pinia.vuejs.org/)
- [Vue 3 스타일 가이드](https://vuejs.org/style-guide/)
- [Composables vs Store 패턴](https://vuejs.org/guide/scaling-up/state-management.html)

---

**작성자**: Claude (AI Assistant)
**마지막 업데이트**: 2024-12-14
