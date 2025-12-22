<template>
  <div class="performance-card" @click="handleClick">
    <!-- Poster with overlays -->
    <div class="poster-container">
      <img
        :src="performance.poster || '/no_poster.png'"
        :alt="`${performance.prfnm} 포스터`"
        class="poster"
        @error="handleImageError"
      />

      <!-- Genre badge overlay -->
      <span v-if="performance.genrenm" class="genre-badge card-badge-overlay">
        {{ performance.genrenm }}
      </span>

      <!-- Like button overlay -->
      <button
        v-if="showLikeButton"
        @click.stop="handleLikeClick"
        :disabled="likeLoading"
        :class="['card-like-button', { liked: performance.is_liked }]"
        :title="performance.is_liked ? '찜 취소' : '찜하기'"
        :aria-label="performance.is_liked ? `${performance.prfnm} 찜 취소` : `${performance.prfnm} 찜하기`"
        :aria-pressed="performance.is_liked"
      >
        <i :class="performance.is_liked ? 'fas fa-heart' : 'far fa-heart'"></i>
      </button>
    </div>

    <!-- Card info -->
    <h3>{{ performance.prfnm }}</h3>
    <p class="venue">{{ performance.fcltynm }}</p>
    <p class="date">{{ formatDateRange(performance.prfpdfrom, performance.prfpdto) }}</p>
  </div>
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
</script>

<style scoped>
.performance-card {
  cursor: pointer;
  border: 1px solid var(--card-border);
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.3s;
  background: var(--card-surface);
}

.performance-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--card-accent);
}

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

.performance-card h3 {
  margin: 0.5rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--card-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.performance-card p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

.venue {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.date {
  font-size: 0.75rem;
}

.genre-badge {
  background: var(--badge-bg-dark);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 4px;
}

/* Dark mode adjustments */
:root.dark .genre-badge {
  background: var(--badge-bg-light);
}

:root.dark .poster {
  background: #374151;
}

/* Backdrop-filter fallback */
@supports not (backdrop-filter: blur(8px)) {
  .genre-badge {
    background: rgba(0, 0, 0, 0.7);
  }

  :root.dark .genre-badge {
    background: rgba(255, 255, 255, 0.25);
  }
}
</style>
