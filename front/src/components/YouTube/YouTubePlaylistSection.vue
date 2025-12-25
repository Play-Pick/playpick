<template>
  <section class="youtube-section">
    <!-- Section header -->
    <div class="section-header">
      <h2 class="section-title">
        <i class="fab fa-youtube"></i>
        공연 영상
      </h2>
      <p class="section-subtitle">추천 공연 영상을 확인해보세요</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">영상을 불러오는 중...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle error-icon"></i>
      <p class="error-text">{{ error }}</p>
    </div>

    <!-- Videos carousel -->
    <div v-else-if="videos.length > 0" class="video-carousel">
      <div class="carousel-wrapper">
        <!-- Left arrow -->
        <button
          v-if="canGoPrev"
          @click="goToPrevPage"
          class="nav-arrow nav-arrow-left"
          aria-label="이전 영상 보기"
        >
          <i class="fas fa-chevron-left"></i>
        </button>

        <!-- Video grid -->
        <div class="videos-grid">
          <div
            v-for="video in displayedVideos"
            :key="video.videoId"
            class="video-card"
            @click="openModal(video.videoId)"
          >
            <!-- Thumbnail -->
            <div class="thumbnail-wrapper">
              <img :src="video.thumbnailUrl" :alt="video.title" class="thumbnail" />
              <div class="play-overlay">
                <i class="fab fa-youtube"></i>
              </div>
            </div>

            <!-- Video info -->
            <div class="video-info">
              <h3 class="video-title">{{ video.title }}</h3>
              <p class="video-channel">PlayPick 추천</p>
            </div>
          </div>
        </div>

        <!-- Right arrow -->
        <button
          v-if="canGoNext"
          @click="goToNextPage"
          class="nav-arrow nav-arrow-right"
          aria-label="다음 영상 보기"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="empty-state">
      <i class="fab fa-youtube empty-icon"></i>
      <p class="empty-text">표시할 영상이 없습니다.</p>
    </div>

    <!-- Video modal -->
    <YouTubeModal :show="showModal" :videoId="selectedVideoId" @close="closeModal" />
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import youtubeAPI from '@/api/youtube'
import YouTubeModal from './YouTubeModal.vue'

const videos = ref([])
const loading = ref(false)
const error = ref(null)

// Pagination
const currentPage = ref(0)
const itemsPerPage = 3

// Modal
const showModal = ref(false)
const selectedVideoId = ref('')

// Computed
const displayedVideos = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return videos.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(videos.value.length / itemsPerPage))
const canGoPrev = computed(() => currentPage.value > 0)
const canGoNext = computed(() => currentPage.value < totalPages.value - 1)

// Methods
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

const openModal = (videoId) => {
  selectedVideoId.value = videoId
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedVideoId.value = ''
}

const loadVideos = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await youtubeAPI.getPlaylistVideos()
    videos.value = response.data.videos || []
  } catch (err) {
    console.error('Failed to load YouTube videos:', err)
    error.value = '영상을 불러오는데 실패했습니다.'
    videos.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadVideos()
})
</script>

<style scoped>
/* Section */
.youtube-section {
  margin-bottom: 6rem;
}

/* Header */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--card-text-primary);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.section-title i {
  color: #ff0000; /* YouTube red */
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
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
  border-top-color: #ff0000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: var(--card-text-secondary);
  font-size: 1.125rem;
  font-weight: 500;
}

/* Error */
.error-container {
  text-align: center;
  padding: 5rem 0;
}

.error-icon {
  font-size: 4rem;
  color: #ef4444;
  margin-bottom: 1.5rem;
}

.error-text {
  color: #dc2626;
  font-size: 1.125rem;
}

/* Carousel */
.video-carousel {
  max-width: 1280px;
  margin: 0 auto;
}

.carousel-wrapper {
  position: relative;
  padding: 0 3.5rem;
}

/* Videos grid - 3 columns */
.videos-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 1rem 0;
}

/* Video card */
.video-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 1rem;
  overflow: hidden;
  background: var(--card-bg);
}

.video-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
}

.thumbnail-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  background: #000;
  overflow: hidden;
}

.thumbnail {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.video-card:hover .thumbnail {
  transform: scale(1.1);
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 4rem;
  height: 4rem;
  background: rgba(255, 0, 0, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-card:hover .play-overlay {
  opacity: 1;
}

.play-overlay i {
  font-size: 2rem;
  color: white;
}

.video-info {
  padding: 1rem;
}

.video-title {
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

.video-channel {
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

/* Navigation arrows */
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

:root.dark .nav-arrow {
  background: white !important;
}

.nav-arrow:hover {
  background: #ff0000;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
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

:root.dark .nav-arrow i {
  color: #111827 !important;
}

.nav-arrow:hover i {
  color: white;
}

:root.dark .nav-arrow:hover i {
  color: #111827 !important;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 5rem 0;
}

.empty-icon {
  font-size: 5rem;
  color: #d1d5db;
  margin-bottom: 1.5rem;
}

.empty-text {
  font-size: 1.25rem;
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 1024px) {
  .videos-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
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

  .videos-grid {
    grid-template-columns: 1fr;
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
}
</style>
