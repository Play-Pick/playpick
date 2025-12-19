<template>
  <div class="comment-form-wrapper">
    <h3>댓글 {{ commentCount }}</h3>

    <div v-if="isAuthenticated" class="comment-form">
      <textarea
        v-model="commentText"
        placeholder="댓글을 작성하세요..."
        rows="3"
      ></textarea>
      <button
        @click="handleSubmit"
        :disabled="!commentText.trim() || loading"
        class="submit-button"
      >
        {{ loading ? '작성 중...' : '댓글 작성' }}
      </button>
    </div>
    <p v-else class="login-required">댓글을 작성하려면 로그인이 필요합니다.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  isAuthenticated: {
    type: Boolean,
    required: true
  },
  commentCount: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const commentText = ref('')

const handleSubmit = () => {
  if (!commentText.value.trim()) return

  emit('submit', commentText.value.trim())
  commentText.value = ''
}
</script>

<style scoped>
.comment-form-wrapper {
  margin-bottom: 2rem;
}

h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  resize: vertical;
  font-family: inherit;
}

.comment-form .submit-button {
  margin-top: 0.5rem;
  padding: 0.6rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.comment-form .submit-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.comment-form .submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #95a5a6;
}

.login-required {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #666;
  text-align: center;
  margin-bottom: 1.5rem;
}
</style>
