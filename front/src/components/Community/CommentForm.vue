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
  margin-bottom: var(--spacing-2xl);
}

h3 {
  margin: 0 0 var(--spacing-xl) 0;
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.3px;
  transition: color 0.3s;
}

.comment-form {
  margin-bottom: var(--spacing-2xl);
}

.comment-form textarea {
  width: 100%;
  padding: var(--spacing-lg);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  resize: vertical;
  font-family: inherit;
  background: var(--bg-card);
  color: var(--text-primary);
  transition: border-color 0.3s, background-color 0.3s, color 0.3s;
}

.comment-form textarea:focus {
  outline: none;
  border-color: var(--border-color-focus);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.comment-form textarea::placeholder {
  color: var(--text-tertiary);
}

.comment-form .submit-button {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-xl);
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 700;
  transition: all 0.3s;
  box-shadow: var(--shadow-sm);
}

.comment-form .submit-button:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.comment-form .submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #95a5a6;
  transform: none;
}

.login-required {
  padding: var(--spacing-lg);
  background-color: var(--bg-card-secondary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: var(--spacing-xl);
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s;
}
</style>
