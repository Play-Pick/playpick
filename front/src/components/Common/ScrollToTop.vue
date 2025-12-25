<template>
  <Transition name="fade-slide">
    <button
      v-if="isVisible"
      @click="scrollToTop"
      class="fab-button scroll-to-top"
      aria-label="맨 위로 이동"
    >
      <i class="fas fa-arrow-up"></i>
    </button>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const scrollThreshold = 300 // 300px 이상 스크롤 시 표시

let ticking = false

const handleScroll = () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      isVisible.value = window.scrollY > scrollThreshold
      ticking = false
    })
    ticking = true
  }
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.fab-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #9333ea 100%);
  color: white;
  border: none;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: all 0.3s;
}

.fab-button:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.4);
}

/* Transition 애니메이션 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 다크모드 시 버튼 색상 */
:root.dark .scroll-to-top {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}

/* 반응형 */
@media (max-width: 768px) {
  .fab-button {
    width: 2rem;
    height: 2rem;
    font-size: 0.875rem;
  }
}
</style>
