<template>
  <BasePerformanceCard
    :performance="performance"
    :show-like-button="showLikeButton"
    :like-loading="likeLoading"
    card-class="recommendation-card"
    @toggle-like="handleLikeClick"
  >
    <!-- 추천 이유 뱃지 -->
    <template #badge>
      <div v-if="reason" class="reason-badge card-badge-overlay">
        <i class="fas fa-sparkles"></i>
        <span>{{ reason }}</span>
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
</script>

<style scoped>
/* Recommendation 카드 커스텀 */
.recommendation-card {
  min-height: 520px; /* 고정된 카드 높이로 레이아웃 균일화 */
}

/* 추천 이유 뱃지 */
.reason-badge {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 4px;
  padding: 0.375rem 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
}

:root.dark .reason-badge {
  background: var(--badge-bg-light);
}

.reason-badge i {
  font-size: 0.75rem;
}

/* Backdrop-filter fallback */
@supports not (backdrop-filter: blur(8px)) {
  .reason-badge {
    background: rgba(0, 0, 0, 0.7);
  }

  :root.dark .reason-badge {
    background: rgba(255, 255, 255, 0.25);
  }
}
</style>
