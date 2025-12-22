<template>
  <!-- Full-screen overlay with dark background -->
  <div class="onboarding-overlay">
    <!-- Header with progress and controls -->
    <div class="onboarding-header">
      <div class="header-content">
        <!-- Progress indicator -->
        <div class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${store.progress}%` }"></div>
          </div>
          <span class="progress-text">
            {{ store.canComplete ? '완료 가능!' : `선택 ${store.likeCount} / 8` }}
          </span>
        </div>

        <!-- Skip button (top-right) -->
        <div class="header-actions">
          <button @click="handleSkipOnboarding" class="skip-button">
            나중에 하기
          </button>
          <button
            @click="handleComplete"
            :disabled="!store.canComplete || submitting"
            class="complete-header-button"
          >
            <span v-if="submitting">완료 중...</span>
            <span v-else>바로 완료하기</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main content area -->
    <div class="onboarding-content">
      <!-- Loading state -->
      <div v-if="store.loading && store.candidates.length === 0" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">로딩중...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="store.error" class="error-container">
        <p class="error-text">{{ store.error }}</p>
        <button @click="store.fetchCandidates()" class="retry-button">
          다시 시도
        </button>
      </div>

      <!-- No candidates available -->
      <div v-else-if="!store.currentCard && store.candidates.length === 0" class="empty-container">
        <p class="empty-text">후보 공연을 불러오지 못했어요.</p>
        <button @click="store.fetchCandidates()" class="retry-button">
          다시 시도
        </button>
      </div>

      <!-- Card display area -->
      <div v-else-if="store.currentCard" class="card-area">
        <!-- Single performance card with animation -->
        <transition :name="cardTransition" @after-leave="onCardTransitionEnd">
          <div
            v-if="showCard"
            :key="store.currentCard.mt20id"
            class="performance-card"
            :class="cardAnimationClass"
          >
            <!-- Poster (3:4 ratio) -->
            <div class="poster-wrapper">
              <img :src="store.currentCard.poster" :alt="store.currentCard.prfnm" class="poster" />
            </div>

            <!-- Info section -->
            <div class="card-info">
              <h2 class="performance-title">{{ store.currentCard.prfnm }}</h2>
              <p class="performance-details">
                <span class="detail-item">{{ store.currentCard.genrenm }}</span>
                <span class="detail-divider">·</span>
                <span class="detail-item">{{ store.currentCard.area }}</span>
              </p>
              <p class="performance-period">
                {{ formatPeriod(store.currentCard.prfpdfrom, store.currentCard.prfpdto) }}
              </p>
            </div>

            <!-- Action buttons -->
            <div class="action-buttons">
              <button @click="handleDislike" class="btn-action btn-dislike">
                <i class="fas fa-times"></i>
                <span>안볼래요</span>
              </button>

              <button @click="handleSkip" class="btn-action btn-skip">
                <i class="fas fa-question"></i>
                <span>모르겠어요</span>
              </button>

              <button @click="handleLike" class="btn-action btn-like">
                <i class="fas fa-heart"></i>
                <span>보고싶어요</span>
              </button>
            </div>
          </div>
        </transition>

        <!-- Keyboard shortcuts hint -->
        <div class="keyboard-hint">
          <span class="hint-item"><kbd>←</kbd> 안볼래요</span>
          <span class="hint-item"><kbd>Space</kbd> 모르겠어요</span>
          <span class="hint-item"><kbd>→</kbd> 보고싶어요</span>
        </div>

        <!-- Loading more indicator (bottom) -->
        <div v-if="isLoadingMore" class="loading-more">
          <div class="small-spinner"></div>
          <span>더 많은 공연을 불러오는 중...</span>
        </div>
      </div>

      <!-- Completion state -->
      <div v-else-if="!store.hasMore && store.totalResponses > 0" class="completion-container">
        <div class="completion-content">
          <div class="completion-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <h2 class="completion-title">모든 공연을 확인했어요!</h2>
          <p class="completion-subtitle">
            총 {{ store.likeCount }}개의 공연을 선택하셨습니다.
          </p>

          <button
            v-if="store.canComplete"
            @click="handleComplete"
            :disabled="submitting"
            class="complete-button"
          >
            <span v-if="submitting">완료 중...</span>
            <span v-else>완료하고 시작하기</span>
          </button>

          <p v-else class="hint-text">
            최소 8개를 선택해야 완료할 수 있어요. ({{ 8 - store.likeCount }}개 부족)
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useOnboardingStore } from '@/stores/onboardingStore'
import { useAuthStore } from '@/stores/authStore'
import { useWelcomeStore } from '@/stores/welcomeStore'

const router = useRouter()
const store = useOnboardingStore()
const authStore = useAuthStore()
const welcomeStore = useWelcomeStore()

const submitting = ref(false)
const showCard = ref(true)
const cardTransition = ref('')
const cardAnimationClass = ref('')
const isLoadingMore = ref(false)

// Format date period
const formatPeriod = (from, to) => {
  if (!from || !to) return ''
  const fromDate = from.replace(/\./g, '/')
  const toDate = to.replace(/\./g, '/')
  return `${fromDate} ~ ${toDate}`
}

// Auto-load more candidates when approaching the end
const checkAndLoadMore = async () => {
  // If we're within 3 cards of the end, load more
  const remainingCards = store.candidates.length - store.currentIndex

  if (remainingCards <= 3 && !isLoadingMore.value && !store.loading) {
    isLoadingMore.value = true
    await store.loadMoreCandidates('balanced')
    isLoadingMore.value = false
  }
}

// Watch currentIndex to auto-load more
watch(() => store.currentIndex, async () => {
  await checkAndLoadMore()
})

// Card animation handlers
const animateCard = (direction) => {
  showCard.value = false
  cardTransition.value = direction
}

const onCardTransitionEnd = () => {
  showCard.value = true
  cardTransition.value = ''
  cardAnimationClass.value = ''
}

// Action handlers
const handleLike = () => {
  cardAnimationClass.value = 'swipe-right'
  animateCard('slide-right')
  setTimeout(() => {
    store.chooseLike()
  }, 150)
}

const handleDislike = () => {
  cardAnimationClass.value = 'swipe-left'
  animateCard('slide-left')
  setTimeout(() => {
    store.chooseDislike()
  }, 150)
}

const handleSkip = () => {
  cardAnimationClass.value = 'fade-out'
  animateCard('fade')
  setTimeout(() => {
    store.chooseSkip()
  }, 150)
}

// Keyboard shortcuts
const handleKeydown = (e) => {
  if (store.loading || submitting.value || !store.currentCard) return

  switch (e.key) {
    case 'ArrowLeft':
      e.preventDefault()
      handleDislike()
      break
    case 'ArrowRight':
      e.preventDefault()
      handleLike()
      break
    case ' ':
      e.preventDefault()
      handleSkip()
      break
  }
}

// Skip onboarding
const handleSkipOnboarding = () => {
  if (confirm('나중에 선호도를 설정하시겠어요? 추천 품질이 떨어질 수 있습니다.')) {
    // Remember skip per-user so 라우터 가드가 막지 않도록 한다
    const skipKey = authStore.userId ? `onboarding_skipped_${authStore.userId}` : 'onboarding_skipped'
    localStorage.setItem(skipKey, '1')
    unlockBodyScroll()
    router.push('/')
  }
}

// Complete onboarding
const handleComplete = async () => {
  if (!store.canComplete || submitting.value) return

  submitting.value = true

  try {
    console.log('[Onboarding] Starting completion...')

    const success = await store.submit()
    console.log('[Onboarding] Submit result:', success)

    if (!success) {
      submitting.value = false
      return
    }

    // Refresh user data
    console.log('[Onboarding] Refreshing user data...')
    await authStore.fetchCurrentUser()
    console.log('[Onboarding] User data refreshed:', authStore.user)

    // 완료 시 스킵 플래그는 지운다 (user-scoped)
    const skipKey = authStore.userId ? `onboarding_skipped_${authStore.userId}` : 'onboarding_skipped'
    localStorage.removeItem(skipKey)

    // Unlock body scroll before navigation
    unlockBodyScroll()

    // Get selected performances for welcome overlay
    const selectedPerformances = store.candidates.filter(perf =>
      store.likes.includes(perf.mt20id)
    )
    console.log('[Onboarding] Selected performances:', selectedPerformances.length)

    // Show welcome overlay (will handle localStorage check internally)
    const wasShown = welcomeStore.showWelcome({
      username: authStore.displayName,
      userId: authStore.userId,
      selectedPerformances: selectedPerformances
    })

    console.log('[Onboarding] Welcome overlay shown:', wasShown)

    // If welcome overlay was not shown (already seen), redirect immediately
    if (!wasShown) {
      console.log('[Onboarding] Redirecting to home (no welcome)...')
      localStorage.removeItem('onboarding_skipped')
      router.push('/')
    } else {
      console.log('[Onboarding] Welcome overlay will handle navigation')
    }
  } catch (err) {
    console.error('[Onboarding] Completion error:', err)
    alert('온보딩 완료 중 오류가 발생했습니다. 다시 시도해주세요.')
  } finally {
    submitting.value = false
  }
}

// Body scroll lock
const lockBodyScroll = () => {
  document.body.style.overflow = 'hidden'
  document.body.style.position = 'fixed'
  document.body.style.width = '100%'
}

const unlockBodyScroll = () => {
  document.body.style.overflow = ''
  document.body.style.position = ''
  document.body.style.width = ''
}

// Lifecycle
onMounted(async () => {
  await store.fetchCandidates('balanced')
  lockBodyScroll()
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  unlockBodyScroll()
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Full-screen overlay with dark gradient background */
.onboarding-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: linear-gradient(135deg, #0a0a0f 0%, #111827 50%, #1a1a2e 100%);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

:root.dark .onboarding-overlay {
  background: linear-gradient(135deg, #000000 0%, #0a0a0f 50%, #111827 100%);
}

/* Header */
.onboarding-header {
  padding: 1.5rem 2rem;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.progress-section {
  flex: 1;
  max-width: 400px;
}

.progress-bar {
  height: 0.75rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #6366f1, #9333ea);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 16px rgba(147, 51, 234, 0.6);
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.skip-button {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(8px);
}

.skip-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.complete-header-button {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 700;
  border-radius: 9999px;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
}

.complete-header-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 12px 24px rgba(99, 102, 241, 0.45);
}

.complete-header-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Main content */
.onboarding-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

/* Loading */
.loading-container {
  text-align: center;
}

.spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Error / Empty */
.error-container,
.empty-container {
  text-align: center;
}

.error-text,
.empty-text {
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.retry-button {
  padding: 0.875rem 2rem;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 9999px;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.retry-button:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 24px rgba(99, 102, 241, 0.4);
}

/* Card area */
.card-area {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

/* Performance card */
.performance-card {
  width: 100%;
  background: white;
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:root.dark .performance-card {
  background: #1f2937;
  border-color: rgba(255, 255, 255, 0.05);
}

.performance-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.7);
}

.poster-wrapper {
  position: relative;
  padding-bottom: 133.33%; /* 3:4 ratio */
  background: #000;
  overflow: hidden;
}

.poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-info {
  padding: 1.5rem;
  background: white;
}

:root.dark .card-info {
  background: #1f2937;
}

.performance-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

:root.dark .performance-title {
  color: #f9fafb;
}

.performance-details {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.detail-item {
  font-weight: 500;
}

.detail-divider {
  color: #d1d5db;
}

.performance-period {
  font-size: 0.875rem;
  color: #9ca3af;
  font-weight: 500;
}

/* Action buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  padding: 0 1.5rem 1.5rem;
  background: white;
}

:root.dark .action-buttons {
  background: #1f2937;
}

.btn-action {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  font-size: 0.875rem;
  font-weight: 700;
  border-radius: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-action i {
  font-size: 1.5rem;
}

.btn-dislike {
  background: #fef2f2;
  color: #dc2626;
}

:root.dark .btn-dislike {
  background: rgba(220, 38, 38, 0.15);
  color: #ef4444;
}

.btn-dislike:hover {
  background: #fee2e2;
  transform: scale(1.05);
}

:root.dark .btn-dislike:hover {
  background: rgba(220, 38, 38, 0.25);
}

.btn-skip {
  background: #f3f4f6;
  color: #6b7280;
}

:root.dark .btn-skip {
  background: #374151;
  color: #9ca3af;
}

.btn-skip:hover {
  background: #e5e7eb;
  transform: scale(1.05);
}

:root.dark .btn-skip:hover {
  background: #4b5563;
}

.btn-like {
  background: #fef2f2;
  color: #dc2626;
}

:root.dark .btn-like {
  background: rgba(220, 38, 38, 0.15);
  color: #ef4444;
}

.btn-like:hover {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  transform: scale(1.05);
}

/* Keyboard hint */
.keyboard-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.hint-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

kbd {
  padding: 0.25rem 0.5rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 0.375rem;
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Loading more indicator */
.loading-more {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.small-spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* Card animations */
.slide-left-leave-active,
.slide-right-leave-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-left-leave-to {
  transform: translateX(-120%) rotate(-15deg);
  opacity: 0;
}

.slide-right-leave-to {
  transform: translateX(120%) rotate(15deg);
  opacity: 0;
}

.fade-leave-to {
  transform: scale(0.8);
  opacity: 0;
}

/* Completion */
.completion-container {
  width: 100%;
  max-width: 480px;
}

.completion-content {
  background: white;
  border-radius: 1.5rem;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:root.dark .completion-content {
  background: #1f2937;
  border-color: rgba(255, 255, 255, 0.05);
}

.completion-icon {
  font-size: 4rem;
  color: #10b981;
  margin-bottom: 1.5rem;
}

.completion-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.75rem;
}

:root.dark .completion-title {
  color: #f9fafb;
}

.completion-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 2rem;
}

.complete-button {
  width: 100%;
  padding: 1.25rem 2rem;
  font-size: 1.25rem;
  font-weight: 700;
  border-radius: 9999px;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.complete-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 15px 30px rgba(99, 102, 241, 0.5);
}

.complete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint-text {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #9ca3af;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 640px) {
  .onboarding-header {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .progress-section {
    max-width: 100%;
  }

  .card-area {
    max-width: 100%;
  }

  .keyboard-hint {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
  }

  .performance-title {
    font-size: 1.25rem;
  }

  .btn-action {
    padding: 0.75rem;
    font-size: 0.75rem;
  }

  .btn-action i {
    font-size: 1.25rem;
  }
}
</style>
