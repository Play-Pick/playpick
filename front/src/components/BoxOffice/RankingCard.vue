<template>
  <router-link
    :to="`/performances/${perf.mt20id}`"
    :class="['ranking-card', getRankClass(perf.rank)]"
  >
    <!-- 순위 배지 (큰 사이즈) -->
    <div :class="['rank-badge-large', getRankBadgeClass(perf.rank)]">
      <div class="rank-number">{{ perf.rank }}</div>
      <div class="rank-label">위</div>
    </div>

    <!-- 포스터 -->
    <div class="card-poster">
      <img
        :src="perf.poster"
        :alt="`${perf.prfnm} 포스터`"
        class="poster-image"
        @error="handleImageError"
      >
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
    <div class="card-content">
      <h3 class="performance-title">{{ perf.prfnm }}</h3>

      <div class="performance-info">
        <div class="info-item">
          <i class="fas fa-map-marker-alt"></i>
          <span>{{ perf.fcltynm || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <i class="fas fa-calendar"></i>
          <span>{{ formatDate(perf.prfpdfrom) }} ~ {{ formatDate(perf.prfpdto) }}</span>
        </div>
        <div class="info-item">
          <i class="fas fa-users"></i>
          <span>좌석 {{ formatNumber(perf.seat_count) }}석</span>
        </div>
        <div class="info-item">
          <i class="fas fa-ticket-alt"></i>
          <span>공연 {{ formatNumber(perf.performance_count) }}회</span>
        </div>
      </div>

      <div class="genre-badge">
        {{ perf.genrenm }}
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

// 순위별 클래스
const getRankClass = (rank) => {
  if (rank === 1) return 'rank-1'
  if (rank === 2) return 'rank-2'
  if (rank === 3) return 'rank-3'
  return ''
}

// 순위 배지 클래스
const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'badge-gold'
  if (rank === 2) return 'badge-silver'
  if (rank === 3) return 'badge-bronze'
  return 'badge-default'
}

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

// 숫자 포맷 (천 단위 콤마)
const formatNumber = (num) => {
  if (!num) return '0'
  return num.toLocaleString()
}

// 이미지 에러 처리
const handleImageError = (event) => {
  event.target.src = '/no_poster.png'
}
</script>

<style scoped>
/* 카드 기본 */
.ranking-card {
  position: relative;
  background: var(--card-surface);
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid var(--card-border);
}

.ranking-card:hover {
  transform: translateY(-1rem) scale(1.02);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
  border-color: var(--card-accent);
}

/* 1위 카드 특별 효과 */
.rank-1 {
  border: 3px solid #fbbf24;
}

.rank-1::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #fbbf24, #f59e0b, #fbbf24);
  border-radius: 1.5rem;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s;
}

.rank-1:hover::before {
  opacity: 0.5;
}

/* 순위 배지 (큰 사이즈) */
.rank-badge-large {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  color: white;
  font-weight: 800;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.4);
}

.badge-gold {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  box-shadow: 0 10px 20px -5px rgba(251, 191, 36, 0.6);
}

.badge-silver {
  background: linear-gradient(135deg, #e5e7eb 0%, #9ca3af 100%);
  box-shadow: 0 10px 20px -5px rgba(156, 163, 175, 0.6);
}

.badge-bronze {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
  box-shadow: 0 10px 20px -5px rgba(251, 146, 60, 0.6);
}

.rank-number {
  font-size: 1.75rem;
  line-height: 1;
}

.rank-label {
  font-size: 0.75rem;
  margin-top: 0.125rem;
}

/* 포스터 */
.card-poster {
  position: relative;
  width: 100%;
  padding-top: 133.33%; /* 3:4 비율 */
  overflow: hidden;
  background: #e5e7eb;
}

:root.dark .card-poster {
  background: #374151;
}

.poster-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.ranking-card:hover .poster-image {
  transform: scale(1.15);
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

.ranking-card:hover .hover-overlay {
  background: rgba(0, 0, 0, 0.4);
}

.hover-overlay span {
  color: white;
  font-weight: 700;
  font-size: 1.25rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.ranking-card:hover .hover-overlay span {
  opacity: 1;
}

/* 카드 내용 */
.card-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.performance-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--card-text-primary);
  margin-bottom: 1rem;
  line-height: 1.4;
  min-height: 2.8rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ranking-card:hover .performance-title {
  color: var(--card-accent);
}

/* 공연 정보 */
.performance-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  flex: 1;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.9375rem;
  color: var(--card-text-secondary);
}

.info-item i {
  color: var(--card-accent);
  margin-top: 0.1875rem;
  flex-shrink: 0;
  width: 1rem;
  text-align: center;
}

.info-item span {
  line-height: 1.5;
}

/* 장르 배지 */
.genre-badge {
  display: inline-block;
  align-self: flex-start;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  background: var(--card-chip-bg);
  color: var(--card-accent);
  font-size: 0.875rem;
  font-weight: 600;
}

/* Like button */
.card-like-button {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  z-index: 10;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  color: #9ca3af;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-like-button:hover {
  background: #fef2f2;
  color: #ef4444;
  transform: scale(1.1);
}

.card-like-button.liked {
  background: #fef2f2;
  color: #ef4444;
}

.card-like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.card-like-button i {
  font-size: 1.25rem;
  transition: transform 0.3s;
}

.card-like-button.liked i {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0%, 100% { transform: scale(1); }
  25% { transform: scale(1.3); }
  50% { transform: scale(1.1); }
  75% { transform: scale(1.2); }
}

/* 반응형 */
@media (max-width: 768px) {
  .rank-badge-large {
    width: 3.5rem;
    height: 3.5rem;
  }

  .rank-number {
    font-size: 1.5rem;
  }

  .performance-title {
    font-size: 1.125rem;
  }

  .info-item {
    font-size: 0.875rem;
  }
}
</style>
