<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <h2>글 작성</h2>
        <button @click="$emit('close')" class="close-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Step 1: Board Type Selection -->
      <div v-if="step === 1" class="step-content">
        <h3>게시판 선택</h3>
        <div class="board-type-selection">
          <button
            @click="selectBoardType('PERFORMANCE')"
            :class="['board-card', { selected: formData.board_type === 'PERFORMANCE' }]"
          >
            <i class="fas fa-theater-masks"></i>
            <h4>공연글</h4>
            <p>공연 후기, 기대평, 질문을 작성합니다</p>
          </button>
          <button
            @click="selectBoardType('GENERAL')"
            :class="['board-card', { selected: formData.board_type === 'GENERAL' }]"
          >
            <i class="fas fa-comments"></i>
            <h4>일반글</h4>
            <p>자유롭게 의견을 나누고 정보를 공유합니다</p>
          </button>
        </div>
      </div>

      <!-- Step 2: Performance Search (PERFORMANCE only) -->
      <div v-if="step === 2 && formData.board_type === 'PERFORMANCE'" class="step-content">
        <h3>공연 선택</h3>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input
            v-model="performanceQuery"
            @input="searchPerformances"
            type="text"
            placeholder="공연 제목이나 장소를 검색하세요..."
          />
        </div>

        <!-- Search Results -->
        <div v-if="performanceResults.length > 0" class="performance-results">
          <div
            v-for="perf in performanceResults"
            :key="perf.mt20id"
            @click="selectPerformance(perf)"
            :class="['performance-item', { selected: formData.performance === perf.mt20id }]"
          >
            <img :src="perf.poster" :alt="perf.prfnm" class="performance-poster" />
            <div class="performance-info">
              <h4>{{ perf.prfnm }}</h4>
              <p class="genre">{{ perf.genrenm }}</p>
              <p class="venue">{{ perf.fcltynm }}</p>
              <p class="period">{{ perf.prfpdfrom }} ~ {{ perf.prfpdto }}</p>
            </div>
            <i v-if="formData.performance === perf.mt20id" class="fas fa-check-circle"></i>
          </div>
        </div>

        <p v-else-if="performanceQuery && !searching" class="no-results">
          검색 결과가 없습니다.
        </p>

        <p v-else class="hint">
          공연 제목이나 장소를 입력하여 검색하세요.
        </p>

        <div class="step-actions">
          <button @click="prevStep" class="btn-secondary">이전</button>
          <button
            @click="nextStep"
            :disabled="!formData.performance"
            class="btn-primary"
          >
            다음
          </button>
        </div>
      </div>

      <!-- Step 3: Category & Content -->
      <div v-if="(step === 2 && formData.board_type === 'GENERAL') || step === 3" class="step-content">
        <h3>글 작성</h3>

        <!-- Category Selection -->
        <div class="form-group">
          <label>카테고리 *</label>
          <div class="category-selection">
            <button
              v-for="cat in availableCategories"
              :key="cat.value"
              @click="formData.category = cat.value"
              :class="['category-btn', { selected: formData.category === cat.value }]"
            >
              {{ cat.label }}
            </button>
          </div>
        </div>

        <!-- Rating (REVIEW only) -->
        <div v-if="formData.category === 'REVIEW'" class="form-group">
          <label>별점 *</label>
          <div class="rating-input">
            <button
              v-for="star in 5"
              :key="star"
              @click="formData.rank = star"
              class="star-btn"
            >
              <i :class="star <= formData.rank ? 'fas fa-star' : 'far fa-star'"></i>
            </button>
            <span class="rating-value">{{ formData.rank || 0 }}점</span>
          </div>
        </div>

        <!-- Title -->
        <div class="form-group">
          <label>제목 *</label>
          <input
            v-model="formData.title"
            type="text"
            placeholder="제목을 입력하세요"
            maxlength="100"
          />
        </div>

        <!-- Content -->
        <div class="form-group">
          <label>내용 *</label>
          <textarea
            v-model="formData.content"
            placeholder="내용을 입력하세요"
            rows="10"
          ></textarea>
        </div>

        <div class="step-actions">
          <button @click="prevStep" class="btn-secondary">이전</button>
          <button
            @click="submitArticle"
            :disabled="!isFormValid || submitting"
            class="btn-primary"
          >
            {{ submitting ? '작성 중...' : '작성 완료' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useCommunityStore } from '@/stores/communityStore'
import axiosInstance from '@/api/axios'

const emit = defineEmits(['close', 'created'])

const communityStore = useCommunityStore()

// Steps
const step = ref(1)

// Form data
const formData = ref({
  board_type: null,
  category: null,
  performance: null,
  title: '',
  content: '',
  rank: null
})

// Performance search
const performanceQuery = ref('')
const performanceResults = ref([])
const searching = ref(false)
const submitting = ref(false)

// Available categories based on board_type
const availableCategories = computed(() => {
  if (formData.value.board_type === 'PERFORMANCE') {
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

// Form validation
const isFormValid = computed(() => {
  if (!formData.value.title || !formData.value.content || !formData.value.category) {
    return false
  }

  // REVIEW requires rating
  if (formData.value.category === 'REVIEW' && !formData.value.rank) {
    return false
  }

  return true
})

// Step navigation
const selectBoardType = (type) => {
  formData.value.board_type = type
  formData.value.category = null
  formData.value.performance = null
  formData.value.rank = null
  nextStep()
}

const nextStep = () => {
  step.value++
}

const prevStep = () => {
  if (step.value > 1) {
    step.value--
  }
}

// Performance search with debounce
let searchTimeout = null
const searchPerformances = async () => {
  if (!performanceQuery.value || performanceQuery.value.length < 2) {
    performanceResults.value = []
    return
  }

  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    searching.value = true
    try {
      // axiosInstance already prefixes /api, so avoid double /api/api
      const response = await axiosInstance.get('/performances/search-autocomplete/', {
        params: { query: performanceQuery.value }
      })

      if (response.data.success) {
        performanceResults.value = response.data.results
      }
    } catch (error) {
      console.error('공연 검색 실패:', error)
      performanceResults.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

const selectPerformance = (performance) => {
  formData.value.performance = performance.mt20id
}

// Submit article
const submitArticle = async () => {
  if (!isFormValid.value || submitting.value) return

  submitting.value = true
  try {
    const payload = {
      board_type: formData.value.board_type,
      category: formData.value.category,
      title: formData.value.title,
      content: formData.value.content
    }

    // Add performance for PERFORMANCE type
    if (formData.value.board_type === 'PERFORMANCE') {
      payload.performance = formData.value.performance
    }

    // Add rank for REVIEW only
    if (formData.value.category === 'REVIEW') {
      payload.rank = formData.value.rank
    } else if (formData.value.category === 'EXPECTATION') {
      payload.rank = 2.5
    }

    await communityStore.createArticle(payload)
    emit('created')
  } catch (error) {
    console.error('글 작성 실패:', error)
    alert('글 작성에 실패했습니다. 다시 시도해주세요.')
  } finally {
    submitting.value = false
  }
}

// Reset category when board_type changes
watch(() => formData.value.board_type, () => {
  formData.value.category = null
  formData.value.rank = null
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transition: background 0.3s;
}

:root.dark .modal-content {
  background: #1f2937;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .modal-header {
  border-bottom-color: #374151;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .modal-header h2 {
  color: #f3f4f6;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #6b7280;
}

.step-content {
  padding: 2rem;
}

.step-content h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .step-content h3 {
  color: #f3f4f6;
}

/* Board Type Selection */
.board-type-selection {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.board-card {
  padding: 2rem;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.board-card:hover {
  border-color: #6366f1;
  background: #ede9fe;
}

.board-card.selected {
  border-color: #6366f1;
  background: #ede9fe;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

:root.dark .board-card {
  background: #111827;
  border-color: #374151;
}

:root.dark .board-card:hover,
:root.dark .board-card.selected {
  border-color: #818cf8;
  background: #1e293b;
}

.board-card i {
  font-size: 3rem;
  color: #6366f1;
  margin-bottom: 1rem;
}

.board-card h4 {
  margin: 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .board-card h4 {
  color: #f3f4f6;
}

.board-card p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .board-card p {
  color: #9ca3af;
}

/* Search Box */
.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  transition: all 0.3s;
}

.search-box:focus-within {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .search-box {
  background: #111827;
  border-color: #374151;
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

/* Performance Results */
.performance-results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
}

.performance-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.performance-item:hover {
  border-color: #6366f1;
  background: #ede9fe;
}

.performance-item.selected {
  border-color: #6366f1;
  background: #ede9fe;
}

:root.dark .performance-item {
  background: #111827;
  border-color: #374151;
}

:root.dark .performance-item:hover,
:root.dark .performance-item.selected {
  border-color: #818cf8;
  background: #1e293b;
}

.performance-poster {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.performance-info {
  flex: 1;
}

.performance-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .performance-info h4 {
  color: #f3f4f6;
}

.performance-info p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .performance-info p {
  color: #9ca3af;
}

.performance-item .fa-check-circle {
  color: #6366f1;
  font-size: 1.5rem;
}

.no-results,
.hint {
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
  padding: 2rem;
}

/* Form Groups */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #f3f4f6;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #111827;
  font-size: 1rem;
  transition: all 0.3s;
}

:root.dark .form-group input,
:root.dark .form-group textarea {
  background: #111827;
  border-color: #374151;
  color: #f3f4f6;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* Category Selection */
.category-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

:deep(.category-btn) {
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

:deep(.category-btn:hover) {
  background: #e5e7eb;
}

:deep(.category-btn.selected) {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

:root.dark :deep(.category-btn) {
  background: #111827;
  border-color: #334155;
  color: #e2e8f0;
}

:root.dark :deep(.category-btn:hover) {
  background: #1f2937;
  border-color: #475569;
  color: #e2e8f0;
}

:root.dark :deep(.category-btn.selected) {
  background: #4f46e5;
  border-color: #6366f1;
  color: #f8fafc;
}

/* Rating Input */
.rating-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.star-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #fbbf24;
  cursor: pointer;
  transition: transform 0.2s;
}

.star-btn:hover {
  transform: scale(1.2);
}

.rating-value {
  margin-left: 0.5rem;
  font-weight: 600;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .rating-value {
  color: #f3f4f6;
}

/* Step Actions */
.step-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

:root.dark .btn-secondary {
  background: #374151;
  color: #d1d5db;
}

:root.dark .btn-secondary:hover {
  background: #4b5563;
}

/* Responsive */
@media (max-width: 768px) {
  .board-type-selection {
    grid-template-columns: 1fr;
  }

  .step-content {
    padding: 1.5rem;
  }

  .step-actions {
    flex-direction: column-reverse;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
