<template>
  <router-link
    :to="`/performances/${perf.mt20id}`"
    class="performance-card"
  >
    <div class="card-poster">
      <!-- 순위 뱃지 (작고 모던하게) -->
      <div :class="['rank-badge card-badge-overlay', getRankBadgeClass(perf.rank)]">
        <i class="fas fa-trophy"></i>{{ perf.rank }}
      </div>

      <!-- 포스터 이미지 -->
      <img
        :src="perf.poster"
        :alt="`${perf.prfnm} 포스터`"
        class="poster-image"
        @error="handleImageError"
      >

      <!-- 호버 오버레이 -->
      <div class="hover-overlay">
        <span>자세히 보기 →</span>
      </div>

      <!-- Like button -->
      <button
        v-if="showLikeButton"
        @click.stop.prevent="handleLikeClick"
        :disabled="likeLoading"
        :class="['card-like-button', { liked: perf.is_liked }]"
        :title="perf.is_liked ? '찜 취소' : '찜하기'"
        :aria-label="perf.is_liked ? `${perf.prfnm} 찜 취소` : `${perf.prfnm} 찜하기`"
        :aria-pressed="perf.is_liked"
      >
        <i :class="perf.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
      </button>
    </div>

    <!-- 공연 정보 -->
    <div class="card-info">
      <h3 class="performance-title">{{ perf.prfnm }}</h3>
      <div class="performance-details">
        <p class="detail-item">
          <i class="fas fa-map-marker-alt"></i>
          <span>{{ perf.fcltynm || '정보 없음' }}</span>
        </p>
        <p class="detail-item">
          <i class="fas fa-calendar"></i>
          <span>{{ formatDate(perf.prfpdfrom) }} ~ {{ formatDate(perf.prfpdto) }}</span>
        </p>
        <p class="genre-tag">
          <span>{{ perf.genrenm || '' }}</span>
        </p>
      </div>
    </div>
  </router-link>
</template>

<script setup>
const props = defineProps({
  perf: {
    type: Object,
    required: true
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
  emit('toggle-like', props.perf.mt20id)
}

// 순위 뱃지 클래스
const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return 'rank-default'
}

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

// 이미지 에러 처리
const handleImageError = (event) => {
  event.target.src = '/no_poster.png'
}
</script>

<style scoped>
/* 공연 카드 */
.performance-card {
  flex-shrink: 0;
  width: 16rem;
  background: var(--card-surface);
  border-radius: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
  border: 1px solid var(--card-border);
}

.performance-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: translateY(-0.5rem);
  border-color: var(--card-accent);
}

.card-poster {
  position: relative;
  width: 100%;
  height: 20rem;
  overflow: hidden;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

:root.dark .card-poster {
  background: #374151;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.5s;
}

.performance-card:hover .poster-image {
  transform: scale(1.1);
}

/* 순위 뱃지 - 컴팩트 버전 */
.rank-badge {
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.rank-gold {
  background: linear-gradient(to right, #fbbf24, #f59e0b);
}

.rank-silver {
  background: linear-gradient(to right, #d1d5db, #9ca3af);
}

.rank-bronze {
  background: linear-gradient(to right, #fb923c, #ea580c);
}

.rank-default {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
}

:root.dark .rank-default {
  background: var(--badge-bg-light);
}

.rank-badge i {
  font-size: 0.75rem;
}

/* 호버 오버레이 */
.hover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.performance-card:hover .hover-overlay {
  background: rgba(0, 0, 0, 0.3);
}

.hover-overlay span {
  color: white;
  font-weight: 700;
  font-size: 1.125rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.performance-card:hover .hover-overlay span {
  opacity: 1;
}

/* 카드 정보 */
.card-info {
  padding: 1.25rem;
}

.performance-title {
  font-weight: 700;
  font-size: 1.125rem;
  margin-bottom: 0.75rem;
  height: 3.5rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  color: var(--card-text-primary);
  transition: color 0.3s;
}

.performance-card:hover .performance-title {
  color: var(--card-accent);
}

.performance-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  font-size: 0.875rem;
  color: var(--card-text-secondary);
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.detail-item i {
  color: var(--card-accent);
  margin-top: 0.25rem;
  flex-shrink: 0;
}

.detail-item span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.genre-tag {
  margin-top: 0.75rem;
}

.genre-tag span {
  display: inline-block;
  background: var(--card-chip-bg);
  color: var(--card-accent);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* 찜하기 버튼 */
.card-like-button {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.card-like-button:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

.card-like-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card-like-button i {
  font-size: 1.125rem;
  color: #6b7280;
  transition: color 0.3s;
}

.card-like-button.liked i {
  color: #ef4444;
  animation: heartBeat 0.3s ease;
}

.card-like-button:hover i {
  color: #ef4444;
}

@keyframes heartBeat {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

/* 다크모드 */
:root.dark .card-like-button {
  background: rgba(31, 41, 55, 0.9);
}

:root.dark .card-like-button:hover {
  background: rgba(31, 41, 55, 1);
}

:root.dark .card-like-button i {
  color: #9ca3af;
}

:root.dark .card-like-button.liked i {
  color: #f87171;
}

:root.dark .card-like-button:hover i {
  color: #f87171;
}
</style>
