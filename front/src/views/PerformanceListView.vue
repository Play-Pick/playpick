<template>
  <div class="performance-list">
    <div class="header">
      <h1>
        <i class="fas fa-theater-masks"></i> 공연 목록
      </h1>
      <p class="subtitle">다양한 공연 정보를 확인하세요</p>
    </div>

    <!-- 필터 -->
    <PerformanceFilters
      v-model:selectedGenre="selectedGenre"
      v-model:searchQuery="searchQuery"
      :genres="genres"
      @filter="filterPerformances"
    />

    <!-- 로딩 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <!-- 공연 목록 -->
    <PerformanceGrid
      v-else
      :performances="performances"
      @card-click="goToDetail"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { usePerformanceList } from '@/composables/usePerformanceList'
import PerformanceFilters from '@/components/Performance/PerformanceFilters.vue'
import PerformanceGrid from '@/components/Performance/PerformanceGrid.vue'

const router = useRouter()

const {
  performances,
  genres,
  loading,
  error,
  selectedGenre,
  searchQuery,
  filterPerformances
} = usePerformanceList()

const goToDetail = (id) => {
  router.push({ name: 'performance-detail', params: { id } })
}
</script>

<style scoped>
.performance-list {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
  transition: background 0.3s;
}

:root.dark .performance-list {
  background: linear-gradient(to bottom, #1a1a1a, #0f0f0f);
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

:root.dark .header h1 {
  color: #f3f4f6;
}

.header h1 i {
  color: #6366f1;
  margin-right: 0.5rem;
  transition: color 0.3s;
}

:root.dark .header h1 i {
  color: #818cf8;
}

.subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .subtitle {
  color: #9ca3af;
}

.loading,
.error {
  text-align: center;
  padding: 5rem 2rem;
}

.loading .spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #6b7280;
  font-size: 1.125rem;
  transition: color 0.3s;
}

:root.dark .loading p {
  color: #9ca3af;
}

.error {
  color: #dc2626;
}

.error i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

@media (max-width: 768px) {
  .performance-list {
    padding: 1rem;
  }

  .header h1 {
    font-size: 2rem;
  }
}
</style>
