<template>
  <div class="ranking-all-view">
    <div class="ranking-content">
      <!-- 페이지 헤더 -->
      <div class="page-header">
        <h1 class="page-title">
          <i class="fas fa-chart-line"></i>
          전체 공연 랭킹
        </h1>
        <p class="page-subtitle">
          KOPIS 예매상황판 기준 좌석수 Top 10
        </p>
      </div>

      <!-- 전체 랭킹 상세 컴포넌트 -->
      <AllRankingDetail />

      <!-- 뒤로 가기 버튼 -->
      <div class="back-button-container">
        <router-link to="/" class="back-button">
          <i class="fas fa-home"></i>
          <span>홈으로 돌아가기</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import AllRankingDetail from '@/components/BoxOffice/AllRankingDetail.vue'
</script>

<style scoped>
.ranking-all-view {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
}

.ranking-content {
  max-width: 1280px;
  margin: 0 auto;
}

/* 페이지 헤더 */
.page-header {
  text-align: center;
  margin-bottom: 4rem;
  padding-top: 2rem;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.page-title i {
  color: #6366f1;
}

.page-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
}

/* 뒤로 가기 버튼 */
.back-button-container {
  text-align: center;
  margin-top: 4rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  border-radius: 9999px;
  color: white;
  background: linear-gradient(to right, #6366f1, #9333ea);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

.back-button:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

/* 반응형 */
@media (max-width: 768px) {
  .ranking-all-view {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }
}
</style>
