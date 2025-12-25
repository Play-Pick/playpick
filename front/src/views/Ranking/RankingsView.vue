<template>
  <div class="rankings-view">
    <div class="rankings-container">
      <!-- 페이지 헤더 -->
      <div class="page-header">
        <h1 class="page-title">
          <i class="fas fa-trophy"></i>
          공연 랭킹
        </h1>
        <p class="page-subtitle">실시간 박스오피스 순위</p>
      </div>

      <!-- 메인 탭 (전체 / 장르별) -->
      <div class="main-tabs-container">
        <div class="main-tabs">
          <button
            @click="changeMainTab('all')"
            :class="['main-tab', { active: currentMainTab === 'all' }]"
          >
            <i class="fas fa-chart-line"></i>
            전체 랭킹
          </button>
          <button
            @click="changeMainTab('genre')"
            :class="['main-tab', { active: currentMainTab === 'genre' }]"
          >
            <i class="fas fa-theater-masks"></i>
            장르별 랭킹
          </button>
        </div>
      </div>

      <!-- 전체 랭킹 탭 콘텐츠 -->
      <div v-if="currentMainTab === 'all'" class="tab-content">
        <AllRankingDetail />
      </div>

      <!-- 장르별 랭킹 탭 콘텐츠 -->
      <div v-else-if="currentMainTab === 'genre'" class="tab-content">
        <!-- 장르 선택 탭 -->
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

        <!-- 장르별 랭킹 상세 -->
        <GenreRankingDetail
          :genreCode="currentGenreCode"
          :genreName="currentGenreName"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AllRankingDetail from '@/components/BoxOffice/AllRankingDetail.vue'
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

// 현재 메인 탭 ('all' or 'genre')
const currentMainTab = ref(route.query.tab || 'all')

// 현재 장르 코드 (장르별 랭킹 탭용)
const currentGenreCode = ref(route.query.genre || 'BBBC')

// 현재 장르명
const currentGenreName = computed(() => {
  const found = genres.find(g => g.code === currentGenreCode.value)
  return found ? found.name : '뮤지컬'
})

// 메인 탭 변경 (전체 ↔ 장르별)
const changeMainTab = (tab) => {
  if (tab === 'all') {
    router.push({ name: 'rankings', query: { tab: 'all' } })
  } else {
    router.push({
      name: 'rankings',
      query: { tab: 'genre', genre: currentGenreCode.value }
    })
  }
}

// 장르 탭 변경
const changeGenreTab = (genreCode) => {
  router.push({
    name: 'rankings',
    query: { tab: 'genre', genre: genreCode }
  })
}

// URL 쿼리 파라미터 변경 감지
watch(() => route.query, (newQuery) => {
  currentMainTab.value = newQuery.tab || 'all'
  if (newQuery.genre) {
    currentGenreCode.value = newQuery.genre
  }
}, { immediate: true })
</script>

<style scoped>
.rankings-view {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
}

.rankings-container {
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
  color: #f59e0b;
}

.page-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
}

/* 메인 탭 (전체 / 장르별) */
.main-tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.main-tabs {
  display: inline-flex;
  background: white;
  border-radius: 9999px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  gap: 0.5rem;
}

.main-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border-radius: 9999px;
  font-weight: 700;
  font-size: 1.0625rem;
  border: none;
  background: none;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.main-tab:hover {
  background: #f3f4f6;
  color: #111827;
}

.main-tab.active {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.main-tab i {
  font-size: 1.125rem;
}

/* 탭 콘텐츠 */
.tab-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* 반응형 */
@media (max-width: 768px) {
  .rankings-view {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .main-tabs {
    padding: 0.375rem;
    gap: 0.375rem;
  }

  .main-tab {
    padding: 0.75rem 1.5rem;
    font-size: 0.9375rem;
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
