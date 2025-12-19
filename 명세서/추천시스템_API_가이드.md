# 🎭 추천 시스템 API 가이드

## 📋 개요

사용자 행동 로그 기반 하이브리드 추천 시스템이 성공적으로 구현되었습니다.

### ✅ 구현 완료 항목

- [x] `recommendations` 앱 생성 및 설정
- [x] `UserLog`, `RecommendationCache` 모델 구현
- [x] Migration 실행
- [x] 추천 엔진 알고리즘 (6개 점수 함수)
- [x] Serializers 구현
- [x] API ViewSet 구현
- [x] URL 라우팅 설정
- [x] Django Admin 등록

---

## 🔌 API 엔드포인트

### 1. 사용자 행동 로그 저장

**POST** `/api/recommendations/log/`

사용자의 공연 조회, 찜하기, 검색 행동을 기록합니다.

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "performance_id": "PF264404",
  "action_type": "view"  // 'view', 'like', 'search' 중 하나
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "로그가 저장되었습니다.",
  "data": {
    "id": 123,
    "performance_id": "PF264404",
    "action_type": "view",
    "timestamp": "2025-12-17T14:30:00Z"
  }
}
```

**프론트엔드 사용 예시:**
```javascript
// useUserTracking.js (Composable)
export const useUserTracking = () => {
  const logAction = async (performanceId, actionType) => {
    try {
      await apiClient.post('/api/recommendations/log/', {
        performance_id: performanceId,
        action_type: actionType
      })
    } catch (error) {
      console.warn('로그 전송 실패:', error)
    }
  }
  return { logAction }
}

// PerformanceDetail.vue
import { useUserTracking } from '@/composables/useUserTracking'

const { logAction } = useUserTracking()

// 페이지 진입 시
onMounted(() => {
  logAction(route.params.id, 'view')
})

// 찜하기 버튼 클릭 시
const handleLike = () => {
  logAction(performance.mt20id, 'like')
  // ... 찜하기 로직
}
```

---

### 2. 추천 목록 조회

**GET** `/api/recommendations/`

사용자 맞춤 추천 공연 목록을 조회합니다.

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `top_n` (optional): 추천 개수 (기본값: 10)

**Request Example:**
```
GET /api/recommendations/?top_n=5
```

**Response (200 OK):**
```json
{
  "recommendations": [
    {
      "mt20id": "PF264404",
      "score": 0.85,
      "reason": "location",
      "reason_text": "🏠 강남구 근처에서 공연해요!",
      "prfnm": "뮤지컬 레베카",
      "poster": "http://www.kopis.or.kr/upload/pfmPoster/PF_PF264404_250117_095508.jpg",
      "prfpdfrom": "2025-01-15",
      "prfpdto": "2025-03-31",
      "fcltynm": "샤롯데씨어터",
      "genrenm": "뮤지컬",
      "area": "서울"
    },
    {
      "mt20id": "PF264321",
      "score": 0.78,
      "reason": "preference",
      "reason_text": "❤️ 취향 저격 공연이에요!",
      "prfnm": "연극 햄릿",
      "poster": "http://...",
      "prfpdfrom": "2025-02-01",
      "prfpdto": "2025-04-30",
      "fcltynm": "예술의전당",
      "genrenm": "연극",
      "area": "서울"
    }
  ],
  "cached": false,
  "updated_at": "2025-12-17T14:30:00Z"
}
```

**프론트엔드 사용 예시:**
```javascript
// useRecommendations.js (Composable)
import { ref } from 'vue'
import apiClient from '@/api/client'

export const useRecommendations = () => {
  const recommendations = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchRecommendations = async (topN = 10) => {
    loading.value = true
    error.value = null

    try {
      const response = await apiClient.get('/api/recommendations/', {
        params: { top_n: topN }
      })
      recommendations.value = response.data.recommendations
    } catch (err) {
      error.value = err.message
      console.error('추천 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    recommendations,
    loading,
    error,
    fetchRecommendations
  }
}

// HomeView.vue 또는 RecommendationSection.vue
<template>
  <div class="recommendations">
    <h2>{{ username }}님을 위한 추천 공연</h2>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="recommendation-grid">
      <PerformanceCard
        v-for="item in recommendations"
        :key="item.mt20id"
        :performance="item"
        :badge="item.reason_text"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRecommendations } from '@/composables/useRecommendations'

const authStore = useAuthStore()
const { recommendations, loading, error, fetchRecommendations } = useRecommendations()

onMounted(() => {
  if (authStore.isAuthenticated) {
    fetchRecommendations(10)
  }
})
</script>
```

---

### 3. 추천 캐시 강제 갱신

**POST** `/api/recommendations/refresh/`

추천 캐시를 강제로 갱신합니다 (일반적으로 필요 없음, 캐시는 1시간 후 자동 갱신).

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "top_n": 10  // optional
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "추천 목록이 갱신되었습니다.",
  "recommendations": [ /* ... */ ],
  "updated_at": "2025-12-17T14:30:00Z"
}
```

---

### 4. 본인의 행동 로그 조회

**GET** `/api/recommendations/log/`

본인의 행동 로그 내역을 조회합니다.

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
[
  {
    "id": 123,
    "performance_id": "PF264404",
    "action_type": "view",
    "timestamp": "2025-12-17T14:30:00Z"
  },
  {
    "id": 122,
    "performance_id": "PF264321",
    "action_type": "like",
    "timestamp": "2025-12-17T14:25:00Z"
  }
]
```

---

## 🎨 추천 사유 (Reason) 종류

추천 엔진이 반환하는 `reason` 필드와 `reason_text` 값:

| reason | reason_text | 설명 |
|:---|:---|:---|
| `click` | "👁️ 최근 {장르} 장르를 자주 보셨어요!" | f1: 클릭/관심 로그 기반 |
| `preference` | "❤️ 취향 저격 공연이에요!" | f2: 선호 장르/배우 매칭 |
| `location` | "🏠 {구} 근처에서 공연해요!" | f3: 위치 근접성 |
| `popularity` | "🔥 지금 가장 핫한 공연이에요!" | f4: 대중성/랭킹 |
| `recency` | "⏰ 곧 시작하는 공연이에요!" | f5: 최신성/마감 임박 |
| `collaborative` | "👥 비슷한 취향의 사람들이 좋아해요!" | f6: 협업 필터링 |

**프론트엔드 뱃지 스타일 예시:**
```vue
<template>
  <div class="recommendation-card">
    <div class="reason-badge" :class="`badge-${reason}`">
      {{ reasonText }}
    </div>
    <img :src="poster" :alt="prfnm" />
    <h3>{{ prfnm }}</h3>
  </div>
</template>

<style scoped>
.reason-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  color: white;
}

.badge-location { background: #3498db; }
.badge-preference { background: #e74c3c; }
.badge-popularity { background: #f39c12; }
.badge-click { background: #9b59b6; }
.badge-recency { background: #1abc9c; }
.badge-collaborative { background: #34495e; }
</style>
```

---

## 🧪 테스트 시나리오

### 1. 기본 추천 흐름 테스트

```bash
# 1. 로그인 (JWT 토큰 발급)
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 응답: {"access": "eyJ0...", "refresh": "eyJ0..."}

# 2. 공연 상세 페이지 조회 로그 저장
curl -X POST http://localhost:8000/api/recommendations/log/ \
  -H "Authorization: Bearer eyJ0..." \
  -H "Content-Type: application/json" \
  -d '{"performance_id": "PF264404", "action_type": "view"}'

# 3. 찜하기 로그 저장
curl -X POST http://localhost:8000/api/recommendations/log/ \
  -H "Authorization: Bearer eyJ0..." \
  -H "Content-Type: application/json" \
  -d '{"performance_id": "PF264404", "action_type": "like"}'

# 4. 추천 목록 조회
curl -X GET "http://localhost:8000/api/recommendations/?top_n=5" \
  -H "Authorization: Bearer eyJ0..."
```

### 2. 프론트엔드 통합 테스트

1. **회원가입 시**: 취향 수집 폼에서 `preference_tags`, `favorite_actors`, `region_gu` 입력
2. **공연 상세 페이지**: `onMounted` 훅에서 `logAction('view')` 자동 호출
3. **찜하기 버튼**: 클릭 시 `logAction('like')` 호출
4. **메인 페이지**: 추천 섹션에서 `/api/recommendations/` 조회 및 렌더링

---

## 📊 추천 알고리즘 상세

### 점수 계산 공식

```
Score(user, performance) =
  0.25 × f1(클릭/관심) +
  0.20 × f2(취향 매칭) +
  0.15 × f3(위치 근접성) +
  0.15 × f4(대중성) +
  0.10 × f5(최신성) +
  0.15 × f6(협업 필터링)
```

### 개별 점수 함수 설명

#### f1: 클릭/관심 로그 기반 (Time Decay)
- 사용자가 최근 30일간 본 공연의 장르와 일치하면 점수 부여
- 행동 유형별 기본 점수: view=1, like=3, search=2
- Time Decay 적용: `score × 0.95^(경과일수)`

#### f2: 취향 매칭
- User의 `preference_tags`와 공연 `genrenm` 일치: +0.6
- User의 `favorite_actors`와 공연 `cast_search_text` 일치: +0.4

#### f3: 위치 근접성
- User의 `region_gu`와 공연 `area` 완전 일치: 1.0
- 시/도 레벨 일치 (예: 둘 다 "서울"): 0.6
- 불일치: 0.0

#### f4: 대중성
- `PerformanceMetric.score_popularity` 값 사용
- 없으면 `BoxOfficeRanking`으로 대체 계산

#### f5: 최신성
- 공연 시작일이 임박할수록 높은 점수 (시그모이드 함수)
- 0~30일 사이: 높은 점수

#### f6: 협업 필터링
- 사용자가 좋아한 공연과 유사한 공연 추천
- `PerformanceMetric.similar_performances` 활용

---

## ⚙️ 캐싱 전략

- **TTL**: 1시간 (기본값)
- **갱신 조건**:
  - 캐시가 없을 때
  - 캐시가 1시간 이상 경과했을 때
  - 명시적으로 `/refresh/` 호출했을 때
- **무효화**: 새 로그 저장 시 자동 삭제 (선택적)

---

## 🔧 향후 개선 사항 (Optional)

1. **Batch Job**: `PerformanceMetric` 주기적 갱신
   ```bash
   python manage.py update_metrics
   ```

2. **Collaborative Filtering 고도화**:
   - 아이템 간 유사도 사전 계산
   - Jaccard Similarity 활용

3. **A/B 테스트**:
   - 가중치 최적화
   - Serendipity 요소 추가 (필터 버블 방지)

4. **실시간 스트리밍**:
   - Kafka/Redis로 로그 수집 파이프라인 구축

---

## 📝 프론트엔드 체크리스트

- [ ] `useUserTracking.js` composable 구현
- [ ] `PerformanceDetail.vue`에서 `logAction('view')` 호출
- [ ] 찜하기 버튼에서 `logAction('like')` 호출
- [ ] `useRecommendations.js` composable 구현
- [ ] 메인 페이지에 추천 섹션 추가
- [ ] 추천 사유 뱃지 UI 구현
- [ ] 회원가입 시 취향 수집 폼 추가

---

## 🎉 완료!

추천 시스템이 성공적으로 구현되었습니다. 프론트엔드에서 위 API를 호출하여 개인화된 공연 추천 서비스를 제공할 수 있습니다.

**API 베이스 URL**: `http://localhost:8000/api/recommendations/`

**Django Admin**: `http://localhost:8000/admin/`에서 로그와 캐시 데이터 확인 가능
