<template>
  <div class="recommands-view">
    <div class="container">
      <!-- Header Section -->
      <div class="header-section">
        <h1 class="title">🤖 AI 공연 추천</h1>
        <p class="subtitle">
          원하는 감정이나 상황을 자유롭게 입력해보세요.<br>
          AI가 당신에게 딱 맞는 공연을 찾아드립니다.
        </p>
      </div>

      <!-- Search Section -->
      <div class="search-section">
        <div class="search-box">
          <input
            v-model="query"
            @keyup.enter="handleSearch"
            type="text"
            placeholder="예: 신나는 공연 추천해줘, 우울할 때 위로가 되는 공연, 데이트하기 좋은 공연..."
            class="search-input"
            :disabled="loading"
          />
          <button
            @click="handleSearch"
            :disabled="loading || !query.trim()"
            class="search-button"
          >
            <i v-if="!loading" class="fas fa-search"></i>
            <i v-else class="fas fa-spinner fa-spin"></i>
            {{ loading ? '검색 중...' : '검색' }}
          </button>
        </div>

        <!-- Search Suggestions -->
        <div class="search-suggestions">
          <span class="suggestion-label">추천 검색어:</span>
          <button
            v-for="suggestion in searchSuggestions"
            :key="suggestion"
            @click="selectSuggestion(suggestion)"
            class="suggestion-chip"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>

      <!-- AI Comment Section -->
      <transition name="fade">
        <div v-if="aiComment" class="ai-comment-section">
          <div class="ai-avatar">
            <i class="fas fa-robot"></i>
          </div>
          <div class="comment-bubble">
            <p class="comment-text">{{ aiComment }}</p>
          </div>
        </div>
      </transition>

      <!-- Error Message -->
      <transition name="fade">
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>
      </transition>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="results-grid">
        <div v-for="i in 10" :key="i" class="skeleton-card">
          <div class="skeleton-poster"></div>
          <div class="skeleton-title"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text short"></div>
        </div>
      </div>

      <!-- Search Results -->
      <transition name="fade">
        <div v-if="!loading && searchResults.length > 0" class="results-section">
          <h2 class="results-title">
            <i class="fas fa-magic"></i>
            추천 공연 목록
            <span class="results-count">{{ searchResults.length }}개</span>
          </h2>

          <div class="results-grid">
            <AISearchCard
              v-for="(performance, index) in searchResults"
              :key="performance.mt20id"
              :performance="performance"
              :rank="index + 1"
              @click="goToDetail"
              @toggle-like="handleToggleLike"
            />
          </div>
        </div>
      </transition>

      <!-- Empty State -->
      <div v-if="!loading && !error && searchResults.length === 0 && lastQuery" class="empty-state">
        <i class="fas fa-search"></i>
        <p>검색 결과가 없습니다.</p>
        <p class="empty-hint">다른 검색어로 시도해보세요.</p>
      </div>

      <!-- Initial State -->
      <div v-if="!loading && !lastQuery" class="initial-state">
        <i class="fas fa-wand-magic-sparkles"></i>
        <p>AI에게 원하는 공연을 설명해보세요</p>
        <div class="example-searches">
          <p class="example-title">검색 예시:</p>
          <ul>
            <li>"시험 기간 스트레스 풀고 싶어"</li>
            <li>"아이와 함께 볼만한 공연"</li>
            <li>"로맨틱한 분위기의 공연"</li>
            <li>"웅장하고 감동적인 작품"</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAISearchStore } from '@/stores/aiSearchStore'
import { usePerformanceStore } from '@/stores/performanceStore'
import AISearchCard from '@/components/AISearch/AISearchCard.vue'

const router = useRouter()
const aiSearchStore = useAISearchStore()
const performanceStore = usePerformanceStore()

// State
const query = ref('')

// Search suggestions
const searchSuggestions = [
  '신나는 공연',
  '감동적인 뮤지컬',
  '데이트하기 좋은',
  '아이랑 보기 좋은',
  '우울할 때 위로되는'
]

// Reactive store values
const { searchResults, aiComment, loading, error, lastQuery } = storeToRefs(aiSearchStore)

// Methods
const handleSearch = async () => {
  if (!query.value.trim()) return

  try {
    await aiSearchStore.searchPerformances(query.value)
  } catch (err) {
    console.error('검색 실패:', err)
  }
}

const selectSuggestion = (suggestion) => {
  query.value = suggestion
  handleSearch()
}

const goToDetail = (performanceId) => {
  router.push({ name: 'performance-detail', params: { id: performanceId } })
}

const handleToggleLike = async (performanceId) => {
  try {
    await performanceStore.toggleLike(performanceId)

    // AI 검색 결과에서도 좋아요 상태 업데이트
    const performance = searchResults.value.find(p => p.mt20id === performanceId)
    if (performance) {
      performance.is_liked = !performance.is_liked
    }
  } catch (err) {
    console.error('찜하기 실패:', err)
    if (err.message === '로그인이 필요합니다.') {
      alert('로그인이 필요한 기능입니다.')
      router.push({ name: 'login' })
    }
  }
}
</script>

<style scoped>
.recommands-view {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header Section */
.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Search Section */
.search-section {
  max-width: 800px;
  margin: 0 auto 3rem;
}

.search-box {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid var(--border-color);
  border-radius: 2rem;
  font-size: 1rem;
  background: var(--card-surface);
  color: var(--text-primary);
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.search-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-button {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Search Suggestions */
.search-suggestions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.suggestion-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.suggestion-chip {
  padding: 0.5rem 1rem;
  background: var(--card-surface);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.suggestion-chip:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* AI Comment Section */
.ai-comment-section {
  max-width: 800px;
  margin: 0 auto 3rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.ai-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.comment-bubble {
  flex: 1;
  background: var(--card-surface);
  border: 2px solid var(--primary-color);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.comment-text {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0;
}

/* Error Message */
.error-message {
  max-width: 800px;
  margin: 0 auto 2rem;
  padding: 1rem 1.5rem;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 0.5rem;
  color: #c33;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Results Section */
.results-section {
  margin-top: 3rem;
}

.results-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.results-count {
  font-size: 1rem;
  font-weight: 400;
  color: var(--text-secondary);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  grid-auto-rows: 1fr;
}

/* Skeleton Loading */
.skeleton-card {
  background: var(--card-surface);
  border-radius: 0.75rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
}

.skeleton-poster {
  width: 100%;
  aspect-ratio: 3/4;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.skeleton-title {
  height: 1.25rem;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.skeleton-text {
  height: 1rem;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.skeleton-text.short {
  width: 60%;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

:root.dark .skeleton-poster,
:root.dark .skeleton-title,
:root.dark .skeleton-text {
  background: linear-gradient(90deg, #374151 25%, #4b5563 50%, #374151 75%);
  background-size: 200% 100%;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.empty-state p {
  font-size: 1.125rem;
  margin: 0.5rem 0;
}

.empty-hint {
  font-size: 0.875rem;
  opacity: 0.7;
}

/* Initial State */
.initial-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.initial-state i {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.initial-state > p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.example-searches {
  max-width: 500px;
  margin: 0 auto;
  text-align: left;
  background: var(--card-surface);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  padding: 2rem;
}

.example-title {
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.example-searches ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.example-searches li {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.example-searches li:last-child {
  border-bottom: none;
}

.example-searches li::before {
  content: '💡 ';
  margin-right: 0.5rem;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .search-box {
    flex-direction: column;
  }

  .search-button {
    width: 100%;
    justify-content: center;
  }

  .results-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>
