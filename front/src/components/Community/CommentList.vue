<template>
  <div class="comments-wrapper">
    <div v-if="comments && comments.length > 0" class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.nickname || comment.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <div v-if="isEditing(comment.id)" class="edit-area">
          <textarea v-model="editContent" rows="3"></textarea>
          <div class="edit-actions">
            <button @click="saveEdit(comment.id)" class="btn-save">저장</button>
            <button @click="cancelEdit" class="btn-cancel">취소</button>
          </div>
        </div>
        <p v-else class="comment-content">{{ comment.content }}</p>

        <div class="comment-actions" v-if="canManage(comment)">
          <button @click="startEdit(comment)" class="edit-button">수정</button>
          <button @click="handleDelete(comment.id)" class="delete-button">삭제</button>
        </div>
      </div>
    </div>
    <p v-else class="no-comments">아직 댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

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

const emit = defineEmits(['delete', 'update'])

const editingId = ref(null)
const editContent = ref('')

const canManage = (comment) => {
  return props.currentUsername && props.currentUsername === comment.username
}

const startEdit = (comment) => {
  editingId.value = comment.id
  editContent.value = comment.content
}

const cancelEdit = () => {
  editingId.value = null
  editContent.value = ''
}

const saveEdit = (commentId) => {
  if (!editContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }
  emit('update', { id: commentId, content: editContent.value.trim() })
  cancelEdit()
}

const handleDelete = (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  emit('delete', commentId)
}

const isEditing = (id) => editingId.value === id

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
  margin-top: var(--spacing-2xl);
}

.no-comments {
  padding: var(--spacing-lg);
  background-color: var(--bg-card-secondary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: var(--spacing-xl);
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.comment-item {
  padding: var(--spacing-lg);
  background-color: var(--bg-card-secondary);
  border-radius: var(--radius-md);
  position: relative;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.comment-item:hover {
  box-shadow: var(--shadow-sm);
}

.comment-header {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.comment-author {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: color 0.3s;
}

.comment-date {
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.3s;
}

.comment-content {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.7;
  font-size: 0.95rem;
  transition: color 0.3s;
}

.comment-actions {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.35rem;
}

.comment-item .edit-button,
.comment-item .delete-button {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s;
}

.comment-item .edit-button {
  background-color: var(--color-primary);
  color: white;
}

.comment-item .edit-button:hover {
  background-color: var(--color-primary-hover);
}

.comment-item .delete-button {
  background-color: var(--color-danger);
  color: white;
}

.comment-item .delete-button:hover {
  background-color: var(--color-danger-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

.edit-area {
  margin-top: var(--spacing-sm);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.edit-area textarea {
  width: 100%;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  border: 2px solid var(--border-color);
  resize: vertical;
  font-size: 0.95rem;
  background: var(--bg-card);
  color: var(--text-primary);
  transition: border-color 0.3s;
}

.edit-area textarea:focus {
  outline: none;
  border-color: var(--border-color-focus);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.edit-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-save,
.btn-cancel {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
}

.btn-save {
  background: #10b981;
  color: white;
}

.btn-cancel {
  background: #e5e7eb;
  color: #374151;
}

:root.dark .btn-cancel {
  background: var(--bg-card-secondary);
  color: #e2e8f0;
}
</style>
