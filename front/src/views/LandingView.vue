<template>
  <div class="landing-container">
    <!-- 1. 하이라이트 캐러셀 (전체 폭) -->
    <HighlightCarousel />

    <!-- 나머지 콘텐츠 (컨테이너 내부) -->
    <div class="landing-content">
      <!-- 2. 개인화 추천 섹션 (항상 표시, 비로그인 시 블러 처리) -->
      <RecommendationSection />

      <!-- 3. YouTube 공연 영상 섹션 -->
      <YouTubePlaylistSection />

      <!-- 4. 전체 랭킹 섹션 -->
      <AllRankingSection />

      <!-- 4. 장르별 랭킹 섹션 -->
      <GenreRankingSection />

      <!-- 전체 공연 보기 버튼 -->
      <div class="view-all-container">
        <router-link to="/performances" class="view-all-button">
          <span>전체 공연 목록 보기</span>
          <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import HighlightCarousel from '@/components/BoxOffice/HighlightCarousel.vue'
import AllRankingSection from '@/components/BoxOffice/AllRankingSection.vue'
import GenreRankingSection from '@/components/BoxOffice/GenreRankingSection.vue'
import RecommendationSection from '@/components/Recommendation/RecommendationSection.vue'
import YouTubePlaylistSection from '@/components/YouTube/YouTubePlaylistSection.vue'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
</script>

<style scoped>
/* 컨테이너 */
.landing-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
}

.landing-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 3rem 1rem;
}

/* 전체 보기 버튼 */
.view-all-container {
  text-align: center;
  margin-top: 4rem;
}

.view-all-button {
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

.view-all-button:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.view-all-button i {
  transition: transform 0.3s;
}

.view-all-button:hover i {
  transform: translateX(0.5rem);
}

/* 반응형 */
@media (max-width: 768px) {
  .landing-content {
    padding: 2rem 0.5rem;
  }

  .title {
    font-size: 2rem;
  }
}
</style>
