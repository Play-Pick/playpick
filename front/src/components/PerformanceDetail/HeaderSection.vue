<template>
  <div class="header-section">
    <div class="poster-section">
      <img
        :src="performance.poster || 'https://via.placeholder.com/400x560?text=No+Poster'"
        :alt="performance.prfnm"
        class="poster-large"
        @error="handleImageError"
      />

      <!-- 평점 차트 (포스터 하단) -->
      <div class="poster-rating">
        <slot name="rating-chart"></slot>
      </div>
    </div>
    <div class="info-section">
      <h1>{{ performance.prfnm }}</h1>

      <div class="info-grid">
        <div v-if="performance.genrenm" class="info-item">
          <i class="fas fa-theater-masks icon"></i>
          <span class="label">장르:</span>
          <span>{{ performance.genrenm }}</span>
        </div>

        <div v-if="performance.prfpdfrom && performance.prfpdto" class="info-item">
          <i class="fas fa-calendar icon"></i>
          <span class="label">공연기간:</span>
          <span>{{ performance.prfpdfrom }} ~ {{ performance.prfpdto }}</span>
        </div>

        <div v-if="performance.fcltynm" class="info-item">
          <i class="fas fa-map-marker-alt icon"></i>
          <span class="label">공연장소:</span>
          <span>{{ performance.fcltynm }}</span>
          <button @click="emit('open-map')" class="map-button" title="지도 보기">
            <i class="fas fa-external-link-alt"></i>
          </button>
        </div>

        <div v-if="performance.detail?.prfruntime" class="info-item">
          <i class="fas fa-clock icon"></i>
          <span class="label">공연시간:</span>
          <span>{{ performance.detail.prfruntime }}</span>
        </div>

        <div v-if="performance.detail?.prfage" class="info-item">
          <i class="fas fa-user-check icon"></i>
          <span class="label">관람연령:</span>
          <span>{{ performance.detail.prfage }}</span>
        </div>

        <div v-if="performance.detail?.entrpsnm" class="info-item">
          <i class="fas fa-building icon"></i>
          <span class="label">제작사:</span>
          <span>{{ performance.detail.entrpsnm }}</span>
        </div>

        <div v-if="performance.prfstate" class="info-item">
          <i class="fas fa-info-circle icon"></i>
          <span class="label">공연상태:</span>
          <span :class="`status-badge status-${performance.prfstate}`">
            {{ performance.prfstate }}
          </span>
        </div>
      </div>

      <!-- 찜하기 및 관람함 버튼 -->
      <div class="action-buttons">
        <button
          @click="emit('toggle-like')"
          :disabled="likeLoading"
          :class="{ liked: performance.is_liked }"
          class="like-button"
        >
          <i :class="performance.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
          {{ performance.is_liked ? '찜 취소' : '찜하기' }}
          <span v-if="performance.like_count > 0" class="like-count">
            {{ performance.like_count }}
          </span>
        </button>

        <button
          @click="emit('toggle-watched')"
          :disabled="watchedLoading"
          :class="{ watched: performance.is_watched }"
          class="watched-button"
        >
          <i :class="performance.is_watched ? 'fas fa-check-circle' : 'far fa-check-circle'"></i>
          {{ performance.is_watched ? '관람함' : '봤어요' }}
        </button>
      </div>

      <!-- 예매 링크 -->
      <div v-if="performance.detail?.relates?.length" class="booking-section">
        <h3><i class="fas fa-ticket-alt"></i> 예매하기</h3>
        <div class="booking-links">
          <a
            v-for="relate in performance.detail.relates"
            :key="relate.relatenm"
            :href="relate.relateurl"
            target="_blank"
            class="booking-link"
          >
            {{ relate.relatenm }}
            <i class="fas fa-external-link-alt"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  performance: {
    type: Object,
    required: true
  },
  likeLoading: {
    type: Boolean,
    default: false
  },
  watchedLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['open-map', 'toggle-like', 'toggle-watched'])

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/400x560?text=No+Poster'
}
</script>

<style scoped>
.header-section {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .header-section {
  background: #2c2c2c;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.poster-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.poster-large {
  width: 100%;
  border-radius: 0.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.poster-rating {
  width: 100%;
}

/* 포스터 하단 평점 차트 스타일 조정 */
.poster-rating :deep(.rating-chart) {
  padding: 1rem;
  margin-bottom: 0;
}

.poster-rating :deep(.chart-header) {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.poster-rating :deep(.header-left) {
  min-width: auto;
  width: 100%;
}

.poster-rating :deep(.label) {
  font-size: 0.75rem;
}

.poster-rating :deep(.average) {
  font-size: 1rem;
}

.poster-rating :deep(.average i) {
  font-size: 0.875rem;
}

.poster-rating :deep(.total) {
  font-size: 0.75rem;
}

.poster-rating :deep(.chart-bars) {
  width: 100%;
  height: 30px;
  padding: 0;
}

.poster-rating :deep(.bar-container) {
  height: 20px;
}

.poster-rating :deep(.bar-label) {
  font-size: 0.5rem;
}

.poster-rating :deep(.axis-label) {
  font-size: 0.625rem;
  margin-bottom: 1rem;
}

.info-section h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #111827;
  border-bottom: 3px solid #6366f1;
  padding-bottom: 0.5rem;
  transition: color 0.3s, border-color 0.3s;
}

:root.dark .info-section h1 {
  color: #f3f4f6;
  border-bottom-color: #818cf8;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  line-height: 1.6;
  transition: color 0.3s;
}

:root.dark .info-item {
  color: #f3f4f6;
}

.info-item .icon {
  color: #6366f1;
  width: 20px;
  text-align: center;
  transition: color 0.3s;
}

:root.dark .info-item .icon {
  color: #818cf8;
}

.info-item .label {
  font-weight: 600;
  color: #4b5563;
  min-width: 80px;
  transition: color 0.3s;
}

:root.dark .info-item .label {
  color: #9ca3af;
}

.map-button {
  margin-left: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: transparent;
  border: none;
  color: #6366f1;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.3s;
}

:root.dark .map-button {
  color: #818cf8;
}

.map-button:hover {
  color: #4f46e5;
}

:root.dark .map-button:hover {
  color: #a78bfa;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 700;
}

.status-공연중 {
  background-color: #10b981;
  color: white;
}

.status-공연예정 {
  background-color: #3b82f6;
  color: white;
}

.status-공연완료 {
  background-color: #6b7280;
  color: white;
}

.booking-section {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  transition: background 0.3s;
}

:root.dark .booking-section {
  background: #1a1a1a;
}

.booking-section h3 {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .booking-section h3 {
  color: #f3f4f6;
}

.booking-section h3 i {
  color: #6366f1;
  margin-right: 0.5rem;
  transition: color 0.3s;
}

:root.dark .booking-section h3 i {
  color: #818cf8;
}

.booking-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.booking-link {
  padding: 0.5rem 1rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  text-decoration: none;
  border-radius: 9999px;
  font-size: 0.9rem;
  transition: all 0.3s;
  font-weight: 600;
}

.booking-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.booking-link i {
  font-size: 0.75rem;
  margin-left: 0.25rem;
}

/* 찜하기 버튼 */
.action-buttons {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.like-button,
.watched-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 9999px;
  font-size: 1rem;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s;
}

:root.dark .like-button {
  border-color: #374151;
  background: #2c2c2c;
  color: #9ca3af;
}

.like-button:hover:not(:disabled) {
  border-color: #ef4444;
  color: #ef4444;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.like-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.like-button.liked {
  border-color: #ef4444;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.like-button.liked:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.like-button i {
  font-size: 1.1rem;
}

.like-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 700;
}

.like-button:not(.liked) .like-count {
  background: #f3f4f6;
  color: #6b7280;
}

:root.dark .like-button:not(.liked) .like-count {
  background: #374151;
  color: #9ca3af;
}

/* 봤어요 버튼 스타일 */
:root.dark .watched-button {
  border-color: #374151;
  background: #2c2c2c;
  color: #9ca3af;
}

.watched-button:hover:not(:disabled) {
  border-color: #6366f1;
  color: #6366f1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.watched-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.watched-button.watched {
  border-color: #6366f1;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
}

.watched-button.watched:hover:not(:disabled) {
  background: linear-gradient(135deg, #4f46e5, #4338ca);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.watched-button i {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .header-section {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .poster-section {
    max-width: 300px;
    margin: 0 auto;
  }

  .poster-large {
    width: 100%;
  }

  .info-grid {
    text-align: left;
  }
}
</style>
