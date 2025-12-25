<template>
  <BasePerformanceCard
    :performance="performance"
    :show-like-button="showLikeButton"
    :like-loading="likeLoading"
    card-class="recommendation-card"
    @toggle-like="handleLikeClick"
  >
    <!-- 추천 점수 뱃지 -->
    <template #badge>
      <div v-if="reason" :class="['score-badge', getScoreBadgeClass(reason)]">
        <div class="score-text">{{ reason }}</div>
      </div>
    </template>
  </BasePerformanceCard>
</template>

<script setup>
import BasePerformanceCard from '@/components/Common/BasePerformanceCard.vue'

const props = defineProps({
  performance: {
    type: Object,
    required: true
  },
  reason: {
    type: String,
    default: ''
  },
  showLikeButton: {
    type: Boolean,
    default: true
  },
  likeLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle-like'])

const handleLikeClick = () => {
  emit('toggle-like', props.performance.mt20id)
}

// 점수에 따른 배지 클래스 결정
const getScoreBadgeClass = (reason) => {
  // reason에서 숫자 추출 (예: "85.2%" -> 85.2)
  const scoreMatch = reason.match(/[\d.]+/)
  if (!scoreMatch) return '' // 점수가 없으면 배지 표시 안 함

  const score = parseFloat(scoreMatch[0])

  if (score >= 90) return 'score-gold'      // 90점 이상 - 골드
  if (score >= 75) return 'score-silver'    // 75점 이상 - 실버
  if (score >= 60) return 'score-bronze'    // 60점 이상 - 브론즈
  return '' // 60점 미만 - 배지 표시 안 함
}
</script>

<style scoped>
/* Recommendation 카드 커스텀 */
.recommendation-card {
  min-height: 520px; /* 고정된 카드 높이로 레이아웃 균일화 */
}

/* 추천 점수 뱃지 - 우측 상단 */
.score-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 50px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 10;
  animation: pulse 2s infinite;
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
}

.score-text {
  color: white;
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.3px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  line-height: 1;
}

/* 점수별 배지 색상 - BoxOfficeCard와 동일 */
.score-gold {
  background: linear-gradient(to right, #fbbf24, #f59e0b);
}

.score-silver {
  background: linear-gradient(to right, #d1d5db, #9ca3af);
}

.score-bronze {
  background: linear-gradient(to right, #fb923c, #ea580c);
}

/* 애니메이션 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}
</style>
