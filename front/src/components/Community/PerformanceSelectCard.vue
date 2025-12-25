<template>
  <div class="performance-select-card">
    <div v-if="performance" class="selected-performance">
      <img :src="performance.poster" alt="공연 포스터" class="performance-poster" />
      <div class="performance-details">
        <h3>{{ performance.prfnm }}</h3>
        <p>{{ performance.prfpdfrom }} ~ {{ performance.prfpdto }}</p>
        <button type="button" @click="$emit('clear')" class="btn-clear">
          <i class="fas fa-times"></i> 선택 해제
        </button>
      </div>
    </div>
    <div v-else class="no-performance">
      <i class="fas fa-theater-masks"></i>
      <p>공연을 선택하지 않았습니다</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  performance: {
    type: Object,
    default: null
  }
})

defineEmits(['clear'])
</script>

<style scoped>
.performance-select-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  transition: background 0.3s;
}

:root.dark .performance-select-card {
  background: #1a1a1a;
}

.selected-performance {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.performance-poster {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.performance-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.performance-details h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .performance-details h3 {
  color: #f3f4f6;
}

.performance-details p {
  color: #6b7280;
  font-size: 0.9375rem;
  transition: color 0.3s;
}

:root.dark .performance-details p {
  color: #9ca3af;
}

.btn-clear {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  align-self: flex-start;
}

.btn-clear:hover {
  background: #dc2626;
}

.no-performance {
  text-align: center;
  padding: 2rem;
  color: #9ca3af;
}

.no-performance i {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  display: block;
}

.no-performance p {
  font-size: 0.9375rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .selected-performance {
    flex-direction: column;
  }

  .performance-poster {
    align-self: center;
  }
}
</style>
