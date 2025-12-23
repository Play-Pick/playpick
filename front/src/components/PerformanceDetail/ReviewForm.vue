<template>
  <div class="review-form">
    <h3 class="form-title">
      <i class="fas fa-pen"></i>
      리뷰 작성하기
    </h3>

    <div v-if="!isAuthenticated" class="login-required">
      <i class="fas fa-lock"></i>
      <p>리뷰를 작성하려면 로그인이 필요합니다</p>
      <button @click="goToLogin" class="btn-login">
        <i class="fas fa-sign-in-alt"></i> 로그인
      </button>
    </div>

    <form v-else @submit.prevent="submitReview" class="form-content">
      <!-- 카테고리 선택 -->
      <div class="form-group">
        <label>카테고리</label>
        <select v-model="form.category" class="select-category">
          <option value="REVIEW">후기</option>
          <option value="EXPECTATION">기대평</option>
          <option value="INFO">정보공유</option>
          <option value="QNA">질문</option>
        </select>
      </div>

      <!-- 별점 (후기만) -->
      <div v-if="form.category === 'REVIEW'" class="form-group">
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
          rows="6"
          required
          class="textarea-content"
        ></textarea>
      </div>

      <!-- 버튼 -->
      <div class="form-actions">
        <button type="submit" class="btn-submit" :disabled="submitting">
          <i class="fas fa-paper-plane"></i>
          {{ submitting ? '작성 중...' : '리뷰 작성' }}
        </button>
        <button type="button" @click="resetForm" class="btn-reset">
          <i class="fas fa-redo"></i> 초기화
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import communityAPI from '@/api/community'

const props = defineProps({
  performanceId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['review-created'])

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

const form = ref({
  category: 'REVIEW',
  title: '',
  content: '',
  rank: 5,
})

const submitting = ref(false)
const hoverRating = ref(0)

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

const submitReview = async () => {
  try {
    submitting.value = true

    const reviewData = {
      performance: props.performanceId,
      category: form.value.category,
      title: form.value.title,
      content: form.value.content,
    }

    // 별점은 후기일 때만 포함
    if (form.value.category === 'REVIEW') {
      reviewData.rank = form.value.rank
    } else if (form.value.category === 'EXPECTATION') {
      reviewData.rank = 2.5
    }

    await communityAPI.createArticle(reviewData)

    alert('리뷰가 작성되었습니다!')
    resetForm()
    emit('review-created')
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
    alert('리뷰 작성에 실패했습니다.')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.value = {
    category: 'REVIEW',
    title: '',
    content: '',
    rank: 5,
  }
}

const goToLogin = () => {
  router.push({ name: 'login' })
}
</script>

<style scoped>
.review-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .review-form {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.form-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

:root.dark .form-title {
  color: #f3f4f6;
}

.form-title i {
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .form-title i {
  color: #818cf8;
}

/* 로그인 필요 */
.login-required {
  text-align: center;
  padding: 3rem 2rem;
  background: #f9fafb;
  border-radius: 8px;
  transition: background 0.3s;
}

:root.dark .login-required {
  background: #1a1a1a;
}

.login-required i {
  font-size: 3rem;
  color: #9ca3af;
  margin-bottom: 1rem;
  display: block;
  transition: color 0.3s;
}

:root.dark .login-required i {
  color: #6b7280;
}

.login-required p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  transition: color 0.3s;
}

:root.dark .login-required p {
  color: #9ca3af;
}

.btn-login {
  padding: 0.75rem 2rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

:root.dark .btn-login {
  background: #818cf8;
}

.btn-login:hover {
  background: #4f46e5;
}

:root.dark .btn-login:hover {
  background: #6366f1;
}

/* 폼 */
.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #9ca3af;
}

.select-category,
.input-title,
.textarea-content {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #111827;
}

:root.dark .select-category,
:root.dark .input-title,
:root.dark .textarea-content {
  background: #1a1a1a;
  border-color: #374151;
  color: #f3f4f6;
}

.select-category:focus,
.input-title:focus,
.textarea-content:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .select-category:focus,
:root.dark .input-title:focus,
:root.dark .textarea-content:focus {
  border-color: #818cf8;
}

.textarea-content {
  resize: vertical;
  font-family: inherit;
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
  font-size: 2rem;
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
  transform: scale(1.1);
}

.rating-text {
  margin-left: 0.5rem;
  font-weight: 600;
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .rating-text {
  color: #818cf8;
}

/* 버튼 */
.form-actions {
  display: flex;
  gap: 1rem;
}

.btn-submit,
.btn-reset {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit {
  background: #6366f1;
  color: white;
  flex: 1;
}

:root.dark .btn-submit {
  background: #818cf8;
}

.btn-submit:hover:not(:disabled) {
  background: #4f46e5;
}

:root.dark .btn-submit:hover:not(:disabled) {
  background: #6366f1;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reset {
  background: #e5e7eb;
  color: #374151;
}

:root.dark .btn-reset {
  background: #374151;
  color: #f3f4f6;
}

.btn-reset:hover {
  background: #d1d5db;
}

:root.dark .btn-reset:hover {
  background: #4b5563;
}

/* 반응형 */
@media (max-width: 768px) {
  .review-form {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-submit,
  .btn-reset {
    width: 100%;
  }
}
</style>
