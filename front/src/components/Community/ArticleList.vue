<template>
  <div class="articles-list">
    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="articles.length === 0" class="empty">
      게시글이 없습니다.
    </div>

    <ArticleCard
      v-for="article in articles"
      :key="article.id"
      :article="article"
      @like="handleLike"
    />
  </div>
</template>

<script setup>
import ArticleCard from './ArticleCard.vue'

defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['like'])

const handleLike = (articleId) => {
  emit('like', articleId)
}
</script>

<style scoped>
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem;
  font-size: 1rem;
}

.error {
  color: #e74c3c;
}

.empty {
  color: #95a5a6;
}

.loading {
  color: #3498db;
}
</style>
