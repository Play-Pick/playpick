<template>
  <div v-if="show" class="map-modal" @click="emit('close')">
    <div class="map-modal-content" @click.stop>
      <div class="modal-header">
        <h3>
          <i class="fas fa-map-marker-alt"></i>
          {{ venueName }}
        </h3>
        <button @click="emit('close')" class="close-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div id="map" class="map-container"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  venueName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])
</script>

<style scoped>
.map-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.map-modal-content {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 1.25rem;
  color: #111827;
  margin: 0;
}

.modal-header h3 i {
  color: #6366f1;
  margin-right: 0.5rem;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #111827;
}

.map-container {
  width: 100%;
  height: 500px;
}

@media (max-width: 768px) {
  .map-container {
    height: 400px;
  }
}
</style>
