<template>
  <div class="community-write-container">
    <div class="write-content">
      <!-- 헤더 -->
      <div class="page-header">
        <button @click="goBack" class="back-button">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1 class="page-title">
          <i :class="categoryIcon"></i>
          {{ categoryLabel }} 작성
        </h1>
      </div>

      <!-- 로그인 필요 -->
      <div v-if="!isAuthenticated" class="login-required">
        <i class="fas fa-lock"></i>
        <p>글을 작성하려면 로그인이 필요합니다</p>
        <button @click="goToLogin" class="btn-login">
          <i class="fas fa-sign-in-alt"></i> 로그인
        </button>
      </div>

      <!-- 작성 폼 -->
      <form v-else @submit.prevent="submitArticle" class="write-form">
        <!-- 공연 선택 (선택사항) -->
        <div class="form-group">
          <label>공연 선택 (선택사항)</label>
          <div class="performance-info">
            <div v-if="performance" class="selected-performance">
              <img :src="performance.poster" alt="공연 포스터" class="performance-poster" />
              <div class="performance-details">
                <h3>{{ performance.prfnm }}</h3>
                <p>{{ performance.prfpdfrom }} ~ {{ performance.prfpdto }}</p>
                <button type="button" @click="clearPerformance" class="btn-clear">
                  <i class="fas fa-times"></i> 선택 해제
                </button>
              </div>
            </div>
            <div v-else class="no-performance">
              <i class="fas fa-theater-masks"></i>
              <p>공연을 선택하지 않았습니다</p>
            </div>
          </div>
        </div>

        <!-- 카테고리 (읽기 전용 표시) -->
        <div class="form-group">
          <label>카테고리</label>
          <div class="category-display">
            <i :class="categoryIcon"></i>
            {{ categoryLabel }}
          </div>
        </div>

        <!-- 별점 (관람후기, 기대평만) -->
        <div v-if="category === 'REVIEW' || category === 'EXPECT'" class="form-group">
          <label>별점</label>
          <div class="star-rating">
            <div
              v-for="n in 5"
              :key="n"
              class="star-wrapper"
              @mousemove="handleStarHover($event, n)"
              @mouseleave="hoverRating = 0"
              @click="handleStarClick($event, n)"
            >
              <i
                class="fas fa-star star-full"
                :class="{ active: n <= (hoverRating || form.rank) }"
              ></i>
              <i
                class="fas fa-star-half-alt star-half"
                :class="{ active: n - 0.5 === (hoverRating || form.rank) }"
              ></i>
            </div>
            <span class="rating-text">{{ form.rank }}점</span>
          </div>
        </div>

        <!-- 제목 -->
        <div class="form-group">
          <label>제목</label>
          <input
            v-model="form.title"
            type="text"
            placeholder="제목을 입력하세요"
            required
            class="input-title"
          />
        </div>

        <!-- 내용 -->
        <div class="form-group">
          <label>내용</label>
          <textarea
            v-model="form.content"
            placeholder="내용을 입력하세요"
            rows="12"
            required
            class="textarea-content"
          ></textarea>
        </div>

        <!-- 버튼 -->
        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitting">
            <i class="fas fa-paper-plane"></i>
            {{ submitting ? '작성 중...' : '작성 완료' }}
          </button>
          <button type="button" @click="goBack" class="btn-cancel">
            <i class="fas fa-times"></i> 취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

// URL 파라미터에서 카테고리와 공연ID 가져오기
const category = ref(route.query.category || 'REVIEW')
const performanceId = ref(route.query.performanceId || null)
const performance = ref(null)

const form = ref({
  title: '',
  content: '',
  rank: 5,
})

const submitting = ref(false)
const hoverRating = ref(0)

// 카테고리별 아이콘과 라벨
const categoryIcon = computed(() => {
  const icons = {
    REVIEW: 'fas fa-star',
    EXPECT: 'fas fa-heart',
    QNA: 'fas fa-question-circle',
    INFO: 'fas fa-info-circle'
  }
  return icons[category.value] || 'fas fa-pen'
})

const categoryLabel = computed(() => {
  const labels = {
    REVIEW: '관람후기',
    EXPECT: '기대평',
    QNA: 'Q&A',
    INFO: '정보공유'
  }
  return labels[category.value] || '글'
})

// 공연 정보 불러오기
const loadPerformance = async () => {
  if (!performanceId.value) return

  try {
    const response = await apiClient.get(`/performances/${performanceId.value}/`)
    performance.value = response.data
  } catch (error) {
    console.error('공연 정보 로드 실패:', error)
  }
}

// 공연 선택 해제
const clearPerformance = () => {
  performance.value = null
  performanceId.value = null
}

// 별점 호버 처리 (0.5 단위)
const handleStarHover = (event, starNumber) => {
  const target = event.currentTarget
  const rect = target.getBoundingClientRect()
  const x = event.clientX - rect.left
  const halfWidth = rect.width / 2

  if (x < halfWidth) {
    hoverRating.value = starNumber - 0.5
  } else {
    hoverRating.value = starNumber
  }
}

// 별점 클릭 처리 (0.5 단위)
const handleStarClick = (event, starNumber) => {
  const target = event.currentTarget
  const rect = target.getBoundingClientRect()
  const x = event.clientX - rect.left
  const halfWidth = rect.width / 2

  if (x < halfWidth) {
    form.value.rank = starNumber - 0.5
  } else {
    form.value.rank = starNumber
  }
}

// 글 작성 제출
const submitArticle = async () => {
  try {
    submitting.value = true

    const articleData = {
      category: category.value,
      title: form.value.title,
      content: form.value.content,
    }

    // 공연이 선택된 경우 포함
    if (performanceId.value) {
      articleData.performance = performanceId.value
    }

    // 별점은 관람후기/기대평일 때만 포함
    if (category.value === 'REVIEW' || category.value === 'EXPECT') {
      articleData.rank = form.value.rank
    }

    await apiClient.post('/community/articles/', articleData)

    alert('글이 작성되었습니다!')

    // 공연 상세 페이지에서 왔으면 돌아가기, 아니면 커뮤니티로
    if (performanceId.value) {
      // refresh 쿼리로 리뷰 새로고침 트리거
      router.push({
        name: 'performance-detail',
        params: { id: performanceId.value },
        query: { refresh: Date.now() }
      })
    } else {
      router.push({ name: 'community' })
    }
  } catch (error) {
    console.error('글 작성 실패:', error)
    alert('글 작성에 실패했습니다.')
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.back()
}

const goToLogin = () => {
  router.push({ name: 'login' })
}

onMounted(() => {
  loadPerformance()
})
</script>

<style scoped>
.community-write-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem 1rem;
  transition: background 0.3s;
}

:root.dark .community-write-container {
  background: linear-gradient(to bottom, #1a1a1a, #0f0f0f);
}

.write-content {
  max-width: 900px;
  margin: 0 auto;
}

/* 헤더 */
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: none;
  background: white;
  color: #6366f1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

:root.dark .back-button {
  background: #2c2c2c;
  color: #818cf8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.back-button:hover {
  background: #6366f1;
  color: white;
  transform: scale(1.05);
}

:root.dark .back-button:hover {
  background: #818cf8;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: color 0.3s;
}

:root.dark .page-title {
  color: #f3f4f6;
}

.page-title i {
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .page-title i {
  color: #818cf8;
}

/* 로그인 필요 */
.login-required {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .login-required {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.login-required i {
  font-size: 4rem;
  color: #9ca3af;
  margin-bottom: 1.5rem;
  display: block;
  transition: color 0.3s;
}

:root.dark .login-required i {
  color: #6b7280;
}

.login-required p {
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 2rem;
  transition: color 0.3s;
}

:root.dark .login-required p {
  color: #9ca3af;
}

.btn-login {
  padding: 0.875rem 2.5rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 1.0625rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .btn-login {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-login:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  transform: scale(1.05);
}

:root.dark .btn-login:hover {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

/* 작성 폼 */
.write-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .write-form {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-weight: 700;
  font-size: 1.0625rem;
  color: #374151;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #d1d5db;
}

/* 공연 정보 */
.performance-info {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  transition: background 0.3s;
}

:root.dark .performance-info {
  background: #1a1a1a;
}

.selected-performance {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.performance-poster {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.performance-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.performance-details h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .performance-details h3 {
  color: #f3f4f6;
}

.performance-details p {
  color: #6b7280;
  font-size: 0.9375rem;
  transition: color 0.3s;
}

:root.dark .performance-details p {
  color: #9ca3af;
}

.btn-clear {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  align-self: flex-start;
}

.btn-clear:hover {
  background: #dc2626;
}

.no-performance {
  text-align: center;
  padding: 2rem;
  color: #9ca3af;
}

.no-performance i {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  display: block;
}

.no-performance p {
  font-size: 0.9375rem;
}

/* 카테고리 표시 */
.category-display {
  padding: 0.875rem 1.25rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.0625rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  align-self: flex-start;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s;
}

:root.dark .category-display {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

/* 별점 */
.star-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.star-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.star-wrapper i {
  font-size: 2.5rem;
  transition: all 0.2s;
}

.star-full {
  color: #d1d5db;
  transition: color 0.3s;
}

:root.dark .star-full {
  color: #4b5563;
}

.star-full.active {
  color: #fbbf24;
}

.star-half {
  position: absolute;
  left: 0;
  top: 0;
  color: transparent;
  overflow: hidden;
  width: 50%;
}

.star-half.active {
  color: #fbbf24;
}

.star-wrapper:hover .star-full,
.star-wrapper:hover .star-half {
  transform: scale(1.15);
}

.rating-text {
  margin-left: 0.75rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .rating-text {
  color: #818cf8;
}

/* 입력 필드 */
.input-title,
.textarea-content {
  padding: 0.875rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #111827;
}

:root.dark .input-title,
:root.dark .textarea-content {
  background: #1a1a1a;
  border-color: #374151;
  color: #f3f4f6;
}

.input-title:focus,
.textarea-content:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .input-title:focus,
:root.dark .textarea-content:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.textarea-content {
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

/* 버튼 */
.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
}

.btn-submit,
.btn-cancel {
  padding: 0.875rem 2.5rem;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 1.0625rem;
  font-weight: 700;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  flex: 1;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

:root.dark .btn-submit {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  transform: scale(1.02);
}

:root.dark .btn-submit:hover:not(:disabled) {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #e5e7eb;
  color: #374151;
}

:root.dark .btn-cancel {
  background: #374151;
  color: #f3f4f6;
}

.btn-cancel:hover {
  background: #d1d5db;
}

:root.dark .btn-cancel:hover {
  background: #4b5563;
}

/* 반응형 */
@media (max-width: 768px) {
  .community-write-container {
    padding: 1rem 0.5rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .write-form {
    padding: 1.5rem;
  }

  .selected-performance {
    flex-direction: column;
  }

  .performance-poster {
    align-self: center;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-submit,
  .btn-cancel {
    width: 100%;
  }
}
</style>
