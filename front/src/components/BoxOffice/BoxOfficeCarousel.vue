<template>
  <div class="performances-section">
    <!-- 로딩 스피너 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">데이터를 불러오는 중...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- 공연 목록 -->
    <div v-else>
      <div class="carousel-wrapper">
        <!-- 좌측 화살표 -->
        <button
          v-if="currentPage > 0"
          @click="prevPage"
          class="nav-arrow nav-arrow-left"
        >
          <i class="fas fa-chevron-left"></i>
        </button>

        <!-- 공연 목록 -->
        <div class="performances-grid">
          <template v-if="pageData.length > 0">
            <BoxOfficeCard
              v-for="perf in pageData"
              :key="perf.mt20id"
              :perf="perf"
            />
          </template>

          <!-- 데이터 없음 -->
          <div v-else class="empty-state">
            <i class="fas fa-exclamation-circle empty-icon"></i>
            <p class="empty-text">진행 중인 공연이 없습니다.</p>
          </div>
        </div>

        <!-- 우측 화살표 -->
        <button
          v-if="currentPage < totalPages - 1"
          @click="nextPage"
          class="nav-arrow nav-arrow-right"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>

      <!-- 페이지 인디케이터 -->
      <div class="page-indicator">
        <span>{{ currentPage + 1 }} / {{ totalPages }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBoxOffice } from '@/composables/useBoxOffice'
import BoxOfficeCard from './BoxOfficeCard.vue'

const {
  pageData,
  currentPage,
  totalPages,
  loading,
  error,
  prevPage,
  nextPage,
  load
} = useBoxOffice()

// 초기 데이터 로드
onMounted(() => {
  load()
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

/* 공연 목록 */
.performances-section {
  margin-bottom: 4rem;
}

.carousel-wrapper {
  position: relative;
  margin: 0 3rem;
}

.performances-grid {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 1rem 0;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.performances-grid::-webkit-scrollbar {
  display: none;
}

/* 네비게이션 화살표 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: white;
  color: #374151;
  border: none;
  border-radius: 50%;
  padding: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.5rem;
  height: 3.5rem;
}

.nav-arrow:hover {
  background: #6366f1;
  color: white;
}

.nav-arrow i {
  font-size: 1.5rem;
}

.nav-arrow-left {
  left: -1.5rem;
}

.nav-arrow-right {
  right: -1.5rem;
}

/* 페이지 인디케이터 */
.page-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}

.page-indicator span {
  color: #6b7280;
  font-weight: 500;
}

/* 빈 상태 */
.empty-state {
  width: 100%;
  text-align: center;
  padding: 5rem 0;
}

.empty-icon {
  font-size: 4rem;
  color: #9ca3af;
  margin-bottom: 1.5rem;
}

.empty-text {
  color: #6b7280;
  font-size: 1.125rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .carousel-wrapper {
    margin: 0 1rem;
  }

  .nav-arrow-left {
    left: -0.5rem;
  }

  .nav-arrow-right {
    right: -0.5rem;
  }
}
</style>
