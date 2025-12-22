<template>
  <div class="edit-article-page">
    <div class="page-header">
      <button @click="goBack" class="back-button">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h1>게시글 수정</h1>
    </div>

    <div v-if="loading" class="loading">로딩중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <form v-else class="edit-form" @submit.prevent="submit">
      <div class="form-group">
        <label>말머리</label>
        <div class="pill">{{ boardTypeLabel }}</div>
      </div>

      <div class="form-group">
        <label>카테고리</label>
        <div class="pill">{{ categoryLabel }}</div>
      </div>

      <div class="form-group" v-if="form.board_type === 'PERFORMANCE'">
        <label>연결된 공연</label>
        <div class="pill">
          {{ performanceDisplay }}
        </div>
      </div>

      <div
        class="form-group"
        v-if="form.board_type === 'PERFORMANCE' && (form.category === 'REVIEW' || form.category === 'EXPECTATION')"
      >
        <label>별점</label>
        <div class="rating-input">
          <button
            v-for="star in 5"
            :key="star"
            type="button"
            :class="['star', { active: star <= form.rank }]"
            @click="form.rank = star"
          >
            <i :class="star <= form.rank ? 'fas fa-star' : 'far fa-star'"></i>
          </button>
          <span class="rating-value">{{ form.rank.toFixed(1) }}</span>
        </div>
      </div>

      <div class="form-group">
        <label>제목</label>
        <input v-model="form.title" type="text" required />
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea v-model="form.content" rows="10" required></textarea>
      </div>

      <div class="actions">
        <button type="submit" class="btn-primary" :disabled="submitting">
          {{ submitting ? '수정 중...' : '수정 완료' }}
        </button>
        <button type="button" class="btn-secondary" @click="goBack">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/communityStore'
import communityAPI from '@/api/community'

const route = useRoute()
const router = useRouter()
const communityStore = useCommunityStore()

const form = ref({
  board_type: '',
  category: '',
  performance: null,
  title: '',
  content: '',
  rank: 0,
})

const loading = ref(true)
const submitting = ref(false)
const error = ref(null)

const boardTypeLabel = computed(() =>
  form.value.board_type === 'GENERAL' ? '자유/정보' : '공연글'
)

const categoryLabel = computed(() => {
  const map = {
    REVIEW: '관람후기',
    EXPECTATION: '기대평',
    QNA: '질문',
    FREE: '자유게시판',
    INFO: '정보공유',
  }
  return map[form.value.category] || form.value.category
})

const performanceDisplay = computed(() => {
  if (!form.value.performance_name) return '연결된 공연 없음'
  return `${form.value.performance_name} (${form.value.performance})`
})

const loadArticle = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await communityAPI.getArticle(route.params.id)
    const data = response.data
    form.value.board_type = data.board_type
    form.value.category = data.category
    form.value.performance = data.performance || null
    form.value.performance_name = data.performance_name || ''
    form.value.title = data.title
    form.value.content = data.content
    form.value.rank = data.rank || 0
  } catch (err) {
    console.error('게시글 불러오기 실패:', err)
    error.value = '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const submit = async () => {
  submitting.value = true
  error.value = null
  try {
    const payload = {
      board_type: form.value.board_type,
      category: form.value.category,
      title: form.value.title,
      content: form.value.content,
    }
    if (form.value.performance) payload.performance = form.value.performance
    if (form.value.board_type === 'PERFORMANCE' && (form.value.category === 'REVIEW' || form.value.category === 'EXPECTATION')) {
      payload.rank = form.value.rank || 0
    }

    await communityStore.updateArticle(route.params.id, payload)
    router.push(`/community/${route.params.id}`)
  } catch (err) {
    console.error('게시글 수정 실패:', err)
    error.value = '게시글 수정에 실패했습니다.'
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadArticle()
})
</script>

<style scoped>
.edit-article-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
}

.back-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
  color: #374151;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:root.dark .back-button {
  background: #1f2937;
  color: #e2e8f0;
}

.back-button:hover {
  transform: scale(1.05);
}

.edit-form {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .edit-form {
  background: #111827;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 700;
  color: #374151;
}

:root.dark .form-group label {
  color: #e2e8f0;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 9999px;
  font-weight: 600;
}

:root.dark .pill {
  background: #1f2937;
  color: #e2e8f0;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.star {
  background: none;
  border: none;
  cursor: pointer;
  color: #d1d5db;
  font-size: 1.5rem;
}

.star.active {
  color: #fbbf24;
}

.rating-value {
  margin-left: 0.5rem;
  font-weight: 700;
  color: #6366f1;
}

:root.dark .rating-value {
  color: #c7d2fe;
}

input,
textarea {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  background: #fff;
  color: #111827;
  transition: border-color 0.3s, box-shadow 0.3s, background 0.3s, color 0.3s;
}

:root.dark input,
:root.dark textarea {
  background: #0f172a;
  color: #e2e8f0;
  border-color: #334155;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

:root.dark input:focus,
:root.dark textarea:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25);
}

.actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 0.9rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

:root.dark .btn-secondary {
  background: #1f2937;
  color: #e2e8f0;
}

.btn-secondary:hover {
  background: #d1d5db;
}

:root.dark .btn-secondary:hover {
  background: #334155;
}

.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

:root.dark .loading,
:root.dark .error {
  color: #e2e8f0;
}

.error {
  color: #dc2626;
}

:root.dark .error {
  color: #fca5a5;
}

@media (max-width: 768px) {
  .edit-form {
    padding: 1.5rem;
  }

  .actions {
    flex-direction: column;
  }
}
</style>
