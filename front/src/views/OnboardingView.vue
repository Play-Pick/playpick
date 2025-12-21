<template>
  <div class="onboarding-container">
    <!-- Header -->
    <div class="onboarding-header">
      <h1 class="title">어떤 공연을 좋아하시나요?</h1>
      <p class="subtitle">최소 8개를 선택해주세요. 더 정확한 추천을 받을 수 있어요!</p>

      <!-- Progress bar -->
      <div class="progress-wrapper">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${onboardingStore.progress}%` }"></div>
        </div>
        <span class="progress-text">
          {{ onboardingStore.canComplete ? '완료 가능!' : `선택 ${onboardingStore.signalCount} / 8` }}
        </span>
      </div>

      <!-- Refresh button -->
      <button
        v-if="!onboardingStore.loading"
        @click="handleRefresh"
        :disabled="refreshing"
        class="refresh-button"
      >
        <i class="fas fa-sync-alt" :class="{ spinning: refreshing }"></i>
        <span>다른 공연 보기 (최대 4개 교체)</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="onboardingStore.loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">로딩중...</p>
    </div>

    <!-- Error -->
    <div v-else-if="onboardingStore.error" class="error-container">
      <p class="error-text">{{ onboardingStore.error }}</p>
      <button @click="onboardingStore.fetchCandidates()" class="retry-button">
        다시 시도
      </button>
    </div>

    <!-- Performance grid -->
    <div v-else class="performances-grid">
      <div
        v-for="performance in onboardingStore.performances"
        :key="performance.mt20id"
        class="performance-card"
        :class="{
          'selected-like': onboardingStore.signals[performance.mt20id] === 1.5,
          'selected-dislike': onboardingStore.signals[performance.mt20id] === -1.0,
          'unselected': !onboardingStore.signals[performance.mt20id]
        }"
      >
        <!-- Poster -->
        <div class="poster-wrapper">
          <img :src="performance.poster" :alt="performance.prfnm" class="poster" />

          <!-- Selected badge -->
          <div
            v-if="onboardingStore.signals[performance.mt20id] && onboardingStore.signals[performance.mt20id] !== 0"
            class="selected-badge"
            :class="{
              'badge-like': onboardingStore.signals[performance.mt20id] === 1.5,
              'badge-dislike': onboardingStore.signals[performance.mt20id] === -1.0
            }"
          >
            <i :class="onboardingStore.signals[performance.mt20id] > 0 ? 'fas fa-heart' : 'fas fa-times'"></i>
            <span class="badge-text">
              {{ onboardingStore.signals[performance.mt20id] > 0 ? '보고싶음' : '관심없음' }}
            </span>
          </div>
        </div>

        <!-- Info -->
        <div class="card-info">
          <h3 class="performance-title">{{ performance.prfnm }}</h3>
          <p class="performance-genre">{{ performance.genrenm }}</p>
        </div>

        <!-- Action buttons -->
        <div class="action-buttons">
          <button
            @click="handleSignal(performance.mt20id, 1.5)"
            class="btn-action btn-like"
            :class="{ active: onboardingStore.signals[performance.mt20id] === 1.5 }"
          >
            <i class="fas fa-heart"></i>
            <span>보고싶어요</span>
          </button>

          <button
            @click="handleSignal(performance.mt20id, 0)"
            class="btn-action btn-neutral"
            :class="{ active: !onboardingStore.signals[performance.mt20id] }"
          >
            <i class="fas fa-question"></i>
            <span>모르겠어요</span>
          </button>

          <button
            @click="handleSignal(performance.mt20id, -1.0)"
            class="btn-action btn-dislike"
            :class="{ active: onboardingStore.signals[performance.mt20id] === -1.0 }"
          >
            <i class="fas fa-times"></i>
            <span>안볼래요</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Complete button -->
    <div class="complete-section">
      <button
        @click="handleComplete"
        :disabled="!onboardingStore.canComplete || submitting"
        class="complete-button"
      >
        <span v-if="submitting">완료 중...</span>
        <span v-else>완료하고 시작하기</span>
      </button>

      <p v-if="!onboardingStore.canComplete" class="hint-text">
        {{ 8 - onboardingStore.signalCount }}개 더 선택해주세요
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOnboardingStore } from '@/stores/onboardingStore'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const onboardingStore = useOnboardingStore()
const authStore = useAuthStore()
const submitting = ref(false)
const refreshing = ref(false)

const handleSignal = (performanceId, signalValue) => {
  onboardingStore.setSignal(performanceId, signalValue)
}

const handleRefresh = async () => {
  if (refreshing.value) return

  refreshing.value = true
  await onboardingStore.refreshUnselectedCards(4)
  refreshing.value = false
}

const handleComplete = async () => {
  if (!onboardingStore.canComplete || submitting.value) return

  submitting.value = true

  try {
    // Save signals
    const signalsSaved = await onboardingStore.saveSignals()
    if (!signalsSaved) {
      submitting.value = false
      return
    }

    // Complete onboarding
    const completed = await onboardingStore.complete()
    if (!completed) {
      submitting.value = false
      return
    }

    // Refresh user data
    await authStore.fetchCurrentUser()

    // Redirect to main page
    router.push('/')
  } catch (err) {
    console.error('Onboarding completion error:', err)
    submitting.value = false
  }
}

onMounted(() => {
  onboardingStore.fetchCandidates('balanced')
})
</script>

<style scoped>
.onboarding-container {
  min-height: 100vh;
  padding: 3rem 1rem;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
}

:root.dark .onboarding-container {
  background: linear-gradient(to bottom, #111827, #1f2937);
}

.onboarding-header {
  max-width: 1280px;
  margin: 0 auto 3rem;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--card-text-primary);
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.25rem;
  color: var(--card-text-secondary);
  margin-bottom: 2rem;
}

.progress-wrapper {
  max-width: 500px;
  margin: 0 auto;
}

.progress-bar {
  height: 1rem;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

:root.dark .progress-bar {
  background: #374151;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #6366f1, #9333ea);
  transition: width 0.3s;
}

.progress-text {
  font-size: 1rem;
  font-weight: 600;
  color: var(--card-text-secondary);
}

/* Refresh button */
.refresh-button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 9999px;
  background: white;
  color: #6366f1;
  border: 2px solid #6366f1;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .refresh-button {
  background: #1f2937;
  color: #818cf8;
  border-color: #818cf8;
}

.refresh-button:hover:not(:disabled) {
  background: #6366f1;
  color: white;
  transform: scale(1.05);
}

:root.dark .refresh-button:hover:not(:disabled) {
  background: #818cf8;
  color: white;
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-button .fa-sync-alt.spinning {
  animation: spin 1s linear infinite;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 5rem 0;
}

.spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

:root.dark .spinner {
  border-color: #374151;
  border-top-color: #6366f1;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: var(--card-text-secondary);
  font-size: 1.125rem;
}

/* Error */
.error-container {
  text-align: center;
  padding: 3rem 0;
}

.error-text {
  color: #dc2626;
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.retry-button {
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 9999px;
  background: #6366f1;
  color: white;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.retry-button:hover {
  background: #4f46e5;
}

/* Performances grid */
.performances-grid {
  max-width: 1280px;
  margin: 0 auto 3rem;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.performance-card {
  background: var(--card-bg);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border: 3px solid transparent;
}

/* Like state: red border + elevation */
.performance-card.selected-like {
  transform: translateY(-0.5rem);
  box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3);
  border-color: #ef4444;
}

/* Dislike state: gray + opacity */
.performance-card.selected-dislike {
  opacity: 0.6;
  filter: grayscale(0.5);
  border-color: #6b7280;
}

/* Unselected state: default */
.performance-card.unselected {
  opacity: 1;
  filter: none;
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

.selected-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
}

.selected-badge.badge-like {
  background: rgba(239, 68, 68, 0.95);
}

.selected-badge.badge-dislike {
  background: rgba(107, 116, 128, 0.95);
}

.badge-text {
  font-size: 0.875rem;
  letter-spacing: -0.025em;
}

.card-info {
  padding: 1rem;
}

.performance-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--card-text-primary);
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.performance-genre {
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

/* Action buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0 1rem 1rem;
}

.btn-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 0.5rem;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-like {
  background: #fef2f2;
  color: #dc2626;
}

:root.dark .btn-like {
  background: rgba(220, 38, 38, 0.1);
  color: #ef4444;
}

.btn-like.active {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.btn-neutral {
  background: #f3f4f6;
  color: #6b7280;
}

:root.dark .btn-neutral {
  background: #374151;
  color: #9ca3af;
}

.btn-neutral.active {
  background: #e5e7eb;
  border-color: #9ca3af;
}

:root.dark .btn-neutral.active {
  background: #4b5563;
  border-color: #6b7280;
}

.btn-dislike {
  background: #f9fafb;
  color: #9ca3af;
}

:root.dark .btn-dislike {
  background: #1f2937;
  color: #6b7280;
}

.btn-dislike.active {
  background: #6b7280;
  color: white;
  border-color: #6b7280;
}

/* Complete section */
.complete-section {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
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
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.complete-button:hover:not(:disabled) {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.complete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint-text {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
  .performances-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .performances-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .performances-grid {
    grid-template-columns: 1fr;
  }
}
</style>
