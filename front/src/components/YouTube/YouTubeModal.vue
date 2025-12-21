<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="modal-overlay" @click="handleClose">
        <div class="modal-container" @click.stop>
          <!-- Close button -->
          <button class="close-button" @click="handleClose" aria-label="닫기">
            <i class="fas fa-times"></i>
          </button>

          <!-- Video iframe -->
          <div class="video-wrapper">
            <iframe
              :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
              title="YouTube video player"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  show: Boolean,
  videoId: String
})

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}

// ESC key to close
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.show) {
    handleClose()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  background: #000;
  border-radius: 1rem;
  overflow: hidden;
}

.close-button {
  position: absolute;
  top: -3rem;
  right: 0;
  background: transparent;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 10;
  transition: transform 0.3s;
}

.close-button:hover {
  transform: scale(1.2);
}

.video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .close-button {
    top: -2.5rem;
    font-size: 1.5rem;
  }
}
</style>
