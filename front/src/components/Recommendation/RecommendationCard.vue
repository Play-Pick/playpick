<template>
  <router-link
    :to="`/performances/${performance.mt20id}`"
    class="recommendation-card"
  >
    <!-- Poster -->
    <div class="card-poster">
      <img
        :src="performance.poster"
        :alt="`${performance.prfnm} 포스터`"
        class="poster-image"
        @error="handleImageError"
      >
      <div class="hover-overlay">
        <span>자세히 보기 →</span>
      </div>

      <!-- Reason badge (modernized) -->
      <div v-if="reason" class="reason-badge card-badge-overlay">
        <i class="fas fa-sparkles"></i>
        <span>{{ reason }}</span>
      </div>
      
      <!-- Like button -->
      <button
        v-if="showLikeButton"
        @click.stop.prevent="handleLikeClick"
        :disabled="likeLoading"
        :class="['card-like-button', { liked: performance.is_liked }]"
        :title="performance.is_liked ? '찜 취소' : '찜하기'"
        :aria-label="performance.is_liked ? `${performance.prfnm} 찜 취소` : `${performance.prfnm} 찜하기`"
        :aria-pressed="performance.is_liked"
      >
        <i :class="performance.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
      </button>
    </div>

    <!-- Performance info -->
    <div class="card-content">
      <h3 class="performance-title">{{ performance.prfnm }}</h3>

      <div class="performance-info">
        <div class="info-item">
          <i class="fas fa-map-marker-alt"></i>
          <span>{{ performance.fcltynm || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <i class="fas fa-calendar"></i>
          <span>{{ formatDate(performance.prfpdfrom) }} ~ {{ formatDate(performance.prfpdto) }}</span>
        </div>
      </div>

      <div class="genre-badge">
        {{ performance.genrenm }}
      </div>
    </div>
  </router-link>
</template>

<script setup>
const props = defineProps({
  performance: {
    type: Object,
    required: true
  },
  reason: {
    type: String,
    default: ''
  },
  showLikeButton: {
    type: Boolean,
    default: true
  },
  likeLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle-like'])

const handleLikeClick = () => {
  emit('toggle-like', props.performance.mt20id)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/300x400?text=No+Poster'
}
</script>

<style scoped>
/* Card basic */
.recommendation-card {
  position: relative;
  background: var(--card-surface);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 520px; /* 고정된 카드 높이로 레이아웃 균일화 */
  border: 1px solid var(--card-border);
}

.recommendation-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: var(--card-accent);
}

/* Poster */
.card-poster {
  position: relative;
  width: 100%;
  padding-top: 133.33%; /* 3:4 ratio */
  overflow: hidden;
  background: #e5e7eb;
}

.poster-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.recommendation-card:hover .poster-image {
  transform: scale(1.1);
}

/* Hover overlay */
.hover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.recommendation-card:hover .hover-overlay {
  background: rgba(0, 0, 0, 0.3);
}

.hover-overlay span {
  color: white;
  font-weight: 700;
  font-size: 1rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.recommendation-card:hover .hover-overlay span {
  opacity: 1;
}

/* Reason badge - modernized */
.reason-badge {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

:root.dark .reason-badge {
  background: var(--badge-bg-light);
}

.reason-badge i {
  font-size: 0.75rem;
}

/* Card content */
.card-content {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.performance-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--card-text-primary);
  margin-bottom: 0.75rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3.2rem; /* 두 줄 공간 확보해 정보 섹션 위치를 고정 */
}

.recommendation-card:hover .performance-title {
  color: var(--card-accent);
}

/* Performance info */
.performance-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex: 1;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

.info-item i {
  color: var(--card-accent);
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.info-item span {
  line-height: 1.5;
}

/* Genre badge - chip style */
.genre-badge {
  display: inline-block;
  align-self: flex-start;
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  background: var(--card-chip-bg);
  color: var(--card-accent);
  font-size: 0.875rem;
  font-weight: 600;
}

/* Dark mode adjustments */
:root.dark .card-poster {
  background: #374151;
}

/* Backdrop-filter fallback */
@supports not (backdrop-filter: blur(8px)) {
  .reason-badge {
    background: rgba(0, 0, 0, 0.7);
  }

  :root.dark .reason-badge {
    background: rgba(255, 255, 255, 0.25);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .card-content {
    padding: 1rem;
  }

  .performance-title {
    font-size: 1rem;
  }

  .info-item {
    font-size: 0.8125rem;
  }
}
</style>
