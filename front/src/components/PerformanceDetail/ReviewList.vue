<template>
  <div class="review-list">
    <h3 class="list-title">
      <i class="fas fa-comments"></i>
      리뷰 목록
      <span class="count">({{ reviews.length }})</span>
    </h3>

    <div v-if="reviews.length === 0" class="empty-state">
      <i class="fas fa-inbox"></i>
      <p>아직 작성된 글이 없습니다</p>
      <p class="sub-text">첫 번째 글을 작성해보세요!</p>
    </div>

    <div v-else class="reviews">
      <div
        v-for="review in paginatedReviews"
        :key="review.id"
        class="review-card"
      >
        <div class="review-header">
          <div class="user-info">
            <div class="avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="user-details">
              <div class="username">{{ review.username }}</div>
              <div class="date">{{ formatDate(review.created_at) }}</div>
            </div>
          </div>

          <div class="review-meta">
            <span class="category-badge" :class="getCategoryClass(review.category)">
              {{ getCategoryLabel(review.category) }}
            </span>
            <div v-if="review.rank" class="rating">
              <i
                v-for="n in 5"
                :key="n"
                :class="['fas fa-star', { filled: n <= review.rank }]"
              ></i>
            </div>
          </div>
        </div>

        <div class="review-content">
          <h4 class="review-title">{{ review.title }}</h4>
          <p class="review-text">{{ review.content }}</p>
        </div>

        <div class="review-footer">
          <button
            @click="toggleLike(review)"
            :class="['btn-like', { liked: isLiked(review) }]"
          >
            <i :class="[isLiked(review) ? 'fas' : 'far', 'fa-heart']"></i>
            {{ review.like_count || 0 }}
          </button>

          <button @click="toggleComments(review)" class="btn-comment">
            <i class="fas fa-comment"></i>
            댓글 {{ review.comments?.length || 0 }}
          </button>
        </div>

        <!-- 댓글 섹션 -->
        <div v-if="expandedReview === review.id" class="comments-section">
          <div class="comments-list">
            <div
              v-for="comment in review.comments"
              :key="comment.id"
              class="comment"
            >
              <div class="comment-avatar">
                <i class="fas fa-user-circle"></i>
              </div>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-username">{{ comment.username }}</span>
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
              </div>
            </div>
          </div>

          <!-- 댓글 작성 -->
          <div v-if="isAuthenticated" class="comment-form">
            <textarea
              v-model="commentText[review.id]"
              placeholder="댓글을 입력하세요..."
              rows="2"
              class="comment-input"
            ></textarea>
            <button @click="submitComment(review)" class="btn-submit-comment">
              <i class="fas fa-paper-plane"></i> 댓글 작성
            </button>
          </div>
          <div v-else class="login-prompt">
            <i class="fas fa-lock"></i>
            댓글을 작성하려면 로그인이 필요합니다
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="btn-page"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="btn-page"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'

const props = defineProps({
  reviews: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['review-updated'])

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUserId = computed(() => authStore.userId)

const expandedReview = ref(null)
const commentText = ref({})
const currentPage = ref(1)
const itemsPerPage = 5

// 페이지네이션
const totalPages = computed(() => {
  return Math.ceil(props.reviews.length / itemsPerPage)
})

const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return props.reviews.slice(start, end)
})

// 카테고리 라벨
const getCategoryLabel = (category) => {
  const labels = {
    REVIEW: '후기',
    EXPECTATION: '기대평',
    INFO: '정보공유',
    QNA: '질문',
    FREE: '자유게시판',
  }
  return labels[category] || category
}

// 카테고리 클래스
const getCategoryClass = (category) => {
  return `category-${category.toLowerCase()}`
}

// 좋아요 여부 확인
const isLiked = (review) => {
  return review.like_users?.includes(currentUserId.value) || false
}

// 좋아요 토글
const toggleLike = async (review) => {
  if (!isAuthenticated.value) {
    alert('로그인이 필요합니다')
    return
  }

  try {
    await apiClient.post(`/articles/${review.id}/like/`)
    emit('review-updated')
  } catch (error) {
    console.error('좋아요 실패:', error)
  }
}

// 댓글 토글
const toggleComments = (review) => {
  if (expandedReview.value === review.id) {
    expandedReview.value = null
  } else {
    expandedReview.value = review.id
  }
}

// 댓글 작성
const submitComment = async (review) => {
  const content = commentText.value[review.id]
  if (!content || !content.trim()) {
    alert('댓글 내용을 입력하세요')
    return
  }

  try {
    await apiClient.post('/comments/', {
      article: review.id,
      content: content.trim(),
    })

    commentText.value[review.id] = ''
    emit('review-updated')
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다')
  }
}

// 날짜 포맷
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<style scoped>
.review-list {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .review-list {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.list-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

:root.dark .list-title {
  color: #f3f4f6;
}

.list-title i {
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .list-title i {
  color: #818cf8;
}

.count {
  color: #6b7280;
  font-size: 1.2rem;
  transition: color 0.3s;
}

:root.dark .count {
  color: #9ca3af;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.sub-text {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-top: 0.5rem;
}

/* Reviews */
.reviews {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.review-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 600;
  color: #1f2937;
}

.date {
  font-size: 0.875rem;
  color: #6b7280;
}

.review-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.category-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.category-review {
  background: #dbeafe;
  color: #1e40af;
}

.category-expectation {
  background: #fef3c7;
  color: #92400e;
}

.category-info {
  background: #d1fae5;
  color: #065f46;
}

.category-qna {
  background: #fce7f3;
  color: #9f1239;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.rating i {
  color: #d1d5db;
  font-size: 1rem;
}

.rating i.filled {
  color: #fbbf24;
}

.review-content {
  margin-bottom: 1rem;
}

.review-title {
  font-size: 1.125rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.review-text {
  color: #4b5563;
  line-height: 1.6;
  white-space: pre-wrap;
}

.review-footer {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-like,
.btn-comment {
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
}

.btn-like:hover,
.btn-comment:hover {
  background: #f9fafb;
}

.btn-like.liked {
  color: #ef4444;
  border-color: #ef4444;
}

/* Comments Section */
.comments-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e5e7eb;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.comment {
  display: flex;
  gap: 1rem;
}

.comment-avatar {
  color: #9ca3af;
  font-size: 1.5rem;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-username {
  font-weight: 600;
  color: #374151;
}

.comment-date {
  font-size: 0.875rem;
  color: #9ca3af;
}

.comment-text {
  color: #4b5563;
  line-height: 1.6;
}

.comment-form {
  display: flex;
  gap: 1rem;
}

.comment-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  resize: vertical;
  font-family: inherit;
  transition: all 0.3s;
}

.comment-input:focus {
  outline: none;
  border-color: #6366f1;
}

.btn-submit-comment {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-submit-comment:hover {
  background: #4f46e5;
}

.login-prompt {
  text-align: center;
  padding: 2rem;
  background: #f9fafb;
  border-radius: 6px;
  color: #6b7280;
}

.login-prompt i {
  margin-right: 0.5rem;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-page {
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-page:hover:not(:disabled) {
  background: #f9fafb;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-weight: 600;
  color: #374151;
}

/* 반응형 */
@media (max-width: 768px) {
  .review-list {
    padding: 1.5rem;
  }

  .review-header {
    flex-direction: column;
    gap: 1rem;
  }

  .review-meta {
    align-items: flex-start;
  }

  .comment-form {
    flex-direction: column;
  }

  .btn-submit-comment {
    width: 100%;
  }
}
</style>
