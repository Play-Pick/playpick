<template>
  <div class="mypage-container">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <div v-else class="mypage-content">
      <!-- 프로필 섹션 -->
      <ProfileSection
        :user="currentUser"
        :profile-image="profileImage"
        :is-edit-mode="isEditMode"
        :edit-form="editForm"
        :articles-count="myArticles.length"
        :average-rating="averageRating"
        @toggle-edit="toggleEditMode"
        @show-edit-account="showEditAccountModal"
        @update:editForm="editForm = $event"
        @save="saveProfile"
        @cancel-edit="cancelEdit"
        @image-change="handleImageChange"
      />

      <!-- 찜한 공연 -->
      <WishlistSection
        :items="wishlistItems"
        :loading="wishlistLoading"
        :error-message="wishlistErrorMessage"
        @browse="goToPerformances"
        @click-performance="goToPerformance"
        @toggle-like="handleWishlistToggle"
      />

      <!-- 관람한 공연 -->
      <WatchedSection
        :items="watchedItems"
        :loading="watchedLoading"
        :error-message="watchedErrorMessage"
        @browse="goToPerformances"
        @click-performance="goToPerformance"
        @remove="handleWatchedRemove"
      />

      <!-- 게시글 / 댓글 탭 -->
      <ArticlesCommentsTab
        v-model:active-tab="activeTab"
        :articles="myArticles"
        :comments="myComments"
        :all-articles="articles"
        @article-click="goToPerformance"
        @comment-click="goToArticle"
      />
    </div>

    <!-- 비밀번호 확인 모달 -->
    <PasswordVerifyModal
      :show="showPasswordModal"
      v-model:password="passwordVerify"
      :loading="verifyLoading"
      :error="passwordError"
      @close="closePasswordModal"
      @verify="verifyPassword"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useWatchedStore } from '@/stores/watchedStore'
import { useMyPage } from '@/composables/useMyPage'
import ProfileSection from '@/components/User/ProfileSection.vue'
import WishlistSection from '@/components/User/WishlistSection.vue'
import WatchedSection from '@/components/User/WatchedSection.vue'
import ArticlesCommentsTab from '@/components/User/ArticlesCommentsTab.vue'
import PasswordVerifyModal from '@/components/User/PasswordVerifyModal.vue'

const wishlistStore = useWishlistStore()
const watchedStore = useWatchedStore()
const { items: wishlistItems, loading: wishlistLoading, errorMessage: wishlistErrorMessage } = storeToRefs(wishlistStore)
const { items: watchedItems, loading: watchedLoading, errorMessage: watchedErrorMessage } = storeToRefs(watchedStore)

// useMyPage composable 사용
const {
  loading,
  error,
  isEditMode,
  activeTab,
  currentUser,
  myArticles,
  myComments,
  articles,
  profileImage,
  editForm,
  showPasswordModal,
  passwordVerify,
  passwordError,
  verifyLoading,
  averageRating,
  loadData,
  initWishlist,
  initWatched,
  toggleEditMode,
  handleImageChange,
  saveProfile,
  cancelEdit,
  showEditAccountModal,
  closePasswordModal,
  verifyPassword,
  goToPerformance,
  goToArticle,
  goToPerformances,
  handleWishlistToggle,
  handleWatchedRemove
} = useMyPage()

onMounted(() => {
  loadData()
  initWishlist()
  initWatched()
})
</script>

<style scoped>
.mypage-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  transition: background 0.3s;
}

:root.dark .mypage-container {
  background: linear-gradient(to bottom, #111827, #1f2937);
}

/* 로딩 & 에러 */
.loading,
.error {
  text-align: center;
  padding: 5rem 2rem;
  color: #1f2937;
  transition: color 0.3s;
}

:root.dark .loading,
:root.dark .error {
  color: #f3f4f6;
}

.loading .spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

:root.dark .loading .spinner {
  border-color: #374151;
  border-top-color: #818cf8;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .mypage-container {
    padding: 1rem;
  }
}
</style>
