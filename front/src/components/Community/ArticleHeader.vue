<template>
  <div class="article-header">
    <div class="category-section">
      <span class="badge" :style="{ backgroundColor: categoryColor }">
        {{ categoryLabel }}
      </span>
    </div>
    <h1 class="article-title">{{ article.title }}</h1>
    <div class="article-meta">
      <span class="author">{{ article.username }}</span>
      <span class="date">{{ formattedDate }}</span>
      <div class="like-section">
        <button @click="handleLike" class="like-button" :disabled="likeLoading">
          {{ article.is_liked ? '❤️' : '🤍' }}
        </button>
        <span class="like-count">{{ article.like_count }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCategoryLabels } from '@/composables/useCategoryLabels'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  likeLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['like'])

const { getCategoryLabel, getCategoryColor } = useCategoryLabels()

const categoryLabel = computed(() => getCategoryLabel(props.article.category))
const categoryColor = computed(() => getCategoryColor(props.article.category))

const formattedDate = computed(() => {
  const date = new Date(props.article.created_at)
  const now = new Date()
  const diff = now - date
  const diffHours = Math.floor(diff / (1000 * 60 * 60))
  const diffDays = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (diffHours < 1) {
    const diffMinutes = Math.floor(diff / (1000 * 60))
    return `${diffMinutes}분 전`
  } else if (diffHours < 24) {
    return `${diffHours}시간 전`
  } else if (diffDays < 7) {
    return `${diffDays}일 전`
  } else {
    return date.toLocaleDateString('ko-KR')
  }
})

const handleLike = () => {
  console.log('Before like:', props.article.is_liked)
  emit('like')
}
</script>

<style scoped>
.article-header {
  padding: 2.5rem 2rem;
  border-bottom: 2px solid #f0f0f0;
  background: transparent;
  transition: border-color 0.3s, background-color 0.3s;
}

:root.dark .article-header {
  border-bottom-color: #374151;
  background: transparent;
}

.category-section {
  margin-bottom: 1.5rem;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: white;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-title {
  margin: 0 0 1.5rem 0;
  font-size: 2.25rem;
  font-weight: 800;
  color: #2c3e50;
  line-height: 1.3;
  letter-spacing: -0.5px;
  transition: color 0.3s;
}

:root.dark .article-title {
  color: #f9fafb;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  color: #666;
  font-size: 0.95rem;
}

.author {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1.05rem;
  transition: color 0.3s;
}

:root.dark .author {
  color: #f3f4f6;
}

.date {
  color: #95a5a6;
  font-weight: 500;
  transition: color 0.3s;
}

:root.dark .date {
  color: #9ca3af;
}

.like-section {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-left: auto;
  padding: 0.5rem 0;
  background: transparent;
  transition: all 0.3s;
}

:root.dark .like-section {
  background: transparent;
}

.like-button {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s, filter 0.2s;
}

.like-button:hover:not(:disabled) {
  transform: scale(1.2);
  filter: brightness(1.1);
}

.like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.like-count {
  font-size: 1.05rem;
  font-weight: 700;
  color: #e74c3c;
  transition: color 0.3s;
}

:root.dark .like-count {
  color: #f87171;
}
</style>
