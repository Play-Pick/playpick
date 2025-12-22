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
      <!-- 말머리 -->
      <CategoryDisplay
        label="말머리"
        icon="fas fa-tag"
        :text="boardTypeLabel"
      />

      <!-- 카테고리 -->
      <CategoryDisplay
        label="카테고리"
        :icon="categoryIcon"
        :text="categoryLabel"
      />

      <!-- 연결된 공연 (공연글인 경우) -->
      <div v-if="form.board_type === 'PERFORMANCE'" class="form-group">
        <label>연결된 공연</label>
        <div class="performance-pill">
          {{ performanceDisplay }}
        </div>
      </div>

      <!-- 제목, 별점, 내용 -->
      <ArticleFormFields
        v-model:title="form.title"
        v-model:content="form.content"
        v-model:rating="form.rank"
        :show-rating="showRating"
        :rows="10"
      />

      <!-- 버튼 -->
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
import { useArticleForm } from '@/composables/useArticleForm'
import communityAPI from '@/api/community'
import CategoryDisplay from '@/components/Community/CategoryDisplay.vue'
import ArticleFormFields from '@/components/Community/ArticleFormFields.vue'

const route = useRoute()
const router = useRouter()
const communityStore = useCommunityStore()

// useArticleForm composable 사용
const {
  submitting,
  getCategoryIcon,
  getCategoryLabel,
  getBoardTypeLabel,
  needsRating,
  goBack
} = useArticleForm()

const form = ref({
  board_type: '',
  category: '',
  performance: null,
  performance_name: '',
  title: '',
  content: '',
  rank: 0,
})

const loading = ref(true)
const error = ref(null)

// 말머리 라벨
const boardTypeLabel = computed(() => getBoardTypeLabel(form.value.board_type))

// 카테고리 라벨 및 아이콘
const categoryLabel = computed(() => getCategoryLabel(form.value.category))
const categoryIcon = computed(() => getCategoryIcon(form.value.category))

// 공연 표시
const performanceDisplay = computed(() => {
  if (!form.value.performance_name) return '연결된 공연 없음'
  return `${form.value.performance_name} (${form.value.performance})`
})

// 별점 표시 여부
const showRating = computed(() => {
  return form.value.board_type === 'PERFORMANCE' && needsRating(form.value.category)
})

// 게시글 불러오기
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

// 게시글 수정 제출
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
    if (showRating.value) {
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
  transition: color 0.3s;
  color: #111827;
}

:root.dark .page-header h1 {
  color: #f3f4f6;
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
  gap: 1.5rem;
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
  font-size: 1.0625rem;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #e2e8f0;
}

.performance-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.9375rem;
  transition: all 0.3s;
}

:root.dark .performance-pill {
  background: #1f2937;
  color: #e2e8f0;
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
