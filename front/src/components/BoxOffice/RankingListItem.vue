<template>
  <router-link
    :to="`/performances/${perf.mt20id}`"
    class="ranking-list-item"
  >
    <!-- 순위 -->
    <div class="rank-number">
      {{ perf.rank }}
    </div>

    <!-- 포스터 썸네일 -->
    <div class="poster-thumbnail">
      <img
        :src="perf.poster"
        :alt="perf.prfnm"
        @error="handleImageError"
      >
    </div>

    <!-- 공연 정보 -->
    <div class="item-content">
      <h4 class="performance-title">{{ perf.prfnm }}</h4>
      <div class="performance-meta">
        <span class="meta-item">
          <i class="fas fa-map-marker-alt"></i>
          {{ perf.fcltynm || '정보 없음' }}
        </span>
        <span class="meta-divider">|</span>
        <span class="meta-item">
          <i class="fas fa-calendar"></i>
          {{ formatDate(perf.prfpdfrom) }} ~ {{ formatDate(perf.prfpdto) }}
        </span>
      </div>
      <div class="genre-tag">{{ perf.genrenm }}</div>
    </div>

    <!-- 지표 -->
    <div class="item-stats">
      <div class="stat-item">
        <i class="fas fa-users"></i>
        <span class="stat-label">좌석</span>
        <span class="stat-value">{{ formatNumber(perf.seat_count) }}</span>
      </div>
      <div class="stat-item">
        <i class="fas fa-ticket-alt"></i>
        <span class="stat-label">공연</span>
        <span class="stat-value">{{ formatNumber(perf.performance_count) }}회</span>
      </div>
    </div>

    <!-- Like button -->
    <button
      v-if="showLikeButton"
      @click.stop.prevent="handleLikeClick"
      :disabled="likeLoading"
      :class="['list-like-button', { liked: perf.is_liked }]"
      :title="perf.is_liked ? '찜 취소' : '찜하기'"
      :aria-label="perf.is_liked ? `${perf.prfnm} 찜 취소` : `${perf.prfnm} 찜하기`"
      :aria-pressed="perf.is_liked"
    >
      <i :class="perf.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
    </button>

    <!-- 화살표 아이콘 -->
    <div class="arrow-icon">
      <i class="fas fa-chevron-right"></i>
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

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

// 숫자 포맷
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
/* 리스트 아이템 */
.ranking-list-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
}

.ranking-list-item:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  transform: translateX(0.5rem);
  background: linear-gradient(to right, #ffffff, #f9fafb);
}

/* 순위 */
.rank-number {
  flex-shrink: 0;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  color: #6366f1;
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  border-radius: 0.75rem;
}

/* 포스터 썸네일 */
.poster-thumbnail {
  flex-shrink: 0;
  width: 5rem;
  height: 6.67rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.poster-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.ranking-list-item:hover .poster-thumbnail img {
  transform: scale(1.1);
}

/* 아이템 내용 */
.item-content {
  flex: 1;
  min-width: 0; /* flex 아이템의 텍스트 오버플로우 방지 */
}

.performance-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.3s;
}

.ranking-list-item:hover .performance-title {
  color: #6366f1;
}

.performance-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.625rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-item i {
  color: #9ca3af;
  font-size: 0.75rem;
  flex-shrink: 0;
  margin-right: 0.25rem;
}

.meta-divider {
  color: #d1d5db;
}

.genre-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 0.75rem;
  font-weight: 500;
}

/* 지표 */
.item-stats {
  display: flex;
  gap: 1.5rem;
  margin-right: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-item i {
  color: #6366f1;
  font-size: 1rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.stat-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

/* Like button */
.list-like-button {
  flex-shrink: 0;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
  color: #9ca3af;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  margin-right: 0.5rem;
}

.list-like-button:hover {
  background: #fef2f2;
  color: #ef4444;
  transform: scale(1.1);
}

.list-like-button.liked {
  background: #fef2f2;
  color: #ef4444;
}

.list-like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.list-like-button i {
  font-size: 1rem;
  transition: transform 0.3s;
}

.list-like-button.liked i {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0%, 100% { transform: scale(1); }
  25% { transform: scale(1.3); }
  50% { transform: scale(1.1); }
  75% { transform: scale(1.2); }
}

/* 화살표 아이콘 */
.arrow-icon {
  flex-shrink: 0;
  color: #d1d5db;
  transition: all 0.3s;
}

.ranking-list-item:hover .arrow-icon {
  color: #6366f1;
  transform: translateX(0.25rem);
}

.arrow-icon i {
  font-size: 1.25rem;
}

/* 반응형 */
@media (max-width: 1024px) {
  .item-stats {
    display: none;
  }
}

@media (max-width: 768px) {
  .ranking-list-item {
    padding: 1rem;
    gap: 1rem;
  }

  .rank-number {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1.25rem;
  }

  .poster-thumbnail {
    width: 4rem;
    height: 5.33rem;
  }

  .performance-title {
    font-size: 1rem;
  }

  .performance-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .meta-divider {
    display: none;
  }

  .arrow-icon {
    display: none;
  }
}

/* Dark mode styles */
:root.dark .ranking-list-item {
  background: #2c2c2c;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

:root.dark .ranking-list-item:hover {
  background: linear-gradient(to right, #333333, #2c2c2c);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.7);
}

:root.dark .rank-number {
  color: #818cf8;
  background: linear-gradient(135deg, #2c2c3d, #252535);
}

:root.dark .poster-thumbnail {
  background: #374151;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

:root.dark .performance-title {
  color: #f3f4f6;
}

:root.dark .ranking-list-item:hover .performance-title {
  color: #818cf8;
}

:root.dark .performance-meta {
  color: #9ca3af;
}

:root.dark .meta-item {
  color: #9ca3af;
}

:root.dark .meta-item i {
  color: #6b7280;
}

:root.dark .meta-divider {
  color: #4b5563;
}

:root.dark .genre-tag {
  background: #374151;
  color: #d1d5db;
}

:root.dark .stat-item i {
  color: #818cf8;
}

:root.dark .stat-label {
  color: #6b7280;
}

:root.dark .stat-value {
  color: #f3f4f6;
}

:root.dark .arrow-icon {
  color: #4b5563;
}

:root.dark .ranking-list-item:hover .arrow-icon {
  color: #818cf8;
}

:root.dark .list-like-button {
  background: #374151;
  color: #6b7280;
}

:root.dark .list-like-button:hover {
  background: #3f1f1f;
  color: #fca5a5;
}

:root.dark .list-like-button.liked {
  background: #3f1f1f;
  color: #fca5a5;
}
</style>
