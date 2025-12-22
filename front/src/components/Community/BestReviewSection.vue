<template>
  <div class="best-section">
    <!-- Header -->
    <div class="section-header">
      <h2>
        <i class="fas fa-crown"></i>
        베스트 관람후기
      </h2>
      <router-link to="/community/best" class="more-btn">
        베스트 더보기
        <i class="fas fa-arrow-right"></i>
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="bestLoading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      로딩 중...
    </div>

    <!-- Best Reviews Grid -->
    <div v-else-if="bestReviews.length > 0" class="best-grid">
      <div
        v-for="(review, index) in bestReviews"
        :key="review.id"
        @click="goToReview(review.id)"
        class="best-card"
      >
        <!-- TOP Badge -->
        <div class="top-badge">TOP {{ index + 1 }}</div>

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
            <h3 class="review-title">{{ review.title }}</h3>
            <p class="review-preview">{{ getPreview(review.content) }}</p>

            <!-- Meta Info -->
            <div class="meta-info">
              <span class="likes">
                <i class="fas fa-heart"></i>
                {{ review.like_count || 0 }}
              </span>
              <span class="author">{{ review.username }}</span>
              <span class="date">{{ formatDate(review.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="fas fa-inbox"></i>
      <p>아직 베스트 관람후기가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useCommunityStore } from '@/stores/communityStore'

const router = useRouter()
const communityStore = useCommunityStore()
const { bestReviews, bestLoading } = storeToRefs(communityStore)

const goToReview = (id) => {
  router.push(`/community/${id}`)
}

const getPreview = (content) => {
  if (!content) return ''
  // Remove HTML tags and limit to 80 characters
  const plainText = content.replace(/<[^>]*>/g, '')
  return plainText.length > 80 ? plainText.substring(0, 80) + '...' : plainText
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '오늘'
  if (days === 1) return '어제'
  if (days < 7) return `${days}일 전`

  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.best-section {
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);
  border-radius: 16px;
  border: 1px solid #e0e7ff;
  transition: all 0.3s;
}

:root.dark .best-section {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
  border-color: #312e81;
}

/* Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  transition: color 0.3s;
}

:root.dark .section-header h2 {
  color: #f1f5f9;
}

.section-header h2 i {
  color: #fbbf24;
  font-size: 1.25rem;
}

.more-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  color: #6366f1;
  border: 1px solid #6366f1;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.more-btn:hover {
  background: #6366f1;
  color: white;
  transform: translateX(4px);
}

:root.dark .more-btn {
  color: #818cf8;
  border-color: #818cf8;
}

:root.dark .more-btn:hover {
  background: #818cf8;
  color: #0f172a;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 1rem;
}

.loading-state i {
  margin-right: 0.5rem;
  font-size: 1.25rem;
}

/* Best Grid */
.best-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

@media (max-width: 768px) {
  .best-grid {
    grid-template-columns: 1fr;
  }
}

/* Best Card */
.best-card {
  position: relative;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.best-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
}

:root.dark .best-card {
  background: #1e293b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

:root.dark .best-card:hover {
  box-shadow: 0 8px 24px rgba(129, 140, 248, 0.2);
}

/* TOP Badge */
.top-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 9999px;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
}

/* Card Content */
.card-content {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}

.poster-wrapper {
  flex-shrink: 0;
  width: 88px;
  height: 117px;
  border-radius: 8px;
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
  gap: 0.5rem;
  min-width: 0;
}

.review-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.3s;
}

:root.dark .review-title {
  color: #f1f5f9;
}

.review-preview {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  transition: color 0.3s;
}

:root.dark .review-preview {
  color: #94a3b8;
}

/* Meta Info */
.meta-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: auto;
}

.meta-info span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.likes {
  color: #ef4444;
  font-weight: 600;
}

.likes i {
  font-size: 0.875rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #94a3b8;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 640px) {
  .best-section {
    padding: 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .more-btn {
    width: 100%;
    justify-content: center;
  }

  .card-content {
    gap: 0.75rem;
  }

  .poster-wrapper {
    width: 72px;
    height: 96px;
  }

  .review-title {
    font-size: 0.875rem;
  }

  .review-preview {
    font-size: 0.813rem;
  }
}
</style>
