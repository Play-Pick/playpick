# Vue Slots 완벽 가이드

## 📌 Slot이란?

Slot은 Vue의 **컴포넌트 재사용 메커니즘**입니다. 부모 컴포넌트가 자식 컴포넌트에게 **HTML 콘텐츠를 전달**할 수 있게 해주는 기능입니다.

### 쉬운 비유
- **Props**: 데이터(문자열, 숫자, 객체)를 전달
- **Slots**: HTML 코드 덩어리를 전달

---

## 🎯 왜 Slot을 사용하는가?

### ❌ Slot 없이 (코드 중복)
```vue
<!-- PerformanceCard.vue -->
<div class="card">
  <img :src="performance.poster" />
  <span class="genre-badge">{{ performance.genre }}</span> <!-- 고정된 뱃지 -->
</div>

<!-- BoxOfficeCard.vue -->
<div class="card">
  <img :src="performance.poster" />
  <span class="rank-badge">🏆 {{ rank }}</span> <!-- 다른 뱃지 필요 -->
</div>
```
👉 **문제**: 거의 동일한 카드를 중복으로 만들어야 함!

### ✅ Slot 사용 (재사용)
```vue
<!-- BaseCard.vue (공통 카드) -->
<div class="card">
  <img :src="performance.poster" />
  <slot name="badge"></slot> <!-- 🎯 여기에 다양한 뱃지를 끼워넣을 수 있음 -->
</div>

<!-- 사용할 때 -->
<BaseCard :performance="perf">
  <template #badge>
    <span class="rank-badge">🏆 {{ rank }}</span>
  </template>
</BaseCard>
```
👉 **해결**: 하나의 카드 컴포넌트로 다양한 변형 생성!

---

## 🔧 Slot 종류

### 1. 기본 Slot (Default Slot)

**가장 간단한 형태**
```vue
<!-- Button.vue -->
<template>
  <button class="custom-btn">
    <slot></slot> <!-- 기본 슬롯 -->
  </button>
</template>

<!-- 사용 -->
<Button>클릭하세요</Button>
<Button>
  <i class="fas fa-heart"></i> 좋아요
</Button>
```

**렌더링 결과:**
```html
<button class="custom-btn">클릭하세요</button>
<button class="custom-btn">
  <i class="fas fa-heart"></i> 좋아요
</button>
```

---

### 2. Named Slot (이름 있는 슬롯)

**여러 위치에 다른 콘텐츠 삽입**
```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <div class="header">
      <slot name="header"></slot> <!-- 헤더 슬롯 -->
    </div>
    <div class="body">
      <slot></slot> <!-- 기본 슬롯 -->
    </div>
    <div class="footer">
      <slot name="footer"></slot> <!-- 푸터 슬롯 -->
    </div>
  </div>
</template>

<!-- 사용 -->
<Card>
  <template #header>
    <h2>제목입니다</h2>
  </template>

  <p>본문 내용입니다</p>

  <template #footer>
    <button>확인</button>
  </template>
</Card>
```

**렌더링 결과:**
```html
<div class="card">
  <div class="header">
    <h2>제목입니다</h2>
  </div>
  <div class="body">
    <p>본문 내용입니다</p>
  </div>
  <div class="footer">
    <button>확인</button>
  </template>
</div>
```

---

### 3. Scoped Slot (스코프 슬롯)

**자식 컴포넌트의 데이터를 부모에게 전달**
```vue
<!-- List.vue -->
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      <slot name="item" :item="item"></slot> <!-- item 데이터 전달 -->
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: Array
})
</script>

<!-- 사용 -->
<List :items="performances">
  <template #item="{ item }"> <!-- item 받아서 사용 -->
    <div>
      <h3>{{ item.title }}</h3>
      <p>{{ item.venue }}</p>
    </div>
  </template>
</List>
```

---

### 4. Fallback Content (기본값)

**슬롯에 아무것도 전달하지 않았을 때 보여줄 기본 콘텐츠**
```vue
<!-- Button.vue -->
<template>
  <button>
    <slot>기본 버튼</slot> <!-- 기본값 -->
  </button>
</template>

<!-- 사용 -->
<Button></Button>          <!-- "기본 버튼" 표시 -->
<Button>저장</Button>       <!-- "저장" 표시 -->
```

---

## 🎨 실전 예제: 공연 카드 재사용

### 현재 프로젝트의 카드 종류
1. **PerformanceCard**: 기본 장르 뱃지
2. **BoxOfficeCard**: 순위 뱃지 (🏆 1위)
3. **RecommendationCard**: 추천 이유 뱃지 (✨ 선호 장르)
4. **RankingCard**: 큰 순위 뱃지 + 통계 정보

### 해결 방안: Slot 기반 BasePerformanceCard

```vue
<!-- BasePerformanceCard.vue (공통 카드) -->
<template>
  <router-link :to="`/performances/${performance.mt20id}`" class="performance-card">
    <!-- 포스터 영역 -->
    <div class="poster-container">
      <img :src="performance.poster" :alt="performance.prfnm" />

      <!-- 🎯 뱃지 슬롯: 각 카드마다 다른 뱃지 삽입 -->
      <slot name="badge"></slot>

      <!-- 찜하기 버튼 (공통) -->
      <button
        v-if="showLikeButton"
        @click.stop.prevent="$emit('toggle-like', performance.mt20id)"
        :class="['like-button', { liked: performance.is_liked }]"
      >
        <i :class="performance.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
      </button>

      <!-- 호버 오버레이 (공통) -->
      <div class="hover-overlay">
        <span>자세히 보기 →</span>
      </div>
    </div>

    <!-- 정보 영역 -->
    <div class="card-info">
      <h3>{{ performance.prfnm }}</h3>

      <!-- 🎯 추가 정보 슬롯: 기본 정보 외 추가 정보 삽입 -->
      <slot name="extra-info">
        <!-- 기본값: 장소와 날짜만 표시 -->
        <p><i class="fas fa-map-marker-alt"></i> {{ performance.fcltynm }}</p>
        <p><i class="fas fa-calendar"></i> {{ formatDate(performance.prfpdfrom, performance.prfpdto) }}</p>
      </slot>

      <!-- 🎯 하단 슬롯: 장르 뱃지 등 -->
      <slot name="bottom">
        <span class="genre-badge">{{ performance.genrenm }}</span>
      </slot>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  performance: { type: Object, required: true },
  showLikeButton: { type: Boolean, default: true }
})

defineEmits(['toggle-like'])

const formatDate = (from, to) => `${from?.replace(/-/g, '.')} ~ ${to?.replace(/-/g, '.')}`
</script>
```

### 사용 예시

#### 1. 기본 PerformanceCard
```vue
<BasePerformanceCard :performance="perf" @toggle-like="handleLike">
  <template #badge>
    <span class="genre-badge-overlay">{{ perf.genrenm }}</span>
  </template>
</BasePerformanceCard>
```

#### 2. BoxOfficeCard (순위 뱃지)
```vue
<BasePerformanceCard :performance="perf" @toggle-like="handleLike">
  <template #badge>
    <div :class="['rank-badge', getRankClass(perf.rank)]">
      <i class="fas fa-trophy"></i> {{ perf.rank }}
    </div>
  </template>
</BasePerformanceCard>
```

#### 3. RecommendationCard (추천 이유)
```vue
<BasePerformanceCard :performance="perf" @toggle-like="handleLike">
  <template #badge>
    <div class="reason-badge">
      <i class="fas fa-sparkles"></i> {{ reason }}
    </div>
  </template>
</BasePerformanceCard>
```

#### 4. RankingCard (상세 정보 추가)
```vue
<BasePerformanceCard :performance="perf" @toggle-like="handleLike">
  <template #badge>
    <div :class="['rank-badge-large', getRankBadgeClass(perf.rank)]">
      <div class="rank-number">{{ perf.rank }}</div>
      <div class="rank-label">위</div>
    </div>
  </template>

  <!-- 추가 정보 슬롯 오버라이드 -->
  <template #extra-info>
    <p><i class="fas fa-map-marker-alt"></i> {{ perf.fcltynm }}</p>
    <p><i class="fas fa-calendar"></i> {{ formatDate(perf.prfpdfrom, perf.prfpdto) }}</p>
    <p><i class="fas fa-users"></i> 좌석 {{ perf.seat_count?.toLocaleString() }}석</p>
    <p><i class="fas fa-ticket-alt"></i> 공연 {{ perf.performance_count?.toLocaleString() }}회</p>
  </template>
</BasePerformanceCard>
```

---

## ✨ Slot의 장점

### 1. **코드 재사용성 극대화**
- 한 번 작성한 컴포넌트를 여러 곳에서 다양하게 사용

### 2. **유지보수 용이**
- 공통 로직 수정 시 BaseCard만 수정하면 모든 카드에 반영

### 3. **유연성**
- 각 사용처마다 필요한 부분만 커스터마이징 가능

### 4. **명확한 구조**
- 어떤 부분이 변할 수 있는지 slot으로 명확히 표현

---

## 🎯 Slot vs Props 언제 사용?

### Props를 사용할 때
- 간단한 데이터 전달 (문자열, 숫자, Boolean)
- 조건부 렌더링 (`v-if`)
```vue
<Button :disabled="true" :loading="false" text="클릭" />
```

### Slot을 사용할 때
- HTML 구조가 달라질 때
- 스타일이 달라질 때
- 아이콘, 이미지 등 복잡한 콘텐츠
```vue
<Button>
  <i class="fas fa-download"></i> 다운로드
</Button>
```

---

## 🔍 실전 팁

### 1. Named Slot 축약 문법
```vue
<!-- 긴 문법 -->
<template v-slot:badge>

<!-- 짧은 문법 (권장) -->
<template #badge>
```

### 2. Slot 존재 여부 확인
```vue
<template>
  <div class="card">
    <div v-if="$slots.header" class="header">
      <slot name="header"></slot>
    </div>
  </div>
</template>
```

### 3. 동적 Slot 이름
```vue
<template>
  <slot :name="slotName"></slot>
</template>
```

---

## 📚 요약

| 개념 | 설명 | 예시 |
|------|------|------|
| **기본 Slot** | 단순 콘텐츠 전달 | `<slot></slot>` |
| **Named Slot** | 여러 위치에 전달 | `<slot name="badge">` |
| **Scoped Slot** | 자식 데이터 활용 | `<slot :item="data">` |
| **Fallback** | 기본값 제공 | `<slot>기본값</slot>` |

---

## 🎓 다음 단계

1. ✅ 이 문서를 읽고 Slot 개념 이해
2. 🔨 BasePerformanceCard 구현
3. 🔄 기존 카드들을 BasePerformanceCard로 리팩토링
4. 🧪 테스트 및 검증

---

**작성일**: 2025-12-23
**프로젝트**: final-pjt
**작성자**: Claude Code
