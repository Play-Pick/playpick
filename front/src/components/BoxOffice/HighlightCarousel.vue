<template>
  <section
    class="hero-banner-section"
    @mouseenter="pauseAutoplay"
    @mouseleave="resumeAutoplay"
    @keydown="handleKeydown"
    @touchstart="handleTouchStart"
    @touchend="handleTouchEnd"
    tabindex="0"
    role="region"
    aria-label="하이라이트 공연 캐러셀"
  >
    <!-- 로딩 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">하이라이트를 불러오는 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- 히어로 배너 -->
    <div v-else-if="highlightPerformances.length > 0" class="hero-container">
      <!-- 배경 레이어 (blur) -->
      <div class="hero-background">
        <img
          :src="currentPerformance.poster"
          :alt="`${currentPerformance.prfnm} 배경`"
          class="background-image"
          @error="handleImageError"
        >
        <div class="background-overlay"></div>
      </div>

      <!-- 전경 콘텐츠 -->
      <div class="hero-content">
        <!-- 포스터 카드 (3:4 비율 유지) -->
        <div class="poster-card">
          <router-link :to="`/performances/${currentPerformance.mt20id}`">
            <img
              :src="currentPerformance.poster"
              :alt="currentPerformance.prfnm"
              class="poster-image"
              @error="handleImageError"
            >
            <!-- 순위 배지 -->
            <div :class="['rank-badge', getRankBadgeClass(currentPerformance.rank)]">
              <i class="fas fa-crown"></i>
              {{ currentPerformance.rank }}위
            </div>
          </router-link>
        </div>

        <!-- 정보 섹션 -->
        <div class="info-section">
          <h2 class="performance-title">{{ currentPerformance.prfnm }}</h2>

          <div class="performance-meta">
            <p class="meta-item">
              <i class="fas fa-map-marker-alt"></i>
              {{ currentPerformance.fcltynm || '정보 없음' }}
            </p>
            <p class="meta-item">
              <i class="fas fa-calendar"></i>
              {{ formatDate(currentPerformance.prfpdfrom) }} ~ {{ formatDate(currentPerformance.prfpdto) }}
            </p>
          </div>

          <router-link
            :to="`/performances/${currentPerformance.mt20id}`"
            class="cta-button"
          >
            자세히 보기
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>

      <!-- 좌측 네비게이션 화살표 -->
      <button
        @click="prevSlide"
        class="nav-arrow nav-arrow-left"
        aria-label="이전 슬라이드"
      >
        <i class="fas fa-chevron-left"></i>
      </button>

      <!-- 우측 네비게이션 화살표 -->
      <button
        @click="nextSlide"
        class="nav-arrow nav-arrow-right"
        aria-label="다음 슬라이드"
      >
        <i class="fas fa-chevron-right"></i>
      </button>

      <!-- 인디케이터 -->
      <div class="indicators">
        <button
          v-for="(perf, index) in highlightPerformances"
          :key="`indicator-${index}`"
          @click="goToSlide(index)"
          :class="['indicator', { active: currentIndex === index }]"
          :aria-label="`슬라이드 ${index + 1}로 이동`"
          :aria-current="currentIndex === index ? 'true' : 'false'"
        ></button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAllRanking } from '@/composables/useAllRanking'

const { highlightPerformances, loading, error, loadHighlightPerformances } = useAllRanking()

const currentIndex = ref(0)
let autoplayInterval = null
let touchStartX = 0
let touchEndX = 0

// 현재 공연
const currentPerformance = computed(() => {
  return highlightPerformances.value[currentIndex.value] || {}
})

// 슬라이드 이동
const goToSlide = (index) => {
  currentIndex.value = index
  resetAutoplay()
}

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = highlightPerformances.value.length - 1
  }
  resetAutoplay()
}

const nextSlide = () => {
  if (currentIndex.value < highlightPerformances.value.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
  resetAutoplay()
}

// 자동재생
const startAutoplay = () => {
  autoplayInterval = setInterval(() => {
    if (currentIndex.value < highlightPerformances.value.length - 1) {
      currentIndex.value++
    } else {
      currentIndex.value = 0
    }
  }, 5000)
}

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
    autoplayInterval = null
  }
}

const resetAutoplay = () => {
  stopAutoplay()
  startAutoplay()
}

// 호버 일시정지
const pauseAutoplay = () => {
  stopAutoplay()
}

const resumeAutoplay = () => {
  startAutoplay()
}

// 키보드 네비게이션
const handleKeydown = (e) => {
  if (e.key === 'ArrowLeft') {
    prevSlide()
  } else if (e.key === 'ArrowRight') {
    nextSlide()
  }
}

// 터치 스와이프
const handleTouchStart = (e) => {
  touchStartX = e.changedTouches[0].screenX
}

const handleTouchEnd = (e) => {
  touchEndX = e.changedTouches[0].screenX
  const swipeDistance = touchStartX - touchEndX

  if (Math.abs(swipeDistance) > 50) {
    if (swipeDistance > 0) {
      nextSlide() // 왼쪽 스와이프 (다음 슬라이드)
    } else {
      prevSlide() // 오른쪽 스와이프 (이전 슬라이드)
    }
  }
}

// 순위 배지 클래스
const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return 'rank-default'
}

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '.')
}

// 이미지 에러 처리
const handleImageError = (event) => {
  event.target.src = '/no_poster.png'
}

// 초기 로드 및 자동재생 시작
onMounted(() => {
  loadHighlightPerformances()
  startAutoplay()
})

// 컴포넌트 해제 시 자동재생 정지
onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
/* 히어로 배너 섹션 */
.hero-banner-section {
  width: 100%;
  margin-bottom: 3rem;
  outline: none;
  position: relative;
}

/* 로딩 & 에러 */
.loading-container,
.error-container {
  text-align: center;
  padding: 5rem 0;
}

.spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: var(--card-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text,
.error-text {
  margin-top: 1.5rem;
  font-size: 1.125rem;
}

.loading-text {
  color: #6b7280;
  font-weight: 500;
}

.error-icon {
  font-size: 4rem;
  color: #ef4444;
  margin-bottom: 1.5rem;
}

.error-text {
  color: #dc2626;
}

/* 히어로 컨테이너 */
.hero-container {
  position: relative;
  width: 100%;
  height: 700px;
  overflow: hidden;
}

/* 배경 레이어 (blur) */
.hero-background {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(20px) brightness(0.7);
  transform: scale(1.1);
}

.background-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.3) 100%
  );
}

/* 전경 콘텐츠 */
.hero-content {
  position: relative;
  z-index: 10;
  max-width: 1280px;
  margin: 0 auto;
  height: 100%;
  padding: 3rem;
  display: flex;
  align-items: center;
  gap: 3rem;
}

/* 포스터 카드 (3:4 비율 유지) */
.poster-card {
  flex-shrink: 0;
  width: 320px;
  height: 427px;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  position: relative;
  transition: transform 0.3s;
}

.poster-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.6);
}

.poster-card a {
  display: block;
  width: 100%;
  height: 100%;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 순위 배지 */
.rank-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 9999px;
  font-size: 1.125rem;
  font-weight: 800;
  color: white;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.4);
}

.rank-gold {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.rank-silver {
  background: linear-gradient(135deg, #e5e7eb 0%, #9ca3af 100%);
}

.rank-bronze {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
}

.rank-default {
  background: linear-gradient(135deg, var(--card-accent) 0%, var(--card-accent-hover) 100%);
}

/* 정보 섹션 */
.info-section {
  flex: 1;
  color: white;
  animation: fadeInRight 0.8s ease;
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.performance-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 2rem;
  line-height: 1.2;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
  color: white;
}

.performance-meta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.25rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
}

.meta-item i {
  color: #fbbf24;
  width: 1.5rem;
  text-align: center;
}

/* CTA 버튼 */
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(to right, var(--card-accent), var(--card-accent-hover));
  border-radius: 9999px;
  text-decoration: none;
  box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.5);
  transition: all 0.3s;
}

:root.dark .cta-button {
  background: white !important;
  color: #111827 !important;
  box-shadow: 0 10px 20px -5px rgba(255, 255, 255, 0.3);
}

.cta-button:hover {
  background: linear-gradient(to right, var(--card-accent-hover), #7c3aed);
  box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.7);
  transform: translateY(-2px);
}

:root.dark .cta-button:hover {
  background: white !important;
  color: #111827 !important;
  box-shadow: 0 15px 30px -5px rgba(255, 255, 255, 0.5);
}

.cta-button i {
  transition: transform 0.3s;
}

.cta-button:hover i {
  transform: translateX(0.5rem);
}

/* 네비게이션 화살표 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 20;
  background: rgba(255, 255, 255, 0.95);
  color: #374151;
  border: none;
  border-radius: 50%;
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
}

.nav-arrow:hover {
  background: white;
  color: var(--card-accent);
  transform: translateY(-50%) scale(1.15);
  box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.4);
}

.nav-arrow-left {
  left: 2rem;
}

.nav-arrow-right {
  right: 2rem;
}

/* 인디케이터 */
.indicators {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;
  display: flex;
  justify-content: center;
  gap: 0.75rem;
}

.indicator {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
  padding: 0;
}

.indicator.active {
  width: 2.5rem;
  border-radius: 0.375rem;
  background: white;
}

.indicator:hover:not(.active) {
  background: rgba(255, 255, 255, 0.8);
}

/* 반응형 */
@media (max-width: 1024px) {
  .hero-container {
    height: 500px;
  }

  .hero-content {
    padding: 2rem;
    gap: 2rem;
  }

  .poster-card {
    width: 280px;
    height: 373px;
  }

  .performance-title {
    font-size: 2.5rem;
  }

  .meta-item {
    font-size: 1.125rem;
  }

  .nav-arrow {
    width: 3.5rem;
    height: 3.5rem;
    font-size: 1.25rem;
  }

  .nav-arrow-left {
    left: 1rem;
  }

  .nav-arrow-right {
    right: 1rem;
  }
}

@media (max-width: 768px) {
  .hero-container {
    height: 700px;
  }

  .hero-content {
    flex-direction: column;
    justify-content: center;
    padding: 2rem 1.5rem;
    gap: 2rem;
  }

  .poster-card {
    width: 240px;
    height: 320px;
  }

  .info-section {
    text-align: center;
  }

  .performance-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .performance-meta {
    gap: 0.75rem;
    margin-bottom: 2rem;
  }

  .meta-item {
    font-size: 1rem;
    justify-content: center;
  }

  .cta-button {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }

  .nav-arrow {
    width: 3rem;
    height: 3rem;
    font-size: 1.125rem;
  }

  .nav-arrow-left {
    left: 0.5rem;
  }

  .nav-arrow-right {
    right: 0.5rem;
  }

  .indicators {
    bottom: 1rem;
  }

  .indicator {
    width: 0.625rem;
    height: 0.625rem;
  }

  .indicator.active {
    width: 2rem;
  }
}

@media (max-width: 480px) {
  .hero-container {
    height: 650px;
  }

  .poster-card {
    width: 200px;
    height: 267px;
  }

  .performance-title {
    font-size: 1.5rem;
  }

  .meta-item {
    font-size: 0.875rem;
  }

  .rank-badge {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}
</style>
