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
  font-size: 1.4rem;
  font-weight: 800;
  color: #2c3e50;
  letter-spacing: -0.3px;
  transition: color 0.3s;
}

:root.dark h3 {
  color: #f9fafb;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  resize: vertical;
  font-family: inherit;
  background: white;
  color: #2c3e50;
  transition: border-color 0.3s, background-color 0.3s, color 0.3s;
}

:root.dark .comment-form textarea {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #3498db;
}

:root.dark .comment-form textarea:focus {
  border-color: #6366f1;
  background: #4b5563;
}

.comment-form textarea::placeholder {
  color: #9ca3af;
}

:root.dark .comment-form textarea::placeholder {
  color: #6b7280;
}

.comment-form .submit-button {
  margin-top: 0.75rem;
  padding: 0.75rem 1.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 700;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-form .submit-button:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

:root.dark .comment-form .submit-button {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

:root.dark .comment-form .submit-button:hover:not(:disabled) {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
}

.comment-form .submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #95a5a6;
  transform: none;
}

:root.dark .comment-form .submit-button:disabled {
  background: #4b5563;
  color: #9ca3af;
}

.login-required {
  padding: 1.25rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #666;
  text-align: center;
  margin-bottom: 1.5rem;
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s;
}

:root.dark .login-required {
  background-color: #374151;
  color: #9ca3af;
}
</style>
