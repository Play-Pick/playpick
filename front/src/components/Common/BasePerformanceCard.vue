<template>
  <component
    :is="clickable ? 'router-link' : 'div'"
    :to="clickable ? `/performances/${performance.mt20id}` : undefined"
    :class="['base-performance-card', cardClass]"
    @click="handleCardClick"
  >
    <!-- 포스터 영역 -->
    <div class="card-poster">
      <img
        :src="performance.poster || '/no_poster.png'"
        :alt="`${performance.prfnm} 포스터`"
        class="poster-image"
        @error="handleImageError"
      />

      <!-- 슬롯 1: 뱃지 (왼쪽 상단 오버레이) -->
      <slot name="badge"></slot>

      <!-- 호버 오버레이 -->
      <div v-if="showHoverOverlay" class="hover-overlay">
        <span>자세히 보기 →</span>
      </div>

      <!-- 찜하기 버튼 (공통) -->
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

    <!-- 카드 정보 영역 -->
    <div class="card-content">
      <h3 class="performance-title">{{ performance.prfnm }}</h3>

      <!-- 슬롯 2: 추가 정보 (기본 정보 외 추가) -->
      <div class="performance-info">
        <slot name="info">
          <!-- 기본값: 장소와 날짜 -->
          <div class="info-item">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ performance.fcltynm || '정보 없음' }}</span>
          </div>
          <div class="info-item">
            <i class="fas fa-calendar"></i>
            <span>{{ formatDateRange(performance.prfpdfrom, performance.prfpdto) }}</span>
          </div>
        </slot>
      </div>

      <!-- 슬롯 3: 하단 (장르 뱃지 등) -->
      <slot name="footer">
        <div class="genre-badge">{{ performance.genrenm }}</div>
      </slot>
    </div>
  </component>
</template>

<script setup>
const props = defineProps({
  performance: {
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
  },
  showHoverOverlay: {
    type: Boolean,
    default: true
  },
  clickable: {
    type: Boolean,
    default: true
  },
  cardClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click', 'toggle-like'])

const handleCardClick = () => {
  if (!props.clickable) {
    emit('click', props.performance.mt20id)
  }
}

const handleLikeClick = () => {
  emit('toggle-like', props.performance.mt20id)
}

const formatDateRange = (from, to) => {
  if (!from || !to) return ''
  return `${from.replace(/-/g, '.')} ~ ${to.replace(/-/g, '.')}`
}

const handleImageError = (event) => {
  event.target.src = '/no_poster.png'
}
</script>

<style scoped>
/* 카드 기본 스타일 */
.base-performance-card {
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
  border: 1px solid var(--card-border);
}

.base-performance-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: var(--card-accent);
}

/* 포스터 영역 */
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
  transition: transform 0.4s ease;
}

.base-performance-card:hover .poster-image {
  transform: scale(1.1);
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
  z-index: 2;
}

.base-performance-card:hover .hover-overlay {
  background: rgba(0, 0, 0, 0.3);
}

.hover-overlay span {
  color: white;
  font-weight: 700;
  font-size: 1rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.base-performance-card:hover .hover-overlay span {
  opacity: 1;
}

/* 찜하기 버튼 */
.card-like-button {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
  z-index: 10;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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

/* 다크모드 찜하기 버튼 */
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

/* 카드 콘텐츠 */
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
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3.2rem;
}

.base-performance-card:hover .performance-title {
  color: var(--card-accent);
}

/* 공연 정보 */
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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 장르 뱃지 */
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

/* 반응형 */
@media (max-width: 768px) {
  .card-content {
    padding: 1rem;
  }

  .performance-title {
    font-size: 1rem;
    min-height: 2.8rem;
  }

  .info-item {
    font-size: 0.8125rem;
  }
}
</style>
