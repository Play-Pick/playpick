<template>
  <div class="performances-grid">
    <PerformanceCard
      v-for="performance in performances"
      :key="performance.mt20id"
      :performance="performance"
      :like-loading="likeLoading"
      @click="handleCardClick"
      @toggle-like="handleToggleLike"
    />
  </div>
</template>

<script setup>
import { useUserTracking } from '@/composables/useUserTracking'
import PerformanceCard from './PerformanceCard.vue'

const props = defineProps({
  performances: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['card-click'])

const { toggleLike, likeLoading } = useUserTracking()

const handleCardClick = (id) => {
  emit('card-click', id)
}

const handleToggleLike = async (performanceId) => {
  try {
    const result = await toggleLike(performanceId)
    
    // Update local performance data
    const performance = props.performances.find(p => p.mt20id === performanceId)
    if (performance) {
      performance.is_liked = result.is_liked
      performance.like_count = result.like_count
    }
  } catch (err) {
    if (err.message === '로그인이 필요합니다.') {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('찜하기 실패:', err)
    }
  }
}
</script>

<style scoped>
.performances-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .performances-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>
