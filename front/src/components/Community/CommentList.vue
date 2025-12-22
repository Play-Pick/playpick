<template>
  <div class="comments-wrapper">
    <div v-if="comments && comments.length > 0" class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.username }}</span>
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
  margin-top: 2rem;
}

.no-comments {
  padding: 1.25rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #666;
  text-align: center;
  margin-bottom: 1.5rem;
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s;
}

:root.dark .no-comments {
  background-color: #374151;
  color: #9ca3af;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  padding: 1.25rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  position: relative;
  transition: background-color 0.3s, box-shadow 0.3s;
}

:root.dark .comment-item {
  background-color: #374151;
}

.comment-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:root.dark .comment-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.comment-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.comment-author {
  font-weight: 700;
  color: #2c3e50;
  font-size: 0.95rem;
  transition: color 0.3s;
}

:root.dark .comment-author {
  color: #f3f4f6;
}

.comment-date {
  color: #95a5a6;
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.3s;
}

:root.dark .comment-date {
  color: #9ca3af;
}

.comment-content {
  margin: 0;
  color: #333;
  line-height: 1.7;
  font-size: 0.95rem;
  transition: color 0.3s;
}

:root.dark .comment-content {
  color: #d1d5db;
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
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.comment-item .edit-button {
  background-color: #6366f1;
  color: white;
}

.comment-item .edit-button:hover {
  background-color: #4f46e5;
}

.comment-item .delete-button {
  background-color: #e74c3c;
  color: white;
}

.comment-item .delete-button:hover {
  background-color: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

:root.dark .comment-item .delete-button {
  background-color: #dc2626;
}

:root.dark .comment-item .delete-button:hover {
  background-color: #b91c1c;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.4);
}

.edit-area {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.edit-area textarea {
  width: 100%;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  resize: vertical;
  font-size: 0.95rem;
  background: white;
  color: #1f2937;
}

:root.dark .edit-area textarea {
  background: #1f2937;
  color: #f3f4f6;
  border-color: #374151;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-save,
.btn-cancel {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
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
  background: #374151;
  color: #e2e8f0;
}
</style>
