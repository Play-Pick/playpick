<template>
  <div class="best-page">
    <!-- Header -->
    <div class="page-header">
      <button @click="goBack" class="back-btn">
        <i class="fas fa-arrow-left"></i>
        뒤로가기
      </button>
      <h1>
        <i class="fas fa-crown"></i>
        베스트 관람후기
      </h1>
      <p class="subtitle">최근 14일간 가장 인기 있는 관람후기를 확인하세요</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      로딩 중...
    </div>

    <!-- Best Reviews List -->
    <div v-else-if="bestReviews.length > 0" class="best-list">
      <div
        v-for="(review, index) in bestReviews"
        :key="review.id"
        @click="goToReview(review.id)"
        class="best-card"
      >
        <!-- Rank Badge -->
        <div class="rank-badge" :class="`rank-${index + 1}`">
          {{ index + 1 }}
        </div>

        <!-- Content -->
        <div class="card-content">
          <!-- Poster Thumbnail -->
          <div class="poster-wrapper">
            <img
              :src="review.performance_poster || review.performance?.poster || '/default-poster.jpg'"
              :alt="review.performance_name || review.performance?.prfnm"
              class="poster"
            />
          </div>

          <!-- Review Info -->
          <div class="review-info">
            <!-- Performance Name -->
            <span class="performance-name">{{ review.performance_name || review.performance?.prfnm }}</span>

            <!-- Title -->
            <h3 class="review-title">{{ review.title }}</h3>

            <!-- Content Preview -->
            <p class="review-preview">{{ getPreview(review.content) }}</p>

            <!-- Rating (if available) -->
            <div v-if="review.rank" class="rating">
              <i
                v-for="star in 5"
                :key="star"
                :class="star <= review.rank ? 'fas fa-star' : 'far fa-star'"
              ></i>
              <span class="rating-value">{{ review.rank.toFixed(1) }}</span>
            </div>

            <!-- Meta Info -->
            <div class="meta-info">
              <span class="likes">
                <i class="fas fa-heart"></i>
                {{ review.like_count || 0 }}
              </span>
              <span class="author">
                <i class="fas fa-user"></i>
                {{ review.username }}
              </span>
              <span class="date">
                <i class="fas fa-clock"></i>
                {{ formatDate(review.created_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox"></i>
      <p>아직 베스트 관람후기가 없습니다.</p>
      <router-link to="/community" class="go-community-btn">
        커뮤니티로 이동
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/communityStore'
import { storeToRefs } from 'pinia'

const router = useRouter()
const communityStore = useCommunityStore()
const { bestReviews } = storeToRefs(communityStore)
const loading = ref(false)

const goBack = () => {
  router.back()
}

const goToReview = (id) => {
  router.push(`/community/${id}`)
}

const getPreview = (content) => {
  if (!content) return ''
  const plainText = content.replace(/<[^>]*>/g, '')
  return plainText.length > 150 ? plainText.substring(0, 150) + '...' : plainText
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  loading.value = true
  try {
    await communityStore.fetchBestReviews(20) // Fetch more for the full page
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.best-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .best-page {
  color: #f3f4f6;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  color: #6366f1;
  border: 1px solid #6366f1;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 1.5rem;
}

.back-btn:hover {
  background: #6366f1;
  color: white;
}

:root.dark .back-btn {
  color: #818cf8;
  border-color: #818cf8;
}

:root.dark .back-btn:hover {
  background: #818cf8;
  color: #0f172a;
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.page-header h1 i {
  color: #fbbf24;
}

.subtitle {
  margin: 0;
  color: #64748b;
  font-size: 1rem;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem;
  color: #64748b;
  font-size: 1.25rem;
}

.loading-state i {
  margin-right: 0.5rem;
  font-size: 1.5rem;
}

/* Best List */
.best-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Best Card */
.best-card {
  position: relative;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.best-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.15);
  border-color: #6366f1;
}

:root.dark .best-card {
  background: #1e293b;
  border-color: #334155;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

:root.dark .best-card:hover {
  box-shadow: 0 12px 32px rgba(129, 140, 248, 0.2);
  border-color: #818cf8;
}

/* Rank Badge */
.rank-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.rank-1 {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.rank-2 {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
}

.rank-3 {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
}

.rank-badge:not(.rank-1):not(.rank-2):not(.rank-3) {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

/* Card Content */
.card-content {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
}

.poster-wrapper {
  flex-shrink: 0;
  width: 120px;
  height: 160px;
  border-radius: 12px;
  overflow: hidden;
  background: #f1f5f9;
}

.poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 0;
}

.performance-name {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #ede9fe;
  color: #6366f1;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  width: fit-content;
}

:root.dark .performance-name {
  background: #312e81;
  color: #c7d2fe;
}

.review-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  transition: color 0.3s;
}

:root.dark .review-title {
  color: #f1f5f9;
}

.review-preview {
  margin: 0;
  font-size: 0.938rem;
  color: #64748b;
  line-height: 1.6;
  transition: color 0.3s;
}

:root.dark .review-preview {
  color: #94a3b8;
}

/* Rating */
.rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #fbbf24;
  font-size: 1rem;
}

.rating-value {
  margin-left: 0.5rem;
  color: #64748b;
  font-weight: 600;
}

/* Meta Info */
.meta-info {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: auto;
}

.meta-info span {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.likes {
  color: #ef4444;
  font-weight: 600;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #94a3b8;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
  font-size: 1.125rem;
}

.go-community-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.go-community-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .best-page {
    padding: 1rem;
  }

  .card-content {
    flex-direction: column;
    gap: 1rem;
  }

  .poster-wrapper {
    width: 100%;
    height: 240px;
  }

  .rank-badge {
    top: 0.75rem;
    left: 0.75rem;
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .review-title {
    font-size: 1.125rem;
  }

  .meta-info {
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}
</style>
