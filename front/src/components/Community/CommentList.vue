<template>
  <div class="comments-wrapper">
    <div v-if="comments && comments.length > 0" class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <button
          v-if="canDelete(comment)"
          @click="handleDelete(comment.id)"
          class="delete-button"
        >
          삭제
        </button>
      </div>
    </div>
    <p v-else class="no-comments">아직 댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  currentUsername: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['delete'])

const canDelete = (comment) => {
  return props.currentUsername && props.currentUsername === comment.username
}

const handleDelete = (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  emit('delete', commentId)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
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
}
</script>

<style scoped>
.comments-wrapper {
  margin-top: 2rem;
}

.no-comments {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #666;
  text-align: center;
  margin-bottom: 1.5rem;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  position: relative;
}

.comment-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
}

.comment-date {
  color: #95a5a6;
  font-size: 0.85rem;
}

.comment-content {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.comment-item .delete-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment-item .delete-button:hover {
  background-color: #c0392b;
}
</style>
