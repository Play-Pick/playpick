# 공연 카드 컴포넌트 분석 및 재사용 전략

## 📊 현재 카드 컴포넌트 현황

### 발견된 카드 종류

| 카드 이름 | 파일 위치 | 주요 용도 |
|----------|----------|----------|
| **PerformanceCard** | `components/Performance/PerformanceCard.vue` | 기본 공연 목록 |
| **BoxOfficeCard** | `components/BoxOffice/BoxOfficeCard.vue` | 박스오피스 순위 |
| **RecommendationCard** | `components/Recommendation/RecommendationCard.vue` | 개인화 추천 |
| **RankingCard** | `components/BoxOffice/RankingCard.vue` | 순위 상세 페이지 |

---

## 🔍 카드별 상세 분석

### 1️⃣ PerformanceCard (기본 카드)

**파일**: `src/components/Performance/PerformanceCard.vue`

**특징**:
- ✅ 가장 심플한 디자인
- ✅ 장르 뱃지 오버레이
- ✅ 찜하기 버튼
- ✅ 클릭 이벤트 emit

**고유 요소**:
```vue
<span class="genre-badge card-badge-overlay">
  {{ performance.genrenm }}
</span>
```

**Props**:
```javascript
{
  performance: Object,
  showLikeButton: Boolean (default: true),
  likeLoading: Boolean (default: false)
}
```

**Emits**:
- `click` - 카드 클릭
- `toggle-like` - 찜하기 토글

---

### 2️⃣ BoxOfficeCard (박스오피스)

**파일**: `src/components/BoxOffice/BoxOfficeCard.vue`

**특징**:
- ✅ 순위 뱃지 (작은 사이즈, 오버레이)
- ✅ 1-3위 금은동 스타일
- ✅ 호버 오버레이 "자세히 보기 →"
- ✅ `router-link` 직접 사용 (emit 없음)

**고유 요소**:
```vue
<!-- 순위 뱃지 -->
<div :class="['rank-badge card-badge-overlay', getRankBadgeClass(perf.rank)]">
  <i class="fas fa-trophy"></i>{{ perf.rank }}
</div>

<!-- 호버 오버레이 -->
<div class="hover-overlay">
  <span>자세히 보기 →</span>
</div>
```

**순위별 스타일**:
```javascript
getRankBadgeClass(rank) {
  if (rank === 1) return 'rank-gold'    // 금색 그라디언트
  if (rank === 2) return 'rank-silver'  // 은색 그라디언트
  if (rank === 3) return 'rank-bronze'  // 동색 그라디언트
  return 'rank-default'                 // 기본 스타일
}
```

**추가 정보**:
- 장소 아이콘 (`fa-map-marker-alt`)
- 날짜 아이콘 (`fa-calendar`)
- 장르 태그 (칩 스타일)

---

### 3️⃣ RecommendationCard (추천 카드)

**파일**: `src/components/Recommendation/RecommendationCard.vue`

**특징**:
- ✅ 추천 이유 뱃지 (sparkles ✨)
- ✅ 고정 높이 레이아웃 (`min-height: 520px`)
- ✅ 포스터 3:4 비율 (`padding-top: 133.33%`)
- ✅ 호버 오버레이

**고유 요소**:
```vue
<!-- 추천 이유 뱃지 -->
<div v-if="reason" class="reason-badge card-badge-overlay">
  <i class="fas fa-sparkles"></i>
  <span>{{ reason }}</span>
</div>
```

**Props**:
```javascript
{
  performance: Object,
  reason: String,              // 🎯 고유: 추천 이유
  showLikeButton: Boolean,
  likeLoading: Boolean
}
```

**레이아웃 특징**:
- 제목 2줄 고정 (`-webkit-line-clamp: 2`)
- 최소 높이 보장으로 그리드 정렬 일관성 유지

---

### 4️⃣ RankingCard (순위 상세)

**파일**: `src/components/BoxOffice/RankingCard.vue`

**특징**:
- ✅ **큰 순위 뱃지** (4rem 원형)
- ✅ 1위 특별 효과 (금색 테두리 애니메이션)
- ✅ **상세 통계 정보** (좌석 수, 공연 횟수)
- ✅ 가장 화려한 호버 효과

**고유 요소**:
```vue
<!-- 대형 순위 뱃지 -->
<div :class="['rank-badge-large', getRankBadgeClass(perf.rank)]">
  <div class="rank-number">{{ perf.rank }}</div>
  <div class="rank-label">위</div>
</div>

<!-- 추가 통계 정보 -->
<div class="info-item">
  <i class="fas fa-users"></i>
  <span>좌석 {{ formatNumber(perf.seat_count) }}석</span>
</div>
<div class="info-item">
  <i class="fas fa-ticket-alt"></i>
  <span>공연 {{ formatNumber(perf.performance_count) }}회</span>
</div>
```

**1위 특별 효과**:
```css
.rank-1 {
  border: 3px solid #fbbf24;
}

.rank-1::before {
  /* 금색 그라디언트 외곽선 애니메이션 */
  background: linear-gradient(45deg, #fbbf24, #f59e0b, #fbbf24);
}

.rank-1:hover::before {
  opacity: 0.5;
}
```

**호버 효과**:
```css
.ranking-card:hover {
  transform: translateY(-1rem) scale(1.02);  /* 더 크게 올라감 */
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
}
```

---

## 🎨 공통 요소 분석

### ✅ 모든 카드의 공통점

| 요소 | 설명 |
|------|------|
| **포스터 이미지** | `performance.poster` |
| **제목** | `performance.prfnm` |
| **장소** | `performance.fcltynm` |
| **날짜** | `performance.prfpdfrom ~ prfpdto` |
| **장르** | `performance.genrenm` |
| **찜하기 버튼** | 동일한 디자인 및 로직 |
| **호버 효과** | 이미지 확대 (`transform: scale(1.1)`) |
| **이미지 에러 처리** | `handleImageError` → `/no_poster.png` |
| **다크모드 지원** | `:root.dark` CSS 변수 |

### 🎯 차이점 요약

| 카드 | 고유 뱃지 | 추가 정보 | 특별 효과 |
|------|----------|----------|----------|
| **Performance** | 장르 뱃지 | - | - |
| **BoxOffice** | 순위 뱃지 (작음) | 호버 메시지 | - |
| **Recommendation** | 추천 이유 뱃지 | - | 고정 높이 |
| **Ranking** | 순위 뱃지 (큼) | 좌석/공연 횟수 | 1위 금테 |

---

## 🔄 재사용 전략

### 📋 제안: BasePerformanceCard 생성

**핵심 아이디어**:
- 공통 부분은 하나의 컴포넌트로
- 차이점은 **Slot**으로 주입

### Slot 구조 설계

```vue
<BasePerformanceCard :performance="perf">
  <!-- 슬롯 1: 뱃지 (왼쪽 상단 오버레이) -->
  <template #badge>
    <!-- PerformanceCard: 장르 뱃지 -->
    <!-- BoxOfficeCard: 순위 뱃지 (작음) -->
    <!-- RecommendationCard: 추천 이유 뱃지 -->
    <!-- RankingCard: 순위 뱃지 (큼) -->
  </template>

  <!-- 슬롯 2: 추가 정보 (날짜/장소 아래) -->
  <template #extra-info>
    <!-- 기본값: 없음 -->
    <!-- RankingCard: 좌석 수, 공연 횟수 -->
  </template>

  <!-- 슬롯 3: 하단 (장르 뱃지 등) -->
  <template #footer>
    <!-- 기본값: 장르 칩 -->
    <!-- 필요시 오버라이드 -->
  </template>
</BasePerformanceCard>
```

---

## 📝 Props 설계

### BasePerformanceCard Props

```typescript
interface Props {
  // 필수
  performance: Performance       // 공연 정보 객체

  // 선택
  showLikeButton?: boolean       // 찜하기 버튼 표시 (default: true)
  likeLoading?: boolean          // 찜하기 로딩 (default: false)
  cardSize?: 'small' | 'medium' | 'large'  // 카드 크기
  hoverEffect?: 'default' | 'premium'      // 호버 효과 강도
}
```

### BasePerformanceCard Emits

```typescript
const emit = defineEmits<{
  'toggle-like': [performanceId: string]
  'click': [performanceId: string]  // optional
}>()
```

---

## 🎯 마이그레이션 계획

### Phase 1: BasePerformanceCard 생성
1. ✅ 공통 HTML 구조 정의
2. ✅ 공통 스타일 추출
3. ✅ Slot 위치 정의
4. ✅ Props/Emits 설계

### Phase 2: 기존 카드 변환
1. PerformanceCard → BasePerformanceCard 래퍼
2. BoxOfficeCard → BasePerformanceCard 래퍼
3. RecommendationCard → BasePerformanceCard 래퍼
4. RankingCard → BasePerformanceCard 래퍼

### Phase 3: 테스트 및 최적화
1. 각 페이지에서 정상 작동 확인
2. 스타일 미세 조정
3. 성능 검증

---

## 📊 예상 효과

### Before (현재)
- 4개 카드 컴포넌트
- 총 ~1,200 줄 코드
- 중복 코드 많음

### After (리팩토링 후)
- 1개 Base + 4개 Wrapper
- 총 ~600 줄 코드 (50% 감소)
- 유지보수성 ↑↑↑

---

## 🚀 추가 개선 아이디어

### 1. 카드 애니메이션 통일
```vue
<!-- BasePerformanceCard에 애니메이션 prop 추가 -->
<BasePerformanceCard
  :animation="'slide-up'"
  :delay="index * 100"
/>
```

### 2. 스켈레톤 로딩
```vue
<BasePerformanceCard :loading="true">
  <!-- 스켈레톤 UI 자동 표시 -->
</BasePerformanceCard>
```

### 3. 카드 액션 슬롯
```vue
<template #actions>
  <button>공유</button>
  <button>리뷰 작성</button>
</template>
```

---

## 📚 참고 파일

- [Vue Slots 가이드](./Vue-Slots-Guide.md)
- [PerformanceCard.vue](../src/components/Performance/PerformanceCard.vue)
- [BoxOfficeCard.vue](../src/components/BoxOffice/BoxOfficeCard.vue)
- [RecommendationCard.vue](../src/components/Recommendation/RecommendationCard.vue)
- [RankingCard.vue](../src/components/BoxOffice/RankingCard.vue)

---

**작성일**: 2025-12-23
**분석자**: Claude Code
**상태**: ✅ 분석 완료, 리팩토링 준비 완료
