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
  padding: 2rem;
  border-bottom: 2px solid #f0f0f0;
}

.category-section {
  margin-bottom: 1rem;
}

.badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  color: white;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
}

.article-title {
  margin: 0 0 1rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.4;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.author {
  font-weight: 600;
  color: #2c3e50;
}

.date {
  color: #95a5a6;
}

.like-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

.like-button {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s;
}

.like-button:hover:not(:disabled) {
  transform: scale(1.2);
}

.like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.like-count {
  font-size: 1rem;
  font-weight: 600;
  color: #e74c3c;
}
</style>
