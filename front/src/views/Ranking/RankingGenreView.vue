<template>
  <div class="ranking-genre-view">
    <div class="ranking-content">
      <!-- 페이지 헤더 -->
      <div class="page-header">
        <h1 class="page-title">
          <i class="fas fa-theater-masks"></i>
          {{ currentGenreName }} 랭킹
        </h1>
        <p class="page-subtitle">
          {{ currentGenreName }} 장르 박스오피스 Top 10
        </p>
      </div>

      <!-- 장르 탭 -->
      <div class="genre-tabs-container">
        <div class="genre-tabs">
          <button
            v-for="genreItem in genres"
            :key="genreItem.code"
            @click="changeGenreTab(genreItem.code)"
            :class="['genre-tab', { active: currentGenreCode === genreItem.code }]"
          >
            {{ genreItem.name }}
          </button>
        </div>
      </div>

      <!-- 장르별 랭킹 상세 컴포넌트 -->
      <GenreRankingDetail
        :genreCode="currentGenreCode"
        :genreName="currentGenreName"
      />

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
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GenreRankingDetail from '@/components/BoxOffice/GenreRankingDetail.vue'

const route = useRoute()
const router = useRouter()

// 장르 목록
const genres = [
  { code: 'GGGA', name: '대중콘서트' },
  { code: 'BBBC', name: '뮤지컬' },
  { code: 'CCCA', name: '클래식' },
  { code: 'CCCD', name: '무용' },
  { code: 'AAAA', name: '연극' },
  { code: 'EEEB', name: '서커스/마술' }
]

// 현재 선택된 장르 코드
const currentGenreCode = ref(route.query.genre || 'BBBC')

// 현재 장르명
const currentGenreName = computed(() => {
  const found = genres.find(g => g.code === currentGenreCode.value)
  return found ? found.name : '뮤지컬'
})

// 장르 탭 변경
const changeGenreTab = (genreCode) => {
  router.push({ name: 'ranking-genre', query: { genre: genreCode } })
}

// URL 쿼리 파라미터 변경 감지
watch(() => route.query.genre, (newGenre) => {
  if (newGenre) {
    currentGenreCode.value = newGenre
  }
})
</script>

<style scoped>
.ranking-genre-view {
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
  margin-bottom: 3rem;
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
  color: #9333ea;
}

.page-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
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
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.genre-tab:hover {
  background: #f3f4f6;
  color: #111827;
}

.genre-tab.active {
  background: linear-gradient(to right, #9333ea, #6366f1);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
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
  background: linear-gradient(to right, #9333ea, #6366f1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

.back-button:hover {
  background: linear-gradient(to right, #7c3aed, #4f46e5);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

/* 반응형 */
@media (max-width: 768px) {
  .ranking-genre-view {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .genre-tabs {
    padding: 0.375rem;
    gap: 0.375rem;
  }

  .genre-tab {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
}
</style>
