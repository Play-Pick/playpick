<template>
  <div class="ai-search-card" @click="handleClick">
    <!-- Rank Badge -->
    <div class="rank-badge" :class="getRankClass(rank)">
      {{ rank }}
    </div>

    <!-- Poster with overlays -->
    <div class="poster-container">
      <img
        :src="performance.poster || '/no_poster.png'"
        :alt="`${performance.prfnm} 포스터`"
        class="poster"
        @error="handleImageError"
      />

      <!-- Similarity Score Badge -->
      <div class="similarity-badge">
        <i class="fas fa-brain"></i>
        {{ (performance.similarity_score * 100).toFixed(0) }}%
      </div>

      <!-- Genre badge -->
      <span v-if="performance.genrenm" class="genre-badge">
        {{ performance.genrenm }}
      </span>

      <!-- Like button -->
      <button
        @click.stop="handleLikeClick"
        :class="['like-button', { liked: performance.is_liked }]"
        :title="performance.is_liked ? '찜 취소' : '찜하기'"
      >
        <i :class="performance.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
      </button>
    </div>

    <!-- Card info -->
    <div class="card-info">
      <h3 class="title">{{ performance.prfnm }}</h3>
      <p class="venue">{{ performance.fcltynm }}</p>
      <p class="date">{{ formatDateRange(performance.prfpdfrom, performance.prfpdto) }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  performance: {
    type: Object,
    required: true
  },
  rank: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['click', 'toggle-like'])

const handleClick = () => {
  emit('click', props.performance.mt20id)
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

const getRankClass = (rank) => {
  if (rank === 1) return 'gold'
  if (rank === 2) return 'silver'
  if (rank === 3) return 'bronze'
  return ''
}
</script>

<style scoped>
.ai-search-card {
  position: relative;
  cursor: pointer;
  border: 1px solid var(--card-border);
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.3s;
  background: var(--card-surface);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.ai-search-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: var(--primary-color);
}

/* Rank Badge */
.rank-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  width: 32px;
  height: 32px;
  background: var(--text-secondary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.rank-badge.gold {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #000;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5);
}

.rank-badge.silver {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
  color: #000;
  box-shadow: 0 4px 12px rgba(192, 192, 192, 0.5);
}

.rank-badge.bronze {
  background: linear-gradient(135deg, #cd7f32 0%, #e6a664 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(205, 127, 50, 0.5);
}

/* Poster Container */
.poster-container {
  position: relative;
  width: 100%;
  margin-bottom: 1rem;
}

.poster {
  width: 100%;
  height: auto;
  aspect-ratio: 3/4;
  object-fit: cover;
  border-radius: 0.5rem;
  background: #f3f4f6;
  display: block;
}

/* Similarity Badge */
.similarity-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

/* Genre Badge */
.genre-badge {
  position: absolute;
  bottom: 0.5rem;
  left: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  z-index: 1;
}

/* Like Button */
.like-button {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: none;
  border-radius: 50%;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1;
}

.like-button:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 1);
}

.like-button.liked {
  background: #ff4757;
  color: white;
}

.like-button.liked:hover {
  background: #ee5a6f;
}

/* Card Info */
.card-info {
  padding: 0.25rem 0;
  display: flex;
  flex-direction: column;
  min-height: 120px;
}

.title {
  margin: 0.5rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--card-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  min-height: 2.8rem;
}

.venue,
.date {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: var(--card-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-height: 1.25rem;
}

.date {
  font-size: 0.75rem;
  min-height: 1.125rem;
}

/* Dark mode adjustments */
:root.dark .genre-badge {
  background: rgba(255, 255, 255, 0.2);
}

:root.dark .poster {
  background: #374151;
}

:root.dark .like-button {
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

:root.dark .like-button:hover {
  background: rgba(0, 0, 0, 0.9);
}

/* Backdrop-filter fallback */
@supports not (backdrop-filter: blur(8px)) {
  .genre-badge {
    background: rgba(0, 0, 0, 0.85);
  }

  .like-button {
    background: rgba(255, 255, 255, 0.95);
  }

  :root.dark .genre-badge {
    background: rgba(255, 255, 255, 0.25);
  }

  :root.dark .like-button {
    background: rgba(0, 0, 0, 0.85);
  }
}
</style>
