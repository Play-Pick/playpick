<template>
  <BasePerformanceCard
    :performance="perf"
    :show-like-button="showLikeButton"
    :like-loading="likeLoading"
    :card-class="['ranking-card', getRankClass(perf.rank)].join(' ')"
    @toggle-like="handleLikeClick"
  >
    <!-- 대형 순위 뱃지 -->
    <template #badge>
      <div :class="['rank-badge-large', getRankBadgeClass(perf.rank)]">
        <div class="rank-number">{{ perf.rank }}</div>
        <div class="rank-label">위</div>
      </div>
    </template>

    <!-- 상세 정보 (기본 정보 + 통계) -->
    <template #info>
      <div class="info-item">
        <i class="fas fa-map-marker-alt"></i>
        <span>{{ perf.fcltynm || '정보 없음' }}</span>
      </div>
      <div class="info-item">
        <i class="fas fa-calendar"></i>
        <span>{{ formatDate(perf.prfpdfrom) }} ~ {{ formatDate(perf.prfpdto) }}</span>
      </div>
      <div class="info-item">
        <i class="fas fa-users"></i>
        <span>좌석 {{ formatNumber(perf.seat_count) }}석</span>
      </div>
      <div class="info-item">
        <i class="fas fa-ticket-alt"></i>
        <span>공연 {{ formatNumber(perf.performance_count) }}회</span>
      </div>
    </template>
  </BasePerformanceCard>
</template>

<script setup>
import BasePerformanceCard from '@/components/Common/BasePerformanceCard.vue'

const props = defineProps({
  perf: {
    type: Object,
    required: true
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
  emit('toggle-like', props.perf.mt20id)
}

// 순위별 클래스
const getRankClass = (rank) => {
  if (rank === 1) return 'rank-1'
  if (rank === 2) return 'rank-2'
  if (rank === 3) return 'rank-3'
  return ''
}

// 순위 배지 클래스
const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'badge-gold'
  if (rank === 2) return 'badge-silver'
  if (rank === 3) return 'badge-bronze'
  return 'badge-default'
}

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

// 숫자 포맷 (천 단위 콤마)
const formatNumber = (num) => {
  if (!num) return '0'
  return num.toLocaleString()
}
</script>

<style scoped>
/* Ranking 카드 커스텀 */
.ranking-card {
  border-radius: 1.5rem;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.ranking-card:hover {
  transform: translateY(-1rem) scale(1.02);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
}

/* 1위 카드 특별 효과 */
.rank-1 {
  border: 3px solid #fbbf24;
}

.rank-1::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #fbbf24, #f59e0b, #fbbf24);
  border-radius: 1.5rem;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s;
}

.rank-1:hover::before {
  opacity: 0.5;
}

/* 대형 순위 배지 */
.rank-badge-large {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  color: white;
  font-weight: 800;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.4);
}

.badge-gold {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  box-shadow: 0 10px 20px -5px rgba(251, 191, 36, 0.6);
}

.badge-silver {
  background: linear-gradient(135deg, #e5e7eb 0%, #9ca3af 100%);
  box-shadow: 0 10px 20px -5px rgba(156, 163, 175, 0.6);
}

.badge-bronze {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
  box-shadow: 0 10px 20px -5px rgba(251, 146, 60, 0.6);
}

.badge-default {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  box-shadow: 0 10px 20px -5px rgba(107, 114, 128, 0.6);
}

.rank-number {
  font-size: 1.75rem;
  line-height: 1;
}

.rank-label {
  font-size: 0.75rem;
  margin-top: 0.125rem;
}

/* 상세 정보 아이템 스타일 조정 */
.info-item i {
  width: 1rem;
  text-align: center;
}

/* 반응형 */
@media (max-width: 768px) {
  .rank-badge-large {
    width: 3.5rem;
    height: 3.5rem;
  }

  .rank-number {
    font-size: 1.5rem;
  }
}
</style>
