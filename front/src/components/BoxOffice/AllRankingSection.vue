<template>
  <section class="all-ranking-section">
    <!-- 섹션 헤더 -->
    <div class="section-header">
      <h2 class="section-title">
        <i class="fas fa-chart-line"></i>
        전체 랭킹
      </h2>
      <p class="section-subtitle">좌석수 기준 박스오피스 Top 5</p>
    </div>

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

    <!-- 공연 캐러셀 (Top 10) -->
    <div v-else-if="allRankings.length > 0" class="ranking-carousel">
      <div class="carousel-wrapper">
        <!-- 좌측 화살표 -->
        <button
          v-if="canGoPrev"
          @click="goToPrevPage"
          class="nav-arrow nav-arrow-left"
          aria-label="이전 공연 보기"
        >
          <i class="fas fa-chevron-left"></i>
        </button>

        <!-- 공연 목록 -->
        <div class="performances-scroll">
          <BoxOfficeCard
            v-for="perf in displayedRankings"
            :key="perf.mt20id"
            :perf="perf"
            :like-loading="likeLoading"
            @toggle-like="handleToggleLike"
          />
        </div>

        <!-- 우측 화살표 -->
        <button
          v-if="canGoNext"
          @click="goToNextPage"
          class="nav-arrow nav-arrow-right"
          aria-label="다음 공연 보기"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>

      <!-- 더보기 버튼 -->
      <div class="view-more-container">
        <router-link to="/rankings/all" class="view-more-button">
          <span>전체 랭킹 더보기</span>
          <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>
    </div>

    <!-- 데이터 없음 -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox empty-icon"></i>
      <p class="empty-text">랭킹 데이터가 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAllRanking } from '@/composables/useAllRanking'
import { usePerformanceStore } from '@/stores/performanceStore'
import BoxOfficeCard from './BoxOfficeCard.vue'

const { allRankings, loading, error, loadAllRankings } = useAllRanking()
const performanceStore = usePerformanceStore()
const { toggleLike, likeLoading } = performanceStore

// 페이지네이션 상태
const currentPage = ref(0) // 0: 1-5위, 1: 6-10위
const itemsPerPage = 5

// 현재 페이지에 표시할 랭킹
const displayedRankings = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return allRankings.value.slice(start, end)
})

// 전체 페이지 수
const totalPages = computed(() => Math.ceil(allRankings.value.length / itemsPerPage))

// 화살표 표시 여부
const canGoPrev = computed(() => currentPage.value > 0)
const canGoNext = computed(() => currentPage.value < totalPages.value - 1)

// 페이지 이동
const goToPrevPage = () => {
  if (canGoPrev.value) {
    currentPage.value--
  }
}

const goToNextPage = () => {
  if (canGoNext.value) {
    currentPage.value++
  }
}

// 찜하기 토글 (Store 사용 - 전역 상태 관리)
const handleToggleLike = async (performanceId) => {
  try {
    await toggleLike(performanceId)
    // Store가 자동으로 모든 목록의 상태를 업데이트하므로
    // 별도의 로컬 상태 업데이트 불필요
  } catch (err) {
    if (err.message === '로그인이 필요합니다.') {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('찜하기 실패:', err)
    }
  }
}

// 데이터 로드
onMounted(async () => {
  await loadAllRankings()
})
</script>

<style scoped>
/* 섹션 */
.all-ranking-section {
  margin-bottom: 6rem;
}

/* 섹션 헤더 */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--card-text-primary);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.section-title i {
  color: var(--card-accent);
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
}

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
  border-top-color: var(--card-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: var(--card-text-secondary);
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

/* 캐러셀 */
.ranking-carousel {
  max-width: 1280px;
  margin: 0 auto;
}

.carousel-wrapper {
  position: relative;
  padding: 0 3.5rem;
}

/* 공연 그리드 */
.performances-scroll {
  display: flex;
  gap: 1.2rem;
  padding: 1rem 0;
  justify-content: space-between;
}

/* 카드 크기 조정: 5개가 딱 맞게 */
.performances-scroll :deep(.performance-card),
.performances-scroll :deep(.boxoffice-card) {
  flex-shrink: 0;
  width: calc((100% - (1.2rem * 4)) / 5) !important;
  max-width: calc((100% - (1.2rem * 4)) / 5) !important;
  min-width: 0;
}

/* 네비게이션 화살표 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: white;
  border: none;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

:root.dark .nav-arrow {
  background: white !important;
}

.nav-arrow:hover {
  background: #6366f1;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-50%) scale(1.1);
}

:root.dark .nav-arrow:hover {
  background: white !important;
}

.nav-arrow-left {
  left: 0;
}

.nav-arrow-right {
  right: 0;
}

.nav-arrow i {
  font-size: 1.25rem;
  color: #111827;
}

:root.dark .nav-arrow i {
  color: #111827 !important;
}

.nav-arrow:hover i {
  color: white;
}

:root.dark .nav-arrow:hover i {
  color: #111827 !important;
}

/* 더보기 버튼 */
.view-more-container {
  text-align: center;
  margin-top: 3rem;
}

.view-more-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  border-radius: 9999px;
  color: white;
  background: linear-gradient(to right, var(--card-accent), var(--card-accent-hover));
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

:root.dark .view-more-button {
  background: white !important;
  color: #111827 !important;
}

.view-more-button:hover {
  background: linear-gradient(to right, var(--card-accent-hover), #7c3aed);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

:root.dark .view-more-button:hover {
  background: white !important;
  color: #111827 !important;
}

.view-more-button i {
  transition: transform 0.3s;
}

.view-more-button:hover i {
  transform: translateX(0.5rem);
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
  .carousel-wrapper {
    padding: 0 2.5rem;
  }

  .performances-scroll {
    gap: 1rem;
    overflow-x: auto;
  }

  .performances-scroll :deep(.performance-card),
  .performances-scroll :deep(.boxoffice-card) {
    width: 15rem !important;
    max-width: 15rem !important;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .carousel-wrapper {
    padding: 0 2.5rem;
  }

  .nav-arrow {
    width: 2.5rem;
    height: 2.5rem;
  }

  .nav-arrow i {
    font-size: 1rem;
  }

  .performances-scroll {
    gap: 1rem;
  }

  .performances-scroll :deep(.performance-card),
  .performances-scroll :deep(.boxoffice-card) {
    width: 14rem !important;
    max-width: 14rem !important;
  }

  .view-more-button {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .carousel-wrapper {
    padding: 0 2rem;
  }

  .nav-arrow {
    width: 2rem;
    height: 2rem;
  }

  .nav-arrow i {
    font-size: 0.875rem;
  }

  .performances-scroll :deep(.performance-card),
  .performances-scroll :deep(.boxoffice-card) {
    width: 12rem !important;
    max-width: 12rem !important;
  }
}
</style>
