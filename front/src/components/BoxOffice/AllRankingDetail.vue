<template>
  <div class="all-ranking-detail">
    <!-- 로딩 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">랭킹 데이터를 불러오는 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- 랭킹 내용 -->
    <div v-else-if="allRankings.length > 0" class="ranking-content">
      <!-- Top 1-3: 큰 카드 -->
      <div class="top-three-grid">
        <RankingCard
          v-for="perf in topThree"
          :key="perf.mt20id"
          :perf="perf"
          :like-loading="likeLoading"
          @toggle-like="handleToggleLike"
        />
      </div>

      <!-- 4-10: 리스트 -->
      <div v-if="restRankings.length > 0" class="ranking-list">
        <RankingListItem
          v-for="perf in restRankings"
          :key="perf.mt20id"
          :perf="perf"
          :like-loading="likeLoading"
          @toggle-like="handleToggleLike"
        />
      </div>
    </div>

    <!-- 데이터 없음 -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox empty-icon"></i>
      <p class="empty-text">랭킹 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAllRanking } from '@/composables/useAllRanking'
import { useUserTracking } from '@/composables/useUserTracking'
import RankingCard from './RankingCard.vue'
import RankingListItem from './RankingListItem.vue'

const { allRankings, loading, error, loadAllRankings } = useAllRanking()
const { toggleLike, likeLoading } = useUserTracking()

// Top 1-3
const topThree = computed(() => allRankings.value.slice(0, 3))

// 4-10
const restRankings = computed(() => allRankings.value.slice(3, 10))

// 찜하기 토글 핸들러
const handleToggleLike = async (performanceId) => {
  try {
    const result = await toggleLike(performanceId)

    // Update local performance data
    const performance = allRankings.value.find(p => p.mt20id === performanceId)
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

// 데이터 로드
onMounted(() => {
  loadAllRankings()
})
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
  border-top-color: #6366f1;
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
