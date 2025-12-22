<template>
  <div class="community">
    <!-- Header with title and create button -->
    <div class="community-header">
      <h1>커뮤니티</h1>
      <button @click="showCreateModal = true" class="create-btn">
        <i class="fas fa-pen"></i>
        글 작성
      </button>
    </div>

    <!-- Best Review Section -->
    <BestReviewSection />

    <!-- Board Type Tabs -->
    <div class="board-tabs">
      <button
        @click="handleBoardTypeChange('PERFORMANCE')"
        :class="['tab-btn', { active: currentBoardType === 'PERFORMANCE' }]"
      >
        <i class="fas fa-theater-masks"></i>
        공연글
      </button>
      <button
        @click="handleBoardTypeChange('GENERAL')"
        :class="['tab-btn', { active: currentBoardType === 'GENERAL' }]"
      >
        <i class="fas fa-comments"></i>
        자유/정보
      </button>
    </div>

    <!-- Category Chips -->
    <div class="category-chips">
      <button
        @click="handleCategoryChange(null)"
        :class="['chip', { active: communityStore.filters.category === null }]"
      >
        전체
      </button>
      <button
        v-for="cat in availableCategories"
        :key="cat.value"
        @click="handleCategoryChange(cat.value)"
        :class="['chip', { active: communityStore.filters.category === cat.value }]"
      >
        {{ cat.label }}
      </button>
    </div>

    <!-- Search and Sort -->
    <div class="controls">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="text"
          placeholder="제목, 내용 검색..."
        />
        <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <select v-model="communityStore.filters.ordering" @change="applyFilters" class="sort-select">
        <option value="-created_at">최신순</option>
        <option value="created_at">오래된순</option>
        <option value="-like_count">인기순</option>
      </select>
    </div>

    <!-- Article List -->
    <ArticleList
      :articles="articles"
      :loading="loading"
      :error="error"
      @like="toggleLike"
    />

    <!-- Create Article Modal -->
    <ArticleCreateModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="handleArticleCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCommunityStore } from '@/stores/communityStore'
import { storeToRefs } from 'pinia'
import ArticleList from '@/components/Community/ArticleList.vue'
import ArticleCreateModal from '@/components/Community/ArticleCreateModal.vue'
import BestReviewSection from '@/components/Community/BestReviewSection.vue'

const communityStore = useCommunityStore()
const { articles, loading, error } = storeToRefs(communityStore)

const currentBoardType = ref('PERFORMANCE')
const searchQuery = ref('')
const showCreateModal = ref(false)

// Available categories based on board_type
const availableCategories = computed(() => {
  if (currentBoardType.value === 'PERFORMANCE') {
    return [
      { value: 'REVIEW', label: '후기' },
      { value: 'EXPECTATION', label: '기대평' },
      { value: 'QNA', label: '질문' }
    ]
  } else {
    return [
      { value: 'FREE', label: '자유게시판' },
      { value: 'INFO', label: '정보공유' }
    ]
  }
})

const handleBoardTypeChange = (boardType) => {
  currentBoardType.value = boardType
  communityStore.setFilter('board_type', boardType)
  communityStore.setFilter('category', null) // Reset category when changing board type
  applyFilters()
}

const handleCategoryChange = (category) => {
  communityStore.setFilter('category', category)
  applyFilters()
}

const handleSearch = () => {
  communityStore.setFilter('search', searchQuery.value)
  applyFilters()
}

const clearSearch = () => {
  searchQuery.value = ''
  communityStore.setFilter('search', '')
  applyFilters()
}

const applyFilters = async () => {
  await communityStore.applyFilters()
}

const toggleLike = async (id) => {
  try {
    await communityStore.likeArticle(id)
  } catch (err) {
    console.error('좋아요 처리 실패:', err)
  }
}

const handleArticleCreated = async () => {
  showCreateModal.value = false
  await applyFilters()
}

onMounted(async () => {
  // Fetch best reviews
  await communityStore.fetchBestReviews(4)

  // Initialize with PERFORMANCE board type
  communityStore.setFilter('board_type', 'PERFORMANCE')
  await applyFilters()
})
</script>

<style scoped>
.community {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .community {
  color: #f3f4f6;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Board Type Tabs */
.board-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .board-tabs {
  border-bottom-color: #374151;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: transparent;
  color: #6b7280;
  border: none;
  border-bottom: 3px solid transparent;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: #6366f1;
}

.tab-btn.active {
  color: #6366f1;
  border-bottom-color: #6366f1;
}

:root.dark .tab-btn {
  color: #cbd5e1;
}

:root.dark .tab-btn.active {
  color: #e2e8f0;
  border-bottom-color: #4f46e5;
}

/* Category Chips */
.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.chip {
  padding: 0.5rem 1.25rem;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid transparent;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.chip:hover {
  background: #e5e7eb;
}

.chip.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

:root.dark .chip {
  background: #111827;
  color: #e2e8f0;
  border-color: #334155;
}

:root.dark .chip:hover {
  background: #1f2937;
  border-color: #475569;
}

:root.dark .chip.active {
  background: #4f46e5;
  border-color: #6366f1;
  color: #f8fafc;
}

/* Controls */
.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.3s;
}

.search-box:focus-within {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .search-box {
  background: #1f2937;
  border-color: #374151;
}

:root.dark .search-box:focus-within {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.search-box i {
  color: #9ca3af;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  color: #111827;
  font-size: 1rem;
  outline: none;
}

:root.dark .search-box input {
  color: #f3f4f6;
}

.search-box input::placeholder {
  color: #9ca3af;
}

.clear-btn {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.3s;
}

.clear-btn:hover {
  color: #6b7280;
}

.sort-select {
  padding: 0.75rem 1rem;
  background: #f9fafb;
  color: #111827;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.sort-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .sort-select {
  background: #1f2937;
  color: #f3f4f6;
  border-color: #374151;
}

:root.dark .sort-select:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .community {
    padding: 1rem;
  }

  .community-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }

  .tab-btn {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }

  .controls {
    flex-direction: column;
  }

  .sort-select {
    width: 100%;
  }
}
</style>
