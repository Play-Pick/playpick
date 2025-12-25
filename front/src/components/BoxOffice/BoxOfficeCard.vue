<template>
  <BasePerformanceCard
    :performance="perf"
    :show-like-button="showLikeButton"
    :like-loading="likeLoading"
    card-class="boxoffice-card"
    @toggle-like="handleLikeClick"
  >
    <!-- 순위 뱃지 -->
    <template #badge>
      <div :class="['rank-badge card-badge-overlay', getRankBadgeClass(perf.rank)]">
        <i class="fas fa-trophy"></i>{{ perf.rank }}
      </div>
    </template>

    <!-- 하단 장르 태그 -->
    <template #footer>
      <div class="genre-tag">
        <span>{{ perf.genrenm || '' }}</span>
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

// 순위 뱃지 클래스
const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return 'rank-default'
}
</script>

<style scoped>
/* BoxOffice 카드 커스텀 */
.boxoffice-card {
  flex-shrink: 0;
  width: 16rem;
}

/* BasePerformanceCard의 기본 스타일 오버라이드 */
.boxoffice-card :deep(.card-poster) {
  padding-top: 125%; /* 4:5 비율로 변경 (더 작게) */
}

.boxoffice-card :deep(.card-content) {
  padding: 1.25rem;
}

.boxoffice-card :deep(.performance-title) {
  font-size: 1.125rem;
  height: 3.5rem;
  min-height: 3.5rem;
  margin-bottom: 0.75rem;
}

.boxoffice-card :deep(.performance-info) {
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

/* 순위 뱃지 - 컴팩트 버전 */
.rank-badge {
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
}

.rank-gold {
  background: linear-gradient(to right, #fbbf24, #f59e0b);
}

.rank-silver {
  background: linear-gradient(to right, #d1d5db, #9ca3af);
}

.rank-bronze {
  background: linear-gradient(to right, #fb923c, #ea580c);
}

.rank-default {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
}

:root.dark .rank-default {
  background: var(--badge-bg-light);
}

.rank-badge i {
  font-size: 0.75rem;
}

/* 장르 태그 */
.genre-tag span {
  display: inline-block;
  background: var(--card-chip-bg);
  color: var(--card-accent);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>
