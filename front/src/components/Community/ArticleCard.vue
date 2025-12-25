<template>
  <div class="article-card" @click="goToDetail">
    <div class="card-header">
      <div class="article-category">
        <span class="badge" :style="{ backgroundColor: categoryColor }">
          {{ categoryLabel }}
        </span>
      </div>
      <div class="like-section" @click.stop>
        <span class="like-count">{{ article.like_count }}</span>
        <button @click="handleLike" :disabled="loading" class="like-button">
          {{ article.is_liked ? '❤️' : '🤍' }}
        </button>
      </div>
    </div>

    <h3 class="article-title">{{ article.title }}</h3>

    <div class="article-info">
      <span class="performance-title">{{ article.performance_name }}</span>
      <span v-if="categoryLabel==='후기'" class="rating">⭐ {{ article.rank }}</span>
      <span class="author">{{ article.nickname || article.username }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryLabels } from '@/composables/common/useCategoryLabels'

const router = useRouter()

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['like'])

const { getCategoryLabel, getCategoryColor } = useCategoryLabels()
const loading = ref(false)

const categoryLabel = computed(() => getCategoryLabel(props.article.category))
const categoryColor = computed(() => getCategoryColor(props.article.category))

const goToDetail = () => {
  router.push(`/community/${props.article.id}`)
}

const handleLike = async () => {
  if (loading.value) return

  loading.value = true
  try {
    await emit('like', props.article.id)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.article-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  background-color: #fff;
  transition: all 0.2s;
  cursor: pointer;
}

.article-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-color: #3498db;
}

:root.dark .article-card {
  background-color: #111827;
  border-color: #1f2937;
  box-shadow: none;
}

:root.dark .article-card:hover {
  box-shadow: 0 2px 10px rgba(129, 140, 248, 0.25);
  border-color: #6366f1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  color: white;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}

.article-title {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-title:hover {
  color: #3498db;
}

:root.dark .article-title {
  color: #f8fafc;
}

:root.dark .article-title:hover {
  color: #c7d2fe;
}

.article-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: #666;
}

:root.dark .article-info {
  color: #cbd5e1;
}

.performance-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:root.dark .performance-title {
  color: #e2e8f0;
}

.rating {
  color: #f39c12;
  font-weight: 600;
  white-space: nowrap;
}

.author {
  color: #95a5a6;
  white-space: nowrap;
}

:root.dark .author {
  color: #cbd5e1;
}

.like-section {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.like-count {
  font-size: 0.75rem;
  color: #e74c3c;
  font-weight: 600;
}

:root.dark .like-count {
  color: #f87171;
}

.like-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s;
  line-height: 1;
}

.like-button:hover:not(:disabled) {
  transform: scale(1.15);
}

.like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
