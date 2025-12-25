<template>
  <BasePerformanceCard
    :performance="performance"
    :show-like-button="showLikeButton"
    :like-loading="likeLoading"
    :clickable="false"
    :show-hover-overlay="false"
    @click="handleClick"
    @toggle-like="handleLikeClick"
  >
    <!-- 장르 뱃지 오버레이 -->
    <template #badge>
      <span v-if="performance.genrenm" class="genre-badge-overlay card-badge-overlay">
        {{ performance.genrenm }}
      </span>
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
  showLikeButton: {
    type: Boolean,
    default: true
  },
  likeLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click', 'toggle-like'])

const handleClick = () => {
  emit('click', props.performance.mt20id)
}

const handleLikeClick = () => {
  emit('toggle-like', props.performance.mt20id)
}
</script>

<style scoped>
/* 장르 뱃지 오버레이 스타일 */
.genre-badge-overlay {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 4px;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
}

:root.dark .genre-badge-overlay {
  background: var(--badge-bg-light);
}

/* Backdrop-filter fallback */
@supports not (backdrop-filter: blur(8px)) {
  .genre-badge-overlay {
    background: rgba(0, 0, 0, 0.7);
  }

  :root.dark .genre-badge-overlay {
    background: rgba(255, 255, 255, 0.25);
  }
}
</style>
