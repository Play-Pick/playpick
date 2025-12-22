<template>
  <div class="page-wrapper">
    <div class="detail-container">
      <div v-if="loading" class="loading">로딩 중...</div>

      <div v-else-if="error" class="error">
        {{ error }}
        <button @click="goBack" class="back-button">목록으로</button>
      </div>

      <div v-else-if="currentArticle">
        <!-- 헤더 -->
        <div class="card header-card">
          <div class="header-row">
            <div>
              <div class="chip-row">
                <span class="chip tone">{{ boardTypeLabel }}</span>
                <span class="chip">{{ categoryLabel }}</span>
              </div>
              <h1 class="title">{{ currentArticle.title }}</h1>
              <div class="meta">
                <span class="author">{{ currentArticle.username }}</span>
                <span class="divider">·</span>
                <span class="date">{{ formatDate(currentArticle.created_at) }}</span>
              </div>
            </div>
            <div class="like-box">
              <button
                class="like-button"
                :disabled="likeLoading"
                @click="handleLike"
                aria-label="좋아요"
              >
                <i :class="currentArticle.is_liked ? 'fas fa-heart liked' : 'far fa-heart'"></i>
              </button>
              <span class="like-count">{{ currentArticle.like_count }}</span>
            </div>
          </div>
        </div>

        <!-- 통합 카드: 공연정보 + 본문 + 댓글 -->
        <div class="card content-card">
          <div class="card-head perf-head">
            <h3>관련 공연</h3>
          </div>
          <div class="perf-info">
            <div class="side-text">
              <p class="side-title">{{ currentArticle.performance_name }}</p>
              <p v-if="currentArticle.performance_area" class="side-sub">{{ currentArticle.performance_area }}</p>
              <p v-if="periodText" class="side-sub">{{ periodText }}</p>
              <p v-if="currentArticle.rank" class="side-rating">평점 ★{{ currentArticle.rank }}</p>
              <p v-if="!currentArticle.performance_area && !periodText && !currentArticle.rank" class="side-placeholder">
                공연 정보가 없습니다.
              </p>
            </div>
            <button @click="goToPerformance" class="link-button">공연상세보기</button>
          </div>

          <div class="divider-line"></div>

          <div class="article-body">
            <p>{{ currentArticle.content }}</p>
          </div>

          <div class="divider-line"></div>

          <div class="comments-card">
            <CommentForm
              :is-authenticated="authStore.isAuthenticated"
              :comment-count="comments?.length || 0"
              :loading="commentLoading"
              @submit="submitComment"
            />
            <div class="comment-list-wrapper">
              <CommentList
                :comments="comments"
                :current-username="authStore.user?.username"
                @update="updateComment"
                @delete="deleteComment"
              />
            </div>
          </div>

          <div class="actions">
            <button @click="goBack" class="back-button">목록으로</button>
            <div v-if="authStore.user?.username === currentArticle.username" class="owner-actions">
              <button @click="editArticle" class="edit-button">수정</button>
              <button @click="deleteArticle" class="delete-button">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { storeToRefs } from 'pinia'
import { useCommunityStore } from '@/stores/communityStore'
import CommentForm from '@/components/Community/CommentForm.vue'
import CommentList from '@/components/Community/CommentList.vue'
import { useArticleDetail } from '@/composables/useArticleDetail'

const categoryMap = {
  REVIEW: '관람후기',
  EXPECTATION: '기대평',
  QNA: '질문',
  FREE: '자유게시판',
  INFO: '정보공유'
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const communityStore = useCommunityStore()
const { currentArticle, comments, loading, error } = storeToRefs(communityStore)

const {
  likeLoading,
  commentLoading,
  handleLike,
  submitComment,
  updateComment,
  deleteComment,
  editArticle,
  deleteArticle,
  goBack,
  loadArticleData
} = useArticleDetail(route.params.id)

const categoryLabel = computed(() => categoryMap[currentArticle.value?.category] || currentArticle.value?.category)
const boardTypeLabel = computed(() =>
  currentArticle.value?.board_type === 'GENERAL' ? '자유/정보' : '공연글'
)
const periodText = computed(() => {
  const from = currentArticle.value?.prfpdfrom
  const to = currentArticle.value?.prfpdto
  if (from && to) return `${from} ~ ${to}`
  return ''
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const goToPerformance = () => {
  if (currentArticle.value?.performance) {
    router.push(`/performances/${currentArticle.value.performance}`)
  }
}

onMounted(() => {
  loadArticleData()
})

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadArticleData()
    }
  }
)
</script>

<style scoped>
.page-wrapper {
  background: var(--bg-page);
  min-height: 100vh;
  padding: 2rem 0;
  font-family: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem 3rem;
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
}

.error {
  color: var(--color-danger);
}

.card {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-xl);
  transition: box-shadow 0.2s, transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.header-card {
  margin-bottom: 1.5rem;
  text-align: left;
}

.header-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.chip-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.chip {
  display: inline-flex;
  align-items: center;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: 0.85rem;
  background: #eef2ff;
  color: #4338ca;
}

.chip.tone {
  background: #e0f2fe;
  color: #075985;
}

:root.dark .chip {
  background: var(--bg-card-secondary);
  color: #c7d2fe;
}

.title {
  margin: 0.75rem 0 0.35rem;
  font-size: 2rem;
  line-height: 1.3;
  color: var(--text-primary);
}

.meta {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.divider {
  opacity: 0.6;
}

.like-box {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  margin-left: auto;
  padding: 0.25rem 0.7rem;
  background: #fdf2f2;
  border-radius: 9999px;
  border: 1px solid #fecdd3;
  transform: translateY(6px);
}

:root.dark .like-box {
  background: #2b1414;
  border-color: #7f1d1d;
}

.like-button {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.6rem;
  padding: 0.15rem;
  transition: transform 0.2s ease;
  color: var(--color-danger);
}

.like-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.like-button:hover:not(:disabled) {
  transform: translateY(1px) scale(1.08);
}

.like-count {
  font-weight: 800;
  color: var(--color-danger);
  font-size: 1.05rem;
}

.content-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.perf-head {
  margin-bottom: 0.25rem;
}

.perf-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 0.25rem 0.75rem 0.5rem 0.75rem;
}

.card-head h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
}

.link-button {
  border: none;
  background: #e5e7eb;
  color: #111827;
  border-radius: var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.link-button:hover {
  background: #d1d5db;
}

:root.dark .link-button {
  background: var(--bg-card-secondary);
  color: #e2e8f0;
}

:root.dark .link-button:hover {
  background: #334155;
}

.divider-line {
  border-bottom: 1px solid var(--border-color);
  margin: var(--spacing-sm) 0 var(--spacing-md);
}

.article-body {
  line-height: 1.8;
  font-size: 1rem;
  color: var(--text-primary);
  white-space: pre-wrap;
  min-height: 120px;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-sm);
}

.comments-card {
  padding-bottom: 1.5rem;
}

.comment-list-wrapper {
  margin-top: 0.5rem;
  padding: 0 0.75rem 0 0.75rem;
}

.comments-card :deep(.comment-item) {
  padding: 1rem 0.75rem 1rem 1.25rem;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.back-button {
  padding: var(--spacing-md) var(--spacing-xl);
  background: #e5e7eb;
  color: #111827;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.back-button:hover {
  background: #d1d5db;
}

:root.dark .back-button {
  background: var(--bg-card-secondary);
  color: #e2e8f0;
}

:root.dark .back-button:hover {
  background: #334155;
}

.owner-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button,
.delete-button {
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.edit-button {
  background: var(--color-primary);
}

.edit-button:hover {
  background: var(--color-primary-hover);
}

.delete-button {
  background: var(--color-danger);
}

.delete-button:hover {
  background: var(--color-danger-hover);
}

.side-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.side-title {
  margin: 0;
  font-weight: 800;
  color: var(--text-primary);
}

.side-sub,
.side-rating,
.side-placeholder {
  margin: 0;
  color: var(--text-secondary);
  font-weight: 600;
}
</style>
