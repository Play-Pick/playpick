<template>
  <div class="genre-ranking-detail">
    <!-- 로딩 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">{{ genreName }} 랭킹을 불러오는 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- 랭킹 내용 -->
    <div v-else-if="performances.length > 0" class="ranking-content">
      <!-- Top 1-3: 큰 카드 -->
      <div class="top-three-grid">
        <RankingCard
          v-for="perf in topThree"
          :key="perf.mt20id"
          :perf="perf"
        />
      </div>

      <!-- 4-10: 리스트 -->
      <div v-if="restPerformances.length > 0" class="ranking-list">
        <RankingListItem
          v-for="perf in restPerformances"
          :key="perf.mt20id"
          :perf="perf"
        />
      </div>
    </div>

    <!-- 데이터 없음 -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox empty-icon"></i>
      <p class="empty-text">{{ genreName }} 랭킹 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useBoxOffice } from '@/composables/useBoxOffice'
import RankingCard from './RankingCard.vue'
import RankingListItem from './RankingListItem.vue'

const props = defineProps({
  genreCode: {
    type: String,
    required: true
  },
  genreName: {
    type: String,
    required: true
  }
})

const { allPerformances: performances, loading, error, changeGenre } = useBoxOffice()

// Top 1-3
const topThree = computed(() => performances.value.slice(0, 3))

// 4-10
const restPerformances = computed(() => performances.value.slice(3, 10))

// 장르 변경 시 데이터 로드
watch(() => props.genreCode, async (newGenre) => {
  if (newGenre) {
    await changeGenre(newGenre)
  }
}, { immediate: true })
</script>

<style scoped>
/* 로딩 */
.loading-container {
  text-align: center;
  padding: 5rem 0;
}

.spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #9333ea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: #6b7280;
  font-size: 1.125rem;
  font-weight: 500;
}

/* 에러 */
.error-container {
  text-align: center;
  padding: 5rem 0;
}

.error-icon {
  font-size: 4rem;
  color: #ef4444;
  margin-bottom: 1.5rem;
}

.error-text {
  color: #dc2626;
  font-size: 1.125rem;
}

/* 랭킹 내용 */
.ranking-content {
  max-width: 1280px;
  margin: 0 auto;
}

/* Top 3 그리드 */
.top-three-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
}

/* 랭킹 리스트 */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 5rem 0;
}

.empty-icon {
  font-size: 5rem;
  color: #d1d5db;
  margin-bottom: 1.5rem;
}

.empty-text {
  font-size: 1.25rem;
  color: #9ca3af;
}

/* 반응형 */
@media (max-width: 1024px) {
  .top-three-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .top-three-grid > :last-child:nth-child(3) {
    grid-column: 1 / -1;
    max-width: 50%;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .top-three-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .top-three-grid > :last-child:nth-child(3) {
    max-width: 100%;
  }

  .ranking-list {
    gap: 0.75rem;
  }
}
</style>
