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
      <div class="profile-section">
        <div class="profile-header">
          <div class="profile-image-wrapper">
            <img
              v-if="profileImage"
              :src="profileImage"
              alt="프로필 이미지"
              class="profile-image"
            />
            <div v-else class="profile-image-placeholder">
              <i class="fas fa-user"></i>
            </div>
            <button @click="toggleEditMode" class="edit-profile-btn">
              <i class="fas fa-camera"></i>
            </button>
          </div>

          <div class="profile-info">
            <div v-if="!isEditMode">
              <h1>{{ currentUser.nickname || currentUser.username }}</h1>
              <p class="username">@{{ currentUser.username }}</p>
              <div class="profile-actions">
                <button @click="toggleEditMode" class="btn-edit">
                  <i class="fas fa-edit"></i> 프로필 수정
                </button>
                <button @click="showEditAccountModal" class="btn-edit-account">
                  <i class="fas fa-user-edit"></i> 회원정보 수정
                </button>
              </div>
            </div>

            <div v-else class="edit-form">
              <input
                v-model="editForm.nickname"
                type="text"
                placeholder="닉네임"
                class="input-nickname"
              />
              <div class="image-upload">
                <input
                  type="file"
                  ref="imageInput"
                  @change="handleImageChange"
                  accept="image/*"
                  class="file-input"
                />
                <button @click="$refs.imageInput.click()" class="btn-upload">
                  <i class="fas fa-upload"></i> 이미지 선택
                </button>
              </div>
              <div class="edit-actions">
                <button @click="saveProfile" class="btn-save">
                  <i class="fas fa-check"></i> 저장
                </button>
                <button @click="cancelEdit" class="btn-cancel">
                  <i class="fas fa-times"></i> 취소
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="stats">
          <div class="stat-item">
            <i class="fas fa-comment"></i>
            <span class="stat-value">{{ myArticles.length }}</span>
            <span class="stat-label">작성한 리뷰</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-star"></i>
            <span class="stat-value">{{ averageRating }}</span>
            <span class="stat-label">평균 별점</span>
          </div>
        </div>
      </div>

      <!-- 찜한 공연 -->
      <div class="wishlist-section">
        <div class="wishlist-header">
          <h2>찜한 공연</h2>
          <span class="wishlist-count">{{ wishlistItems.length }}</span>
        </div>

        <div v-if="wishlistErrorMessage" class="wishlist-alert">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ wishlistErrorMessage }}</span>
        </div>

        <div v-if="wishlistLoading" class="wishlist-loading">
          <div class="wishlist-skeleton">
            <div v-for="n in 4" :key="n" class="skeleton-card"></div>
          </div>
          <p>불러오는 중...</p>
        </div>

        <div v-else-if="wishlistItems.length === 0" class="wishlist-empty">
          <i class="fas fa-heart-broken"></i>
          <p>아직 찜한 공연이 없어요</p>
          <button class="wishlist-browse-btn" @click="goToPerformances">
            공연 둘러보기
          </button>
        </div>

        <div v-else class="wishlist-grid">
          <PerformanceCard
            v-for="item in wishlistItems"
            :key="item.mt20id || item.id"
            :performance="item"
            :like-loading="wishlistLoading"
            @click="goToPerformance"
            @toggle-like="handleWishlistToggle"
          />
        </div>
      </div>

      <!-- 관람한 공연 -->
      <div class="watched-section">
        <div class="watched-header">
          <h2>관람한 공연</h2>
          <span class="watched-count">{{ watchedItems.length }}</span>
        </div>

        <div v-if="watchedErrorMessage" class="watched-alert">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ watchedErrorMessage }}</span>
        </div>

        <div v-if="watchedLoading" class="watched-loading">
          <div class="watched-skeleton">
            <div v-for="n in 4" :key="n" class="skeleton-card"></div>
          </div>
          <p>불러오는 중...</p>
        </div>

        <div v-else-if="watchedItems.length === 0" class="watched-empty">
          <i class="fas fa-check-circle"></i>
          <p>아직 관람한 공연이 없어요</p>
          <p class="watched-empty-hint">공연 상세에서 '봤어요'를 눌러 기록해보세요</p>
          <button class="watched-browse-btn" @click="goToPerformances">
            공연 둘러보기
          </button>
        </div>

        <div v-else class="watched-grid">
          <PerformanceCard
            v-for="item in watchedItems"
            :key="item.mt20id || item.id"
            :performance="item"
            @click="goToPerformance"
          >
            <template #actions>
              <button @click.stop="handleWatchedRemove(item.mt20id || item.id)"
                      class="remove-watched-btn"
                      title="관람 해제">
                <i class="fas fa-times"></i>
              </button>
            </template>
          </PerformanceCard>
        </div>
      </div>

      <!-- 탭 메뉴 -->
      <div class="tabs">
        <button
          :class="['tab', { active: activeTab === 'articles' }]"
          @click="activeTab = 'articles'"
        >
          <i class="fas fa-comment-dots"></i> 내가 쓴 리뷰 ({{ myArticles.length }})
        </button>
        <button
          :class="['tab', { active: activeTab === 'comments' }]"
          @click="activeTab = 'comments'"
        >
          <i class="fas fa-comments"></i> 내가 쓴 댓글 ({{ myComments.length }})
        </button>
      </div>

      <!-- 탭 컨텐츠 -->
      <div class="tab-content">
        <!-- 내가 쓴 리뷰 -->
        <div v-if="activeTab === 'articles'" class="articles-list">
          <div v-if="myArticles.length === 0" class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>작성한 리뷰가 없습니다</p>
          </div>
          <div
            v-for="article in myArticles"
            :key="article.id"
            class="article-card"
            @click="goToPerformance(article.performance)"
          >
            <div class="article-header">
              <h3>{{ article.title }}</h3>
              <div v-if="article.rank" class="rating">
                <i
                  v-for="n in 5"
                  :key="n"
                  :class="['fas fa-star', { filled: n <= article.rank }]"
                ></i>
              </div>
            </div>
            <p class="article-content">{{ truncate(article.content, 100) }}</p>
            <div class="article-meta">
              <span class="performance-name">
                <i class="fas fa-ticket-alt"></i> {{ article.performance_name }}
              </span>
              <span class="date">{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- 내가 쓴 댓글 -->
        <div v-else class="comments-list">
          <div v-if="myComments.length === 0" class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>작성한 댓글이 없습니다</p>
          </div>
          <div
            v-for="comment in myComments"
            :key="comment.id"
            class="comment-card"
            @click="goToArticle(comment.article)"
          >
            <p class="comment-content">{{ comment.content }}</p>
            <div class="comment-meta">
              <span class="article-title">
                <i class="fas fa-file-alt"></i> {{ getArticleTitle(comment.article) }}
              </span>
              <span class="date">{{ formatDate(comment.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 비밀번호 확인 모달 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>비밀번호 확인</h2>
          <button @click="closePasswordModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>회원정보를 수정하려면 비밀번호를 입력해주세요.</p>
          <input
            v-model="passwordVerify"
            type="password"
            placeholder="비밀번호"
            class="password-input"
            @keyup.enter="verifyPassword"
          />
          <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
        </div>
        <div class="modal-footer">
          <button @click="verifyPassword" class="btn-confirm" :disabled="verifyLoading">
            <i v-if="verifyLoading" class="fas fa-spinner fa-spin"></i>
            <span v-else>확인</span>
          </button>
          <button @click="closePasswordModal" class="btn-cancel-modal">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useWatchedStore } from '@/stores/watchedStore'
import PerformanceCard from '@/components/Performance/PerformanceCard.vue'

import authAPI from '@/api/auth'
import communityAPI from '@/api/community'
import wishlistAPI from '@/api/wishlist'
import watchedAPI from '@/api/watched'

const router = useRouter()
const authStore = useAuthStore()
const wishlistStore = useWishlistStore()
const watchedStore = useWatchedStore()
const { items: wishlistItems, loading: wishlistLoading, errorMessage: wishlistErrorMessage } = storeToRefs(wishlistStore)
const { items: watchedItems, loading: watchedLoading, errorMessage: watchedErrorMessage } = storeToRefs(watchedStore)

const loading = ref(true)
const error = ref(null)
const isEditMode = ref(false)
const activeTab = ref('articles')

const currentUser = ref({})
const myArticles = ref([])
const myComments = ref([])
const articles = ref([])

const profileImage = ref(null)
const editForm = ref({
  nickname: '',
  profileImage: null,
})
const imageInput = ref(null)

// 비밀번호 확인 모달 관련
const showPasswordModal = ref(false)
const passwordVerify = ref('')
const passwordError = ref('')
const verifyLoading = ref(false)

const initWishlist = async () => {
  try {
    await wishlistStore.fetchWishlist()
  } catch (err) {
    // Error message is handled in store
  }
}

const initWatched = async () => {
  try {
    await watchedStore.fetchWatched()
  } catch (err) {
    // Error message is handled in store
  }
}

// 평균 별점 계산
const averageRating = computed(() => {
  const ratedArticles = myArticles.value.filter(a => a.rank !== null)
  if (ratedArticles.length === 0) return '0.0'
  const sum = ratedArticles.reduce((acc, a) => acc + a.rank, 0)
  return (sum / ratedArticles.length).toFixed(1)
})

// 데이터 로드
const loadData = async () => {
  try {
    loading.value = true
    error.value = null

    // 현재 사용자 정보
    const userRes = await apiClient.get('/accounts/users/me/')
    currentUser.value = userRes.data

    // 내가 쓴 게시글
    const articlesRes = await apiClient.get('/community/articles/')
    const allArticles = articlesRes.data.results || articlesRes.data
    myArticles.value = allArticles.filter(a => a.user === currentUser.value.id)

    // 내가 쓴 댓글
    const commentsRes = await apiClient.get('/community/comments/')
    const allComments = commentsRes.data.results || commentsRes.data
    myComments.value = allComments.filter(c => c.user === currentUser.value.id)

    // 전체 게시글 목록 (댓글의 게시글 제목 찾기용)
    articles.value = allArticles

    // 프로필 이미지 설정
    if (currentUser.value.profile_image) {
      profileImage.value = currentUser.value.profile_image
    }

    editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
  } catch (err) {
    console.error('데이터 로드 실패:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 프로필 편집 토글
const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  if (isEditMode.value) {
    editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
  }
}

// 이미지 변경 핸들러
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    editForm.value.profileImage = file
    // 미리보기
    const reader = new FileReader()
    reader.onload = (e) => {
      profileImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 프로필 저장
const saveProfile = async () => {
  try {
    const formData = new FormData()
    if (editForm.value.nickname) {
      formData.append('nickname', editForm.value.nickname)
    }
    if (editForm.value.profileImage) {
      formData.append('profile_image', editForm.value.profileImage)
    }

    // TODO: 백엔드 API 호출 (현재는 로컬 상태만 업데이트)
    // await apiClient.patch(`/users/${currentUser.value.id}/`, formData)

    // 로컬 상태 업데이트
    currentUser.value.nickname = editForm.value.nickname

    isEditMode.value = false
    alert('프로필이 업데이트되었습니다!')
  } catch (err) {
    console.error('프로필 저장 실패:', err)
    alert('프로필 저장에 실패했습니다.')
  }
}

// 편집 취소
const cancelEdit = () => {
  isEditMode.value = false
  editForm.value.nickname = currentUser.value.nickname || currentUser.value.username
  profileImage.value = currentUser.value.profile_image || null
}

// 공연 상세 페이지로 이동
const goToPerformance = (performanceId) => {
  router.push({ name: 'performance-detail', params: { id: performanceId } })
}

// 게시글 상세 페이지로 이동 (커뮤니티)
const goToArticle = (articleId) => {
  router.push({ name: 'community', query: { articleId } })
}

const goToPerformances = () => {
  router.push({ name: 'performances' })
}

const handleWishlistToggle = async (performanceId) => {
  try {
    await wishlistStore.removeFromWishlist(performanceId)
  } catch (err) {
    // Error message is handled in store
  }
}

const handleWatchedRemove = async (performanceId) => {
  try {
    await watchedStore.removeFromWatched(performanceId)
  } catch (err) {
    // Error message is handled in store
  }
}

// 게시글 제목 찾기
const getArticleTitle = (articleId) => {
  const article = articles.value.find(a => a.id === articleId)
  return article ? article.title : '알 수 없음'
}

// 텍스트 자르기
const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// 날짜 포맷
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR')
}

// 비밀번호 확인 모달 열기
const showEditAccountModal = () => {
  showPasswordModal.value = true
  passwordVerify.value = ''
  passwordError.value = ''
}

// 비밀번호 확인 모달 닫기
const closePasswordModal = () => {
  showPasswordModal.value = false
  passwordVerify.value = ''
  passwordError.value = ''
}

// 비밀번호 검증
const verifyPassword = async () => {
  if (!passwordVerify.value) {
    passwordError.value = '비밀번호를 입력해주세요.'
    return
  }

  try {
    verifyLoading.value = true
    passwordError.value = ''

    const response = await apiClient.post('/accounts/users/verify_password/', {
      password: passwordVerify.value
    })

    if (response.data.verified) {
      closePasswordModal()
      // 회원정보 수정 페이지로 이동
      router.push({ name: 'edit-account' })
    }
  } catch (err) {
    console.error('비밀번호 확인 실패:', err)
    passwordError.value = err.response?.data?.error || '비밀번호가 일치하지 않습니다.'
  } finally {
    verifyLoading.value = false
  }
}

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

/* 프로필 섹션 */
.profile-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

:root.dark .profile-section {
  background: #1f2937;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.profile-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.profile-image-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
}

.profile-image,
.profile-image-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-image-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
}

.edit-profile-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  border: 3px solid white;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-profile-btn:hover {
  background: #4f46e5;
  transform: scale(1.1);
}

.profile-info {
  flex: 1;
}

.profile-info h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #1f2937;
  transition: color 0.3s;
}

:root.dark .profile-info h1 {
  color: #f3f4f6;
}

.username {
  color: #6b7280;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .username {
  color: #9ca3af;
}

.btn-edit {
  padding: 0.5rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit:hover {
  background: #4f46e5;
}

:root.dark .btn-edit {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

:root.dark .btn-edit:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
}

/* 편집 폼 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-nickname {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .input-nickname {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.input-nickname:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .input-nickname:focus {
  border-color: #818cf8;
  background: #4b5563;
}

.image-upload {
  display: flex;
  gap: 1rem;
}

.file-input {
  display: none;
}

.btn-upload {
  padding: 0.5rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-upload:hover {
  background: #059669;
}

.edit-actions {
  display: flex;
  gap: 1rem;
}

.btn-save,
.btn-cancel {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save {
  background: #10b981;
  color: white;
}

.btn-save:hover {
  background: #059669;
}

.btn-cancel {
  background: #ef4444;
  color: white;
}

.btn-cancel:hover {
  background: #dc2626;
}

/* 통계 */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  transition: background-color 0.3s;
}

:root.dark .stat-item {
  background: #111827;
}

.stat-item i {
  font-size: 2rem;
  color: #6366f1;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

:root.dark .stat-item i {
  color: #818cf8;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.25rem;
  transition: color 0.3s;
}

:root.dark .stat-value {
  color: #f3f4f6;
}

.stat-label {
  color: #6b7280;
  font-size: 0.9rem;
  transition: color 0.3s;
}

:root.dark .stat-label {
  color: #9ca3af;
}

/* 찜한 공연 */
.wishlist-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
  transition: background-color 0.3s, border-color 0.3s, box-shadow 0.3s;
}

:root.dark .wishlist-section {
  background: #1f2937;
  border-color: #374151;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.wishlist-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.wishlist-header h2 {
  font-size: 1.5rem;
  color: #0f172a;
  transition: color 0.3s;
}

:root.dark .wishlist-header h2 {
  color: #f3f4f6;
}

.wishlist-count {
  background: #0d9488;
  color: white;
  font-weight: 700;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

:root.dark .wishlist-count {
  background: #14b8a6;
}

.wishlist-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #0d9488;
  color: #0f172a;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}

:root.dark .wishlist-alert {
  background: #111827;
  border-color: #374151;
  border-left-color: #14b8a6;
  color: #f3f4f6;
}

.wishlist-loading {
  text-align: center;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .wishlist-loading {
  color: #9ca3af;
}

.wishlist-skeleton {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.skeleton-card {
  aspect-ratio: 3/4;
  background: linear-gradient(120deg, #e2e8f0 30%, #f1f5f9 50%, #e2e8f0 70%);
  background-size: 200% 100%;
  animation: shimmer 1.4s ease infinite;
  border-radius: 0.75rem;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.wishlist-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .wishlist-empty {
  color: #9ca3af;
}

.wishlist-empty i {
  font-size: 2.5rem;
  color: #94a3b8;
  margin-bottom: 0.75rem;
  transition: color 0.3s;
}

:root.dark .wishlist-empty i {
  color: #6b7280;
}

.wishlist-browse-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  border-radius: 9999px;
  border: none;
  background: #14b8a6;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.wishlist-browse-btn:hover {
  background: #0d9488;
  transform: translateY(-1px);
}

.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.25rem;
}

/* 관람한 공연 */
.watched-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
  transition: background-color 0.3s, border-color 0.3s, box-shadow 0.3s;
}

:root.dark .watched-section {
  background: #1f2937;
  border-color: #374151;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.watched-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.watched-header h2 {
  font-size: 1.5rem;
  color: #0f172a;
  transition: color 0.3s;
}

:root.dark .watched-header h2 {
  color: #f3f4f6;
}

.watched-count {
  background: #6366f1;
  color: white;
  font-weight: 700;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

:root.dark .watched-count {
  background: #818cf8;
}

.watched-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #6366f1;
  color: #0f172a;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}

:root.dark .watched-alert {
  background: #111827;
  border-color: #374151;
  border-left-color: #818cf8;
  color: #f3f4f6;
}

.watched-loading {
  text-align: center;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .watched-loading {
  color: #9ca3af;
}

.watched-skeleton {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.watched-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .watched-empty {
  color: #9ca3af;
}

.watched-empty i {
  font-size: 2.5rem;
  color: #6366f1;
  margin-bottom: 0.75rem;
  transition: color 0.3s;
}

:root.dark .watched-empty i {
  color: #818cf8;
}

.watched-empty-hint {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

:root.dark .watched-empty-hint {
  color: #6b7280;
}

.watched-browse-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  border-radius: 9999px;
  border: none;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.watched-browse-btn:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  transform: translateY(-1px);
}

.watched-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.25rem;
}

.remove-watched-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s;
  z-index: 10;
}

.watched-grid :deep(.performance-card):hover .remove-watched-btn {
  opacity: 1;
}

.remove-watched-btn:hover {
  background: rgba(220, 38, 38, 1);
  transform: scale(1.1);
}

/* 탭 */
.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .tabs {
  border-bottom-color: #374151;
}

.tab {
  padding: 1rem 2rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
  color: #6b7280;
  font-size: 1rem;
  font-weight: 500;
}

:root.dark .tab {
  color: #9ca3af;
}

.tab:hover {
  color: #6366f1;
}

:root.dark .tab:hover {
  color: #818cf8;
}

.tab.active {
  color: #6366f1;
  border-bottom-color: #6366f1;
}

:root.dark .tab.active {
  color: #818cf8;
  border-bottom-color: #818cf8;
}

/* 리스트 */
.articles-list,
.comments-list {
  display: grid;
  gap: 1rem;
}

.article-card,
.comment-card {
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

:root.dark .article-card,
:root.dark .comment-card {
  background: #1f2937;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.article-card:hover,
.comment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

:root.dark .article-card:hover,
:root.dark .comment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.article-header h3 {
  font-size: 1.25rem;
  color: #1f2937;
  transition: color 0.3s;
}

:root.dark .article-header h3 {
  color: #f3f4f6;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.rating i {
  color: #d1d5db;
  font-size: 1rem;
}

.rating i.filled {
  color: #fbbf24;
}

.article-content,
.comment-content {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .article-content,
:root.dark .comment-content {
  color: #d1d5db;
}

.article-meta,
.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .article-meta,
:root.dark .comment-meta {
  color: #9ca3af;
}

.performance-name,
.article-title {
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .empty-state {
  color: #6b7280;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

/* 프로필 액션 버튼 */
.profile-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-edit-account {
  padding: 0.5rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit-account:hover {
  background: #059669;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
  transition: background-color 0.3s;
}

:root.dark .modal-content {
  background: #1f2937;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .modal-header {
  border-bottom-color: #374151;
}

.modal-header h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0;
  transition: color 0.3s;
}

:root.dark .modal-header h2 {
  color: #f3f4f6;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

:root.dark .modal-close {
  color: #9ca3af;
}

:root.dark .modal-close:hover {
  background: #374151;
  color: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin-bottom: 1rem;
  color: #4b5563;
  transition: color 0.3s;
}

:root.dark .modal-body p {
  color: #d1d5db;
}

.password-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1f2937;
}

:root.dark .password-input {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.password-input:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .password-input:focus {
  border-color: #818cf8;
  background: #4b5563;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.modal-footer {
  display: flex;
  gap: 0.5rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  justify-content: flex-end;
  transition: border-color 0.3s;
}

:root.dark .modal-footer {
  border-top-color: #374151;
}

.btn-confirm {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  min-width: 80px;
}

.btn-confirm:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel-modal {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #1f2937;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-cancel-modal:hover {
  background: #e5e7eb;
}

:root.dark .btn-cancel-modal {
  background: #374151;
  color: #f3f4f6;
}

:root.dark .btn-cancel-modal:hover {
  background: #4b5563;
}

/* 반응형 */
@media (max-width: 1024px) {
  .wishlist-skeleton,
  .wishlist-grid,
  .watched-skeleton,
  .watched-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .mypage-container {
    padding: 1rem;
  }

  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .tabs {
    overflow-x: auto;
  }

  .tab {
    white-space: nowrap;
  }

  .wishlist-skeleton,
  .wishlist-grid,
  .watched-skeleton,
  .watched-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style>
