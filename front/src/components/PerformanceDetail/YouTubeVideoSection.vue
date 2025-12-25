<template>
  <div class="youtube-video-section">
    <h3 class="section-title">
      <i class="fab fa-youtube"></i>
      관련 영상
    </h3>

    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">영상을 검색하는 중...</p>
    </div>

    <!-- Found video -->
    <div v-else-if="status === 'FOUND'" class="video-found">
      <div class="video-card" @click="openModal">
        <div class="thumbnail-wrapper">
          <img :src="videoData.thumbnailUrl" :alt="videoData.title" class="thumbnail" />
          <div class="play-overlay">
            <i class="fab fa-youtube"></i>
            <span>재생하기</span>
          </div>
        </div>
        <div class="video-info">
          <h4 class="video-title">{{ videoData.title }}</h4>
          <p class="video-channel">PlayPick 추천</p>
        </div>
      </div>
    </div>

    <!-- No video found - fallback -->
    <div v-else-if="status === 'NONE'" class="no-video">
      <div class="no-video-icon">
        <i class="fas fa-video-slash"></i>
      </div>
      <p class="no-video-text">공식 영상이 없습니다</p>
      <div class="fallback-links">
        <a :href="fallbackData.youtubeSearchUrl" target="_blank" rel="noopener" class="fallback-button">
          <i class="fab fa-youtube"></i>
          YouTube에서 검색
        </a>
        <a :href="fallbackData.fallbackPlaylistUrl" target="_blank" rel="noopener" class="fallback-button secondary">
          <i class="fas fa-list"></i>
          추천 플레이리스트
        </a>
      </div>
    </div>

    <!-- Modal -->
    <YouTubeModal :show="showModal" :videoId="videoData?.videoId" @close="closeModal" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import youtubeAPI from '@/api/youtube'
import YouTubeModal from '@/components/YouTube/YouTubeModal.vue'

const props = defineProps({
  performanceId: {
    type: [String, Number],
    required: true
  }
})

const loading = ref(false)
const status = ref(null) // 'FOUND' or 'NONE'
const videoData = ref(null)
const fallbackData = ref(null)
const showModal = ref(false)

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const loadVideo = async () => {
  loading.value = true

  try {
    const response = await youtubeAPI.getPerformanceVideo(props.performanceId)
    status.value = response.data.status

    if (response.data.status === 'FOUND') {
      videoData.value = {
        videoId: response.data.videoId,
        title: response.data.title,
        channelTitle: response.data.channelTitle,
        thumbnailUrl: response.data.thumbnailUrl,
        youtubeUrl: response.data.youtubeUrl
      }
    } else {
      fallbackData.value = {
        youtubeSearchUrl: response.data.youtubeSearchUrl,
        fallbackPlaylistUrl: response.data.fallbackPlaylistUrl
      }
    }
  } catch (err) {
    console.error('Failed to load performance video:', err)
    // On error, show NONE status
    status.value = 'NONE'
    fallbackData.value = {
      youtubeSearchUrl: 'https://www.youtube.com/results?search_query=%EA%B3%B5%EC%97%B0',
      fallbackPlaylistUrl: 'https://www.youtube.com'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadVideo()
})
</script>

<style scoped>
.youtube-video-section {
  margin-top: 3rem;
  padding: 2rem;
  background: var(--card-bg);
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--card-text-primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-title i {
  color: #ff0000;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 3rem 0;
}

.spinner {
  display: inline-block;
  width: 3rem;
  height: 3rem;
  border: 3px solid #e5e7eb;
  border-top-color: #ff0000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1rem;
  color: var(--card-text-secondary);
}

/* Video found */
.video-found {
  max-width: 600px;
}

.video-card {
  cursor: pointer;
  border-radius: 0.75rem;
  overflow: hidden;
  background: var(--bg-secondary);
  transition: transform 0.3s, box-shadow 0.3s;
}

.video-card:hover {
  transform: translateY(-0.25rem);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

.thumbnail-wrapper {
  position: relative;
  padding-bottom: 56.25%;
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
  transform: scale(1.05);
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-card:hover .play-overlay {
  opacity: 1;
}

.play-overlay i {
  font-size: 3rem;
  color: white;
}

.play-overlay span {
  font-size: 1.125rem;
  font-weight: 700;
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
}

.video-channel {
  font-size: 0.875rem;
  color: var(--card-text-secondary);
}

/* No video */
.no-video {
  text-align: center;
  padding: 3rem 0;
}

.no-video-icon {
  font-size: 4rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.no-video-text {
  font-size: 1.125rem;
  color: var(--card-text-secondary);
  margin-bottom: 2rem;
}

.fallback-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.fallback-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: 9999px;
  text-decoration: none;
  transition: all 0.3s;
  background: #ff0000;
  color: white;
}

.fallback-button:hover {
  background: #cc0000;
  transform: scale(1.05);
}

.fallback-button.secondary {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.fallback-button.secondary:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
}

@media (max-width: 768px) {
  .youtube-video-section {
    padding: 1.5rem;
  }

  .fallback-links {
    flex-direction: column;
    align-items: center;
  }

  .fallback-button {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
}
</style>
