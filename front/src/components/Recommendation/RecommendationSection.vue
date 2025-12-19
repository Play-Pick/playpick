<template>
  <div class="recommendation-section">
    <!-- 헤더 -->
    <div class="section-header">
      <h2>
        <i class="fas fa-magic"></i>
        {{ isAuthenticated ? `${username}님을 위한` : '당신을 위한' }} 추천 공연
      </h2>
      <p class="subtitle">
        {{ isAuthenticated
          ? '당신의 취향을 기반으로 엄선했어요'
          : '로그인하고 맞춤 추천을 받아보세요'
        }}
      </p>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>추천 공연을 찾고 있어요...</p>
    </div>

    <!-- 추천 없음 (빈 상태) - 로그인 상태에서만 표시 -->
    <div v-else-if="!hasRecommendationsToShow" class="empty-state">
      <i class="fas fa-compass"></i>
      <h3>아직 추천할 공연이 없어요</h3>
      <p>공연을 관람하고 좋아요를 누르면<br>맞춤 추천을 받을 수 있어요!</p>
      <router-link to="/performances" class="browse-button">
        <i class="fas fa-search"></i>
        공연 둘러보기
      </router-link>
    </div>

    <!-- 추천 캐러셀 -->
    <div v-else class="recommendation-carousel">
      <!-- 블러 래퍼 -->
      <div :class="['blur-wrapper', { blurred: shouldShowBlur }]">
        <div class="carousel-wrapper">
          <!-- 좌측 화살표 -->
          <button
            v-if="canGoPrev"
            @click="goToPrevPage"
            class="nav-arrow nav-arrow-left"
            aria-label="이전 공연 보기"
          >
            <i class="fas fa-chevron-left"></i>
          </button>

          <!-- 추천 목록 -->
          <div class="recommendations-scroll">
            <RecommendationCard
              v-for="rec in displayedRecommendations"
              :key="rec.mt20id"
              :performance="rec"
              :reason="rec.reason_text || rec.reason"
              :like-loading="likeLoading"
              @toggle-like="handleToggleLike"
            />
          </div>

          <!-- 우측 화살표 -->
          <button
            v-if="canGoNext"
            @click="goToNextPage"
            class="nav-arrow nav-arrow-right"
            aria-label="다음 공연 보기"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>

        <!-- 더보기 버튼 -->
        <div class="view-more-container">
          <router-link to="/recommendations" class="view-more-button">
            <span>추천 공연 더보기</span>
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 로그인 프롬프트 오버레이 (recommendation-section 전체를 덮음) -->
    <transition name="fade">
      <div v-if="shouldShowBlur" class="login-prompt-overlay" role="dialog" aria-modal="true" aria-labelledby="prompt-title">
        <div class="login-prompt-content">
          <!-- 아이콘 영역 -->
          <div class="prompt-icon">
            <i class="fas fa-sparkles sparkle-1"></i>
            <i class="fas fa-lock lock-icon"></i>
            <i class="fas fa-sparkles sparkle-2"></i>
          </div>

          <!-- 메인 메시지 -->
          <h3 id="prompt-title" class="prompt-title">추천 공연을 확인하세요!</h3>

          <!-- 서브 메시지 -->
          <p class="prompt-description">
            로그인 후 맞춤 추천을 받아보세요
          </p>

          <!-- 액션 버튼 -->
          <div class="prompt-actions">
            <button @click="goToLogin" class="prompt-btn primary">
              <i class="fas fa-sign-in-alt"></i>
              로그인하기
            </button>
            <button @click="goToRegister" class="prompt-btn secondary">
              회원가입
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useRecommendationStore } from '@/stores/recommendationStore'
import { useAuthStore } from '@/stores/authStore'
import { useUserTracking } from '@/composables/useUserTracking'
import RecommendationCard from './RecommendationCard.vue'

const router = useRouter()

const recommendationStore = useRecommendationStore()
const authStore = useAuthStore()
const { toggleLike, likeLoading } = useUserTracking()

const { recommendations, loading, hasRecommendations } = storeToRefs(recommendationStore)
const { username, isAuthenticated } = storeToRefs(authStore)

// 플레이스홀더 데이터 (비로그인 사용자용)
const placeholderRecommendations = [
  {
    mt20id: 'placeholder-1',
    prfnm: '당신을 위한 특별한 공연',
    poster: 'https://via.placeholder.com/300x400?text=추천공연',
    fcltynm: '맞춤 추천 장소',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    genrenm: '추천',
    reason_text: '맞춤 추천'
  },
  {
    mt20id: 'placeholder-2',
    prfnm: '당신을 위한 특별한 공연',
    poster: 'https://via.placeholder.com/300x400?text=추천공연',
    fcltynm: '맞춤 추천 장소',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    genrenm: '추천',
    reason_text: '맞춤 추천'
  },
  {
    mt20id: 'placeholder-3',
    prfnm: '당신을 위한 특별한 공연',
    poster: 'https://via.placeholder.com/300x400?text=추천공연',
    fcltynm: '맞춤 추천 장소',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    genrenm: '추천',
    reason_text: '맞춤 추천'
  },
  {
    mt20id: 'placeholder-4',
    prfnm: '당신을 위한 특별한 공연',
    poster: 'https://via.placeholder.com/300x400?text=추천공연',
    fcltynm: '맞춤 추천 장소',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    genrenm: '추천',
    reason_text: '맞춤 추천'
  },
  {
    mt20id: 'placeholder-5',
    prfnm: '당신을 위한 특별한 공연',
    poster: 'https://via.placeholder.com/300x400?text=추천공연',
    fcltynm: '맞춤 추천 장소',
    prfpdfrom: '2024-01-01',
    prfpdto: '2024-12-31',
    genrenm: '추천',
    reason_text: '맞춤 추천'
  }
]

// 페이지네이션 상태
const currentPage = ref(0)
const itemsPerPage = 5

// 로그인 상태에 따라 다른 데이터 표시
const displayRecommendations = computed(() => {
  if (authStore.isAuthenticated) {
    return recommendations.value
  }
  return placeholderRecommendations
})

// 블러 표시 여부
const shouldShowBlur = computed(() => !authStore.isAuthenticated)

// 표시할 추천이 있는지 확인 (비로그인 시 플레이스홀더 포함)
const hasRecommendationsToShow = computed(() => {
  if (!authStore.isAuthenticated) {
    return true // 비로그인 시 플레이스홀더 항상 표시
  }
  return hasRecommendations.value
})

// 현재 페이지에 표시할 추천
const displayedRecommendations = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return displayRecommendations.value.slice(start, end)
})

// 전체 페이지 수
const totalPages = computed(() => Math.ceil(displayRecommendations.value.length / itemsPerPage))

// 화살표 표시 여부
const canGoPrev = computed(() => currentPage.value > 0)
const canGoNext = computed(() => currentPage.value < totalPages.value - 1)

// 페이지 이동
const goToPrevPage = () => {
  if (canGoPrev.value) {
    currentPage.value--
  }
}

const goToNextPage = () => {
  if (canGoNext.value) {
    currentPage.value++
  }
}

const handleToggleLike = async (performanceId) => {
  try {
    const result = await toggleLike(performanceId)

    // Update local recommendation data
    const rec = recommendations.value.find(r => r.mt20id === performanceId)
    if (rec) {
      rec.is_liked = result.is_liked
      rec.like_count = result.like_count
    }
  } catch (err) {
    if (err.message === '로그인이 필요합니다.') {
      // Silently ignore or show subtle notification
      console.log('Like requires authentication')
    } else {
      console.error('찜하기 실패:', err)
    }
  }
}

// 로그인/회원가입 네비게이션
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

onMounted(async () => {
  // 인증된 사용자만 추천 조회
  if (authStore.isAuthenticated) {
    await recommendationStore.fetchRecommendations()
  }
})
</script>

<style scoped>
.recommendation-section {
  padding: 4rem 0;
  max-width: 1280px;
  margin: 0 auto;
}

/* 섹션 헤더 */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--card-text-primary);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.section-header h2 i {
  color: var(--card-accent);
}

.subtitle {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
}

/* 로딩 상태 */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  display: inline-block;
  width: 3rem;
  height: 3rem;
  border: 3px solid #e5e7eb;
  border-top-color: var(--card-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-container p {
  color: var(--card-text-secondary);
  font-size: 1rem;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  border-radius: 1.5rem;
}

:root.dark .empty-state {
  background: linear-gradient(to bottom, #1a1a1a, #0f0f0f);
}

.empty-state i {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--card-text-primary);
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
  line-height: 1.8;
  margin-bottom: 2rem;
}

.browse-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(to right, var(--card-accent), var(--card-accent-hover));
  color: white;
  text-decoration: none;
  border-radius: 9999px;
  font-weight: 700;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
}

.browse-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(20, 184, 166, 0.4);
}

.browse-button i {
  font-size: 0.875rem;
}

/* 추천 캐러셀 */
.recommendation-carousel {
  max-width: 1280px;
  margin: 0 auto;
}

.carousel-wrapper {
  position: relative;
  padding: 0 3.5rem;
}

/* 추천 스크롤 */
.recommendations-scroll {
  display: flex;
  gap: 1.2rem;
  padding: 1rem 0;
  justify-content: space-between;
}

/* 카드 크기 조정: 5개가 딱 맞게 */
.recommendations-scroll :deep(.recommendation-card) {
  flex-shrink: 0;
  width: calc((100% - (1.2rem * 4)) / 5);
  min-width: 0;
}

/* 네비게이션 화살표 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: white;
  border: none;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

:root.dark .nav-arrow {
  background: white !important;
}

.nav-arrow:hover {
  background: #6366f1;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-50%) scale(1.1);
}

:root.dark .nav-arrow:hover {
  background: white !important;
}

.nav-arrow-left {
  left: 0;
}

.nav-arrow-right {
  right: 0;
}

.nav-arrow i {
  font-size: 1.25rem;
  color: #111827;
}

.nav-arrow:hover i {
  color: white;
}

:root.dark .nav-arrow i {
  color: #111827 !important;
}

:root.dark .nav-arrow:hover i {
  color: #111827 !important;
}

/* 더보기 버튼 */
.view-more-container {
  text-align: center;
  margin-top: 3rem;
}

.view-more-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  border-radius: 9999px;
  color: white;
  background: linear-gradient(to right, var(--card-accent), var(--card-accent-hover));
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

:root.dark .view-more-button {
  background: white !important;
  color: #111827 !important;
}

.view-more-button:hover {
  background: linear-gradient(to right, var(--card-accent-hover), #7c3aed);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

:root.dark .view-more-button:hover {
  background: white !important;
  color: #111827 !important;
}

.view-more-button i {
  transition: transform 0.3s;
}

.view-more-button:hover i {
  transform: translateX(0.5rem);
}

/* 반응형 */
@media (max-width: 1024px) {
  .carousel-wrapper {
    padding: 0 2.5rem;
  }

  .recommendations-scroll {
    gap: 1rem;
    overflow-x: auto;
  }

  .recommendations-scroll :deep(.recommendation-card) {
    width: 15rem;
  }
}

@media (max-width: 768px) {
  .recommendation-section {
    padding: 2rem 1rem;
  }

  .section-header h2 {
    font-size: 1.75rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .carousel-wrapper {
    padding: 0 2.5rem;
  }

  .nav-arrow {
    width: 2.5rem;
    height: 2.5rem;
  }

  .nav-arrow i {
    font-size: 1rem;
  }

  .recommendations-scroll {
    gap: 1rem;
  }

  .recommendations-scroll :deep(.recommendation-card) {
    width: 14rem;
  }

  .view-more-button {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }

  .empty-state {
    padding: 3rem 1.5rem;
  }

  .empty-state i {
    font-size: 3rem;
  }

  .empty-state h3 {
    font-size: 1.5rem;
  }

  .empty-state p {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .carousel-wrapper {
    padding: 0 2rem;
  }

  .nav-arrow {
    width: 2rem;
    height: 2rem;
  }

  .nav-arrow i {
    font-size: 0.875rem;
  }

  .recommendations-scroll :deep(.recommendation-card) {
    width: 12rem;
  }
}

/* ========== 추천 섹션 포지셔닝 ========== */
.recommendation-section {
  position: relative;
}

/* ========== 블러 효과 ========== */
.blur-wrapper {
  position: relative;
  transition: filter 0.6s ease;
}

.blur-wrapper.blurred {
  filter: blur(8px) grayscale(0.3);
  pointer-events: none;
  user-select: none;
}

/* 블러된 상태에서 호버 효과 방지 */
.blur-wrapper.blurred .recommendation-card:hover {
  transform: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* ========== 로그인 프롬프트 오버레이 ========== */
.login-prompt-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.85) 0%,
    rgba(0, 0, 0, 0.75) 100%
  );
  backdrop-filter: blur(16px);
  z-index: 50;
  padding: 2rem;
}

:root.dark .login-prompt-overlay {
  background: linear-gradient(
    135deg,
    rgba(10, 10, 10, 0.9) 0%,
    rgba(20, 20, 20, 0.85) 100%
  );
}

/* 콘텐츠 */
.login-prompt-content {
  text-align: center;
  max-width: 500px;
  animation: fadeInUp 0.6s ease-out;
}

/* ========== 애니메이션 ========== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

@keyframes sparkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0.5) rotate(0deg);
  }
  50% {
    opacity: 1;
    transform: scale(1) rotate(180deg);
  }
}

/* ========== 아이콘 스타일 ========== */
.prompt-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  height: 70px;
}

.lock-icon {
  font-size: 3.5rem;
  background: linear-gradient(135deg, #6366f1, #9333ea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: pulse 2s ease-in-out infinite;
}

.sparkle-1,
.sparkle-2 {
  position: absolute;
  font-size: 1.25rem;
  color: #fbbf24;
  animation: sparkle 1.5s ease-in-out infinite;
}

.sparkle-1 {
  top: 5px;
  left: 20%;
  animation-delay: 0s;
}

.sparkle-2 {
  bottom: 5px;
  right: 20%;
  animation-delay: 0.75s;
}

/* ========== 텍스트 스타일 ========== */
.prompt-title {
  font-size: 1.875rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.75rem;
  line-height: 1.2;
}

:root.dark .prompt-title {
  color: #f3f4f6;
}

.prompt-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 2rem;
  line-height: 1.5;
}

:root.dark .prompt-description {
  color: rgba(243, 244, 246, 0.85);
}

/* ========== 액션 버튼 ========== */
.prompt-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.prompt-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.prompt-btn.primary {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
}

.prompt-btn.primary:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.prompt-btn.secondary {
  background: white;
  color: #6366f1;
  border: 2px solid transparent;
}

:root.dark .prompt-btn.secondary {
  background: #f3f4f6;
  color: #6366f1;
}

.prompt-btn.secondary:hover {
  background: transparent;
  color: white;
  border-color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
}

:root.dark .prompt-btn.secondary:hover {
  color: #f3f4f6;
  border-color: #f3f4f6;
}

/* 페이드 트랜지션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ========== 반응형: 오버레이 스타일 ========== */
/* 태블릿 */
@media (max-width: 1024px) {
  .prompt-title {
    font-size: 1.625rem;
  }

  .prompt-description {
    font-size: 0.9375rem;
  }

  .prompt-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .prompt-btn {
    width: 100%;
    justify-content: center;
  }
}

/* 모바일 */
@media (max-width: 768px) {
  .login-prompt-overlay {
    padding: 1.5rem;
  }

  .prompt-icon {
    margin-bottom: 1rem;
    height: 55px;
  }

  .lock-icon {
    font-size: 2.75rem;
  }

  .sparkle-1,
  .sparkle-2 {
    font-size: 1.125rem;
  }

  .prompt-title {
    font-size: 1.5rem;
  }

  .prompt-description {
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
  }

  .prompt-btn {
    padding: 0.75rem 1.5rem;
    font-size: 0.9375rem;
  }
}

/* 작은 모바일 */
@media (max-width: 480px) {
  .login-prompt-overlay {
    padding: 1.25rem;
  }

  .prompt-icon {
    height: 50px;
    margin-bottom: 0.875rem;
  }

  .lock-icon {
    font-size: 2.5rem;
  }

  .sparkle-1,
  .sparkle-2 {
    font-size: 1rem;
  }

  .prompt-title {
    font-size: 1.375rem;
  }

  .prompt-description {
    font-size: 0.8125rem;
    margin-bottom: 1.25rem;
  }

  .prompt-btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.875rem;
    gap: 0.375rem;
  }

  .prompt-btn i {
    font-size: 0.75rem;
  }
}
</style>
