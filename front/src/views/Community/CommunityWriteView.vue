<template>
  <div class="community-write-container">
    <div class="write-content">
      <!-- 헤더 -->
      <div class="page-header">
        <button @click="goBack" class="back-button">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1 class="page-title">
          <i :class="categoryIcon"></i>
          {{ categoryLabel }} 작성
        </h1>
      </div>

      <!-- 로그인 필요 -->
      <div v-if="!isAuthenticated" class="login-required">
        <i class="fas fa-lock"></i>
        <p>글을 작성하려면 로그인이 필요합니다</p>
        <button @click="goToLogin" class="btn-login">
          <i class="fas fa-sign-in-alt"></i> 로그인
        </button>
      </div>

      <!-- 작성 폼 -->
      <form v-else @submit.prevent="submitArticle" class="write-form">
        <!-- 공연 선택 (선택사항) -->
        <div class="form-group">
          <label>공연 선택 (선택사항)</label>
          <PerformanceSelectCard
            :performance="performance"
            @clear="clearPerformance"
          />
        </div>

        <!-- 카테고리 표시 -->
        <CategoryDisplay
          label="카테고리"
          :icon="categoryIcon"
          :text="categoryLabel"
        />

        <!-- 제목, 별점, 내용 -->
        <ArticleFormFields
          v-model:title="form.title"
          v-model:content="form.content"
          v-model:rating="form.rank"
          :show-rating="needsRating(category)"
          :rows="12"
        />

        <!-- 버튼 -->
        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitting">
            <i class="fas fa-paper-plane"></i>
            {{ submitting ? '작성 중...' : '작성 완료' }}
          </button>
          <button type="button" @click="goBack" class="btn-cancel">
            <i class="fas fa-times"></i> 취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useArticleForm } from '@/composables/community/useArticleForm'
import communityAPI from '@/api/community'
import performanceAPI from '@/api/performances'
import PerformanceSelectCard from '@/components/Community/PerformanceSelectCard.vue'
import CategoryDisplay from '@/components/Community/CategoryDisplay.vue'
import ArticleFormFields from '@/components/Community/ArticleFormFields.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// useArticleForm composable 사용
const {
  submitting,
  getCategoryIcon,
  getCategoryLabel,
  needsRating,
  goBack,
  goToLogin
} = useArticleForm()

const isAuthenticated = computed(() => authStore.isAuthenticated)

// URL 파라미터에서 카테고리와 공연ID 가져오기
const category = ref(route.query.category || 'REVIEW')
const performanceId = ref(route.query.performanceId || null)
const performance = ref(null)

const form = ref({
  title: '',
  content: '',
  rank: 5,
})

// 카테고리별 아이콘과 라벨
const categoryIcon = computed(() => getCategoryIcon(category.value))
const categoryLabel = computed(() => getCategoryLabel(category.value))

// 공연 정보 불러오기
const loadPerformance = async () => {
  if (!performanceId.value) return

  try {
    const response = await performanceAPI.getPerformance(performanceId.value)
    performance.value = response.data
  } catch (error) {
    console.error('공연 정보 로드 실패:', error)
  }
}

// 공연 선택 해제
const clearPerformance = () => {
  performance.value = null
  performanceId.value = null
}

// 글 작성 제출
const submitArticle = async () => {
  try {
    submitting.value = true

    const articleData = {
      category: category.value,
      title: form.value.title,
      content: form.value.content,
    }

    // 공연이 선택된 경우 포함
    if (performanceId.value) {
      articleData.performance = performanceId.value
    }

    // 별점은 관람후기일 때만 포함
    if (needsRating(category.value)) {
      articleData.rank = form.value.rank
    } else if (category.value === 'EXPECTATION') {
      articleData.rank = 2.5
    }

    await communityAPI.createArticle(articleData)

    alert('글이 작성되었습니다!')

    // 공연 상세 페이지에서 왔으면 돌아가기, 아니면 커뮤니티로
    if (performanceId.value) {
      // refresh 쿼리로 리뷰 새로고침 트리거
      router.push({
        name: 'performance-detail',
        params: { id: performanceId.value },
        query: { refresh: Date.now() }
      })
    } else {
      router.push({ name: 'community' })
    }
  } catch (error) {
    console.error('글 작성 실패:', error)
    alert('글 작성에 실패했습니다.')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadPerformance()
})
</script>

<style scoped>
.community-write-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem 1rem;
  transition: background 0.3s;
}

:root.dark .community-write-container {
  background: linear-gradient(to bottom, #1a1a1a, #0f0f0f);
}

.write-content {
  max-width: 900px;
  margin: 0 auto;
}

/* 헤더 */
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: none;
  background: white;
  color: #6366f1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

:root.dark .back-button {
  background: #2c2c2c;
  color: #818cf8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.back-button:hover {
  background: #6366f1;
  color: white;
  transform: scale(1.05);
}

:root.dark .back-button:hover {
  background: #818cf8;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: color 0.3s;
}

:root.dark .page-title {
  color: #f3f4f6;
}

.page-title i {
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .page-title i {
  color: #818cf8;
}

/* 로그인 필요 */
.login-required {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .login-required {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.login-required i {
  font-size: 4rem;
  color: #9ca3af;
  margin-bottom: 1.5rem;
  display: block;
  transition: color 0.3s;
}

:root.dark .login-required i {
  color: #6b7280;
}

.login-required p {
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 2rem;
  transition: color 0.3s;
}

:root.dark .login-required p {
  color: #9ca3af;
}

.btn-login {
  padding: 0.875rem 2.5rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 1.0625rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .btn-login {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-login:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  transform: scale(1.05);
}

:root.dark .btn-login:hover {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

/* 작성 폼 */
.write-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .write-form {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-weight: 700;
  font-size: 1.0625rem;
  color: #374151;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #d1d5db;
}

/* 버튼 */
.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
}

.btn-submit,
.btn-cancel {
  padding: 0.875rem 2.5rem;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 1.0625rem;
  font-weight: 700;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  flex: 1;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

:root.dark .btn-submit {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  transform: scale(1.02);
}

:root.dark .btn-submit:hover:not(:disabled) {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #e5e7eb;
  color: #374151;
}

:root.dark .btn-cancel {
  background: #374151;
  color: #f3f4f6;
}

.btn-cancel:hover {
  background: #d1d5db;
}

:root.dark .btn-cancel:hover {
  background: #4b5563;
}

/* 반응형 */
@media (max-width: 768px) {
  .community-write-container {
    padding: 1rem 0.5rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .write-form {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-submit,
  .btn-cancel {
    width: 100%;
  }
}
</style>
