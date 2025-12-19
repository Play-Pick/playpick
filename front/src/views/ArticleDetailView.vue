<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="goBack" class="back-button">목록으로</button>
    </div>

    <div v-else-if="currentArticle" class="article-content">
      <!-- 헤더 -->
      <ArticleHeader
        :article="currentArticle"
        :like-loading="likeLoading"
        @like="handleLike"
      />

      <!-- 공연 정보 -->
      <div class="performance-section">
        <h3>관련 공연</h3>
        <div class="performance-info">
          <p class="performance-title">{{ currentArticle.performance_name }}</p>
          <button @click="goToPerformance" class="detail-button">상세보기 →</button>
        </div>
        <p v-if="currentArticle.rank" class="rating">평점: ⭐ {{ currentArticle.rank }}</p>
      </div>

      <!-- 본문 -->
      <div class="article-body">
        <p>{{ currentArticle.content }}</p>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <CommentForm
          :is-authenticated="authStore.isAuthenticated"
          :comment-count="comments?.length || 0"
          :loading="commentLoading"
          @submit="submitComment"
        />

        <CommentList
          :comments="comments"
          :current-username="authStore.user?.username"
          @delete="deleteComment"
        />
      </div>

      <!-- 하단 버튼 -->
      <div class="actions">
        <button @click="goBack" class="back-button">목록으로</button>
        <div v-if="authStore.user?.username === currentArticle.username" class="owner-actions">
          <button @click="editArticle" class="edit-button">수정</button>
          <button @click="deleteArticle" class="delete-button">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { storeToRefs } from 'pinia'
import { useCommunityStore } from '@/stores/communityStore'
import ArticleHeader from '@/components/Community/ArticleHeader.vue'
import CommentForm from '@/components/Community/CommentForm.vue'
import CommentList from '@/components/Community/CommentList.vue'
import { useArticleDetail } from '@/composables/useArticleDetail'

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
  deleteComment,
  editArticle,
  deleteArticle,
  goBack,
  loadArticleData
} = useArticleDetail(route.params.id)

// 관련 공연 상세 페이지로 이동
const goToPerformance = () => {
  if (currentArticle.value?.performance) {
    router.push(`/performances/${currentArticle.value.performance}`)
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadArticleData()
})

// 라우트 파라미터 변경 감지 (다른 게시글로 이동할 때)
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
.article-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}

.article-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.performance-section {
  padding: 1.5rem 2rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.performance-section h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

.performance-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0.5rem 0;
}

.performance-title {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 600;
  flex: 1;
}

.detail-button {
  padding: 0.4rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.detail-button:hover {
  background-color: #2980b9;
}

.rating {
  margin: 0.5rem 0 0 0;
  font-size: 1rem;
  color: #f39c12;
  font-weight: 600;
}

.article-body {
  padding: 2rem;
  line-height: 1.8;
  font-size: 1.05rem;
  color: #333;
  white-space: pre-wrap;
  min-height: 200px;
}

.comments-section {
  padding: 2rem;
  border-top: 2px solid #f0f0f0;
}

.actions {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e0e0e0;
}

.back-button {
  padding: 0.6rem 1.5rem;
  background-color: #95a5a6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
}

.back-button:hover {
  background-color: #7f8c8d;
}

.owner-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button,
.delete-button {
  padding: 0.6rem 1.2rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
}

.edit-button {
  background-color: #3498db;
}

.edit-button:hover {
  background-color: #2980b9;
}

.actions .delete-button {
  background-color: #e74c3c;
}

.actions .delete-button:hover {
  background-color: #c0392b;
}
</style>
