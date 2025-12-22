<template>
  <transition name="fade-overlay">
    <div v-if="welcomeStore.shouldShowWelcome" class="welcome-overlay" @click.self="handleSkip">
      <!-- Sparkle particles -->
      <div class="particles">
        <div v-for="i in 15" :key="i" class="particle" :style="getParticleStyle(i)"></div>
      </div>

      <!-- Main content -->
      <transition name="slide-up">
        <div v-if="showContent" class="welcome-content">
          <!-- Welcome icon -->
          <div class="welcome-icon">
            <i class="fas fa-sparkles"></i>
          </div>

          <!-- Title -->
          <h1 class="welcome-title">
            {{ welcomeStore.welcomeData?.username }}님, 환영해요 ✨
          </h1>

          <!-- Subtitle -->
          <p class="welcome-subtitle">
            취향을 반영해 오늘의 공연을 준비했어요
          </p>

          <!-- Keywords chips -->
          <div v-if="welcomeStore.welcomeData?.keywords?.length > 0" class="keywords">
            <span
              v-for="(keyword, index) in welcomeStore.welcomeData.keywords"
              :key="index"
              class="keyword-chip"
            >
              {{ keyword }}
            </span>
          </div>

          <!-- Skip button -->
          <button @click="handleSkip" class="skip-btn">
            바로 시작하기
          </button>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useWelcomeStore } from '@/stores/welcomeStore'

const router = useRouter()
const welcomeStore = useWelcomeStore()

const showContent = ref(false)
let autoCloseTimer = null

// Particle positioning
const getParticleStyle = (index) => {
  const angle = (index / 15) * 360
  const radius = 40 + Math.random() * 20
  const x = Math.cos(angle * Math.PI / 180) * radius
  const y = Math.sin(angle * Math.PI / 180) * radius
  const delay = Math.random() * 2
  const duration = 2 + Math.random() * 2

  return {
    left: `calc(50% + ${x}vw)`,
    top: `calc(50% + ${y}vh)`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

// Handle skip
const handleSkip = () => {
  clearAutoCloseTimer()
  closeWelcome()
}

// Handle ESC key
const handleKeydown = (e) => {
  if (e.key === 'Escape') {
    handleSkip()
  }
}

// Close welcome and navigate
const closeWelcome = () => {
  console.log('[WelcomeOverlay] Closing welcome...')
  showContent.value = false

  setTimeout(() => {
    console.log('[WelcomeOverlay] Hiding overlay and navigating...')
    welcomeStore.hideWelcome()
    unlockBodyScroll()

    // Navigate to main page
    console.log('[WelcomeOverlay] Pushing to home route')
    router.push('/')
  }, 400)
}

// Auto-close after 2.5 seconds
const startAutoCloseTimer = () => {
  console.log('[WelcomeOverlay] Starting auto-close timer (2.5s)...')
  autoCloseTimer = setTimeout(() => {
    console.log('[WelcomeOverlay] Auto-close timer fired')
    closeWelcome()
  }, 2500)
}

const clearAutoCloseTimer = () => {
  if (autoCloseTimer) {
    clearTimeout(autoCloseTimer)
    autoCloseTimer = null
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

// Watch for overlay to show
watch(() => welcomeStore.shouldShowWelcome, (newVal) => {
  console.log('[WelcomeOverlay] shouldShowWelcome changed to:', newVal)

  if (newVal) {
    console.log('[WelcomeOverlay] Showing welcome overlay')
    lockBodyScroll()
    window.addEventListener('keydown', handleKeydown)

    // Show content with delay for animation
    setTimeout(() => {
      console.log('[WelcomeOverlay] Showing content')
      showContent.value = true
    }, 100)

    // Start auto-close timer
    startAutoCloseTimer()
  } else {
    console.log('[WelcomeOverlay] Hiding welcome overlay')
    unlockBodyScroll()
    window.removeEventListener('keydown', handleKeydown)
    clearAutoCloseTimer()
  }
})

onBeforeUnmount(() => {
  unlockBodyScroll()
  window.removeEventListener('keydown', handleKeydown)
  clearAutoCloseTimer()
})
</script>

<style scoped>
/* Overlay */
.welcome-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(147, 51, 234, 0.15) 100%),
              linear-gradient(to bottom, rgba(17, 24, 39, 0.95), rgba(31, 41, 55, 0.95));
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Particles */
.particles {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
  opacity: 0;
  animation: sparkle 3s ease-in-out infinite;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
}

@keyframes sparkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0) translateY(0);
  }
  50% {
    opacity: 1;
    transform: scale(1) translateY(-20px);
  }
}

/* Content */
.welcome-content {
  text-align: center;
  padding: 3rem 2rem;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  border-radius: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

:root.dark .welcome-content {
  background: rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.08);
}

/* Icon */
.welcome-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: pulse-glow 2s ease-in-out infinite;
}

.welcome-icon i {
  background: linear-gradient(135deg, #6366f1, #9333ea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 20px rgba(147, 51, 234, 0.6));
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(1);
    filter: drop-shadow(0 0 20px rgba(147, 51, 234, 0.6));
  }
  50% {
    transform: scale(1.1);
    filter: drop-shadow(0 0 30px rgba(147, 51, 234, 0.8));
  }
}

/* Title */
.welcome-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1rem;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  line-height: 1.2;
}

/* Subtitle */
.welcome-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  font-weight: 500;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

/* Keywords */
.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.keyword-chip {
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(147, 51, 234, 0.3));
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  animation: chip-appear 0.4s ease-out backwards;
}

.keyword-chip:nth-child(1) { animation-delay: 0.2s; }
.keyword-chip:nth-child(2) { animation-delay: 0.3s; }
.keyword-chip:nth-child(3) { animation-delay: 0.4s; }

@keyframes chip-appear {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Skip button */
.skip-btn {
  padding: 0.875rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(8px);
}

.skip-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Transitions */
.fade-overlay-enter-active {
  animation: fade-in 0.3s ease-out;
}

.fade-overlay-leave-active {
  animation: fade-out 0.4s ease-in;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

.slide-up-enter-active {
  animation: slide-up 0.5s ease-out;
}

.slide-up-leave-active {
  animation: slide-down 0.4s ease-in;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-down {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .welcome-content {
    padding: 2rem 1.5rem;
    border-radius: 1.5rem;
  }

  .welcome-icon {
    font-size: 3rem;
  }

  .welcome-title {
    font-size: 1.75rem;
  }

  .welcome-subtitle {
    font-size: 1rem;
  }

  .keyword-chip {
    font-size: 0.75rem;
    padding: 0.4rem 1rem;
  }
}
</style>
