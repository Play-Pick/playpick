<template>
  <section class="genre-ranking-section">
    <!-- 섹션 헤더 -->
    <div class="section-header">
      <h2 class="section-title">
        <i class="fas fa-theater-masks"></i>
        장르별 랭킹
      </h2>
      <p class="section-subtitle">장르를 선택하여 인기 공연을 확인하세요</p>
    </div>

    <!-- 장르 탭 -->
    <div class="genre-tabs-container">
      <div class="genre-tabs">
        <button
          v-for="genreItem in genres"
          :key="genreItem.code"
          @click="handleGenreChange(genreItem.code)"
          :class="['genre-tab', { active: currentGenre === genreItem.code }]"
        >
          {{ genreItem.name }}
        </button>
      </div>
    </div>

    <!-- 에러 -->
    <div v-if="error && !loading" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- 공연 캐러셀 (Top 10) -->
    <div v-else-if="allPerformances.length > 0 || loading" class="genre-carousel">
      <!-- 로딩 오버레이 -->
      <div v-if="loading" class="loading-overlay">
        <div class="spinner"></div>
      </div>

      <div class="carousel-wrapper" :class="{ 'is-loading': loading }">
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
            v-for="perf in genrePerformances"
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
        <router-link
          :to="{ name: 'ranking-genre', query: { genre: currentGenre } }"
          class="view-more-button"
        >
          <span>{{ currentGenreName }} 더보기</span>
          <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>
    </div>

    <!-- 데이터 없음 -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox empty-icon"></i>
      <p class="empty-text">{{ currentGenreName }} 랭킹 데이터가 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBoxOffice } from '@/composables/useBoxOffice'
import { usePerformanceStore } from '@/stores/performanceStore'
import BoxOfficeCard from './BoxOfficeCard.vue'

// 장르 목록 (기타 추가)
const genres = [
  { code: 'GGGA', name: '대중콘서트' },
  { code: 'BBBC', name: '뮤지컬' },
  { code: 'CCCA', name: '클래식' },
  { code: 'CCCD', name: '무용' },
  { code: 'AAAA', name: '연극' },
  { code: 'ETC', name: '기타' }
]

// 기타 장르명 리스트 (서커스/마술, 한국음악 등)
const ETC_GENRES = ['서커스/마술', '한국음악(국악)', '복합', '오페라', '아동']

const { genre: currentGenre, allPerformances, loading, error, load, changeGenre: changeGenreFunc } = useBoxOffice()
const performanceStore = usePerformanceStore()
const { toggleLike, likeLoading } = performanceStore

// 페이지네이션 상태
const currentPage = ref(0) // 0: 1-5위, 1: 6-10위
const itemsPerPage = 5

// 현재 장르명
const currentGenreName = computed(() => {
  const found = genres.find(g => g.code === currentGenre.value)
  return found ? found.name : '전체'
})

// 현재 페이지에 표시할 랭킹
const genrePerformances = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return allPerformances.value.slice(start, end)
})

// 전체 페이지 수
const totalPages = computed(() => Math.ceil(allPerformances.value.length / itemsPerPage))

// 화살표 표시 여부
const canGoPrev = computed(() => currentPage.value > 0)
const canGoNext = computed(() => currentPage.value < totalPages.value - 1)

// 찜하기 토글 (Store 사용 - 전역 상태 관리)
const handleToggleLike = async (performanceId) => {
  try {
    await toggleLike(performanceId)
    // Store가 자동으로 모든 목록의 상태를 업데이트
  } catch (err) {
    if (err.message === '로그인이 필요합니다.') {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('찜하기 실패:', err)
    }
  }
}

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

const handleGenreChange = async (genreCode) => {
  currentPage.value = 0 // 장르 변경 시 첫 페이지로
  if (genreCode === 'ETC') {
    // 기타 장르는 별도 처리 (백엔드 수정 필요)
    // 임시로 서커스/마술 표시
    await changeGenreFunc('EEEB')
  } else {
    await changeGenreFunc(genreCode)
  }
}

// 초기 로드
onMounted(() => {
  load()
})
</script>

<style scoped>
/* 섹션 */
.genre-ranking-section {
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
  color: #9333ea;
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
}

/* 장르 탭 */
.genre-tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.genre-tabs {
  display: inline-flex;
  background: white;
  border-radius: 9999px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.genre-tab {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.9375rem;
  border: none;
  background: none;
  color: var(--card-text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.genre-tab:hover {
  background: #f3f4f6;
  color: var(--card-text-primary);
}

.genre-tab.active {
  background: linear-gradient(to right, #9333ea, #6366f1);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

/* 로딩 오버레이 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  border-radius: 1rem;
}

:root.dark .loading-overlay {
  background: rgba(26, 26, 26, 0.8);
}

.spinner {
  display: inline-block;
  width: 3.5rem;
  height: 3.5rem;
  border: 4px solid #e5e7eb;
  border-top-color: #9333ea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

:root.dark .spinner {
  border-color: #374151;
  border-top-color: #818cf8;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.carousel-wrapper.is-loading {
  opacity: 0.4;
  pointer-events: none;
}

/* 에러 */
.error-container {
  text-align: center;
  padding: 4rem 0;
}

.error-icon {
  font-size: 3.5rem;
  color: #ef4444;
  margin-bottom: 1.25rem;
}

.error-text {
  color: #dc2626;
  font-size: 1.0625rem;
}

/* 캐러셀 */
.genre-carousel {
  max-width: 1280px;
  margin: 0 auto;
  position: relative;
  min-height: 400px;
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

.nav-arrow:hover i {
  color: white;
}

:root.dark .nav-arrow:hover i {
  color: #111827 !important;
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

/* 더보기 버튼 */
.view-more-container {
  text-align: center;
  margin-top: 3rem;
}

.view-more-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 2rem;
  font-size: 1.0625rem;
  font-weight: 700;
  border-radius: 9999px;
  color: white;
  background: linear-gradient(to right, #9333ea, #6366f1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

:root.dark .view-more-button {
  background: white !important;
  color: #111827 !important;
}

.view-more-button:hover {
  background: linear-gradient(to right, #7c3aed, #4f46e5);
  box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.2);
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
  transform: translateX(0.375rem);
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 4rem 0;
}

.empty-icon {
  font-size: 4.5rem;
  color: #d1d5db;
  margin-bottom: 1.25rem;
}

.empty-text {
  font-size: 1.125rem;
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

  .genre-tabs {
    padding: 0.375rem;
    gap: 0.375rem;
  }

  .genre-tab {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
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
