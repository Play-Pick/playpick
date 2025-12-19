<template>
  <div class="rating-chart">
    <div class="chart-header">
      <div class="header-left">
        <div class="rating-summary">
          <span class="average">평균 <i class="fas fa-star"></i>{{ averageRating }}</span>
          <span class="total">({{ totalReviews }}개)</span>
        </div>
      </div>
      <div class="chart-bars">
        <div
          v-for="rating in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]"
          :key="rating"
          class="bar-column"
        >
          <div class="bar-container">
            <div
              class="bar-fill"
              :style="{ height: getBarHeight(rating) + '%' }"
              :class="{ highlight: isHighlighted(rating) }"
            ></div>
          </div>
          <span class="bar-label">{{ rating }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  reviews: {
    type: Array,
    default: () => [],
  },
})

// 별점이 있는 리뷰만 필터링
const ratedReviews = computed(() => {
  return props.reviews.filter(r => r.rank !== null && r.rank !== undefined)
})

// 총 리뷰 수
const totalReviews = computed(() => ratedReviews.value.length)

// 평균 별점
const averageRating = computed(() => {
  if (totalReviews.value === 0) return 0
  const sum = ratedReviews.value.reduce((acc, r) => acc + r.rank, 0)
  return (sum / totalReviews.value).toFixed(1)
})

// 특정 별점의 개수
const getRatingCount = (rating) => {
  return ratedReviews.value.filter(r => r.rank === rating).length
}

// 특정 별점의 퍼센트
const getPercentage = (rating) => {
  if (totalReviews.value === 0) return 0
  return ((getRatingCount(rating) / totalReviews.value) * 100).toFixed(1)
}

// 막대 높이 계산 (0.5 단위)
const getBarHeight = (rating) => {
  const count = getRatingCount(rating)
  if (totalReviews.value === 0) return 0
  const percentage = (count / totalReviews.value) * 100
  return Math.min(percentage * 1.5, 100) // 최대 높이 제한
}

// 평균 별점에 가까운 막대 강조
const isHighlighted = (rating) => {
  const avg = parseFloat(averageRating.value)
  return Math.abs(rating - avg) <= 0.3
}
</script>

<style scoped>
.rating-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .rating-chart {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.chart-header {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}

.header-left {
  min-width: 120px;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.average {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  transition: color 0.3s;
}

:root.dark .average {
  color: #f3f4f6;
}

.average i {
  color: #fbbf24;
  margin: 0 0.25rem;
  font-size: 1rem;
}

.total {
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .total {
  color: #9ca3af;
}

.chart-bars {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.25rem;
  height: 80px;
  padding: 0 0.5rem;
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
}

.bar-container {
  width: 100%;
  height: 60px;
  display: flex;
  align-items: flex-end;
}

.bar-fill {
  width: 100%;
  background: #f3e8ff;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
  min-height: 2px;
}

:root.dark .bar-fill {
  background: #4b5563;
}

.bar-fill.highlight {
  background: #ec4899;
}

:root.dark .bar-fill.highlight {
  background: #818cf8;
}

.bar-label {
  font-size: 0.625rem;
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .bar-label {
  color: #6b7280;
}

/* 반응형 */
@media (max-width: 768px) {
  .rating-chart {
    padding: 1rem;
  }

  .chart-bars {
    height: 60px;
  }

  .bar-container {
    height: 45px;
  }
}
</style>
