<template>
  <div class="watched-section">
    <div class="watched-header">
      <h2>관람한 공연</h2>
      <span class="watched-count">{{ items.length }}</span>
    </div>

    <div v-if="errorMessage" class="watched-alert">
      <i class="fas fa-exclamation-circle"></i>
      <span>{{ errorMessage }}</span>
    </div>

    <div v-if="loading" class="watched-loading">
      <div class="watched-skeleton">
        <div v-for="n in 4" :key="n" class="skeleton-card"></div>
      </div>
      <p>불러오는 중...</p>
    </div>

    <div v-else-if="items.length === 0" class="watched-empty">
      <i class="fas fa-check-circle"></i>
      <p>아직 관람한 공연이 없어요</p>
      <p class="watched-empty-hint">공연 상세에서 '봤어요'를 눌러 기록해보세요</p>
      <button class="watched-browse-btn" @click="$emit('browse')">
        공연 둘러보기
      </button>
    </div>

    <div v-else class="watched-grid">
      <PerformanceCard
        v-for="item in items"
        :key="item.mt20id || item.id"
        :performance="item"
        @click="$emit('click-performance', $event)"
        @toggle-like="$emit('toggle-like', $event)"
      >
        <template #actions>
          <button @click.stop="$emit('remove', item.mt20id || item.id)"
                  class="remove-watched-btn"
                  title="관람 해제">
            <i class="fas fa-times"></i>
          </button>
        </template>
      </PerformanceCard>
    </div>
  </div>
</template>

<script setup>
import PerformanceCard from '@/components/Performance/PerformanceCard.vue'

defineProps({
  items: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: null
  }
})

defineEmits(['browse', 'click-performance', 'remove', 'toggle-like'])
</script>

<style scoped>
.watched-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
  transition: background-color 0.3s, border-color 0.3s, box-shadow 0.3s;
}

:root.dark .watched-section {
  background: #1f2937;
  border-color: #374151;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.watched-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.watched-header h2 {
  font-size: 1.5rem;
  color: #0f172a;
  transition: color 0.3s;
}

:root.dark .watched-header h2 {
  color: #f3f4f6;
}

.watched-count {
  background: #6366f1;
  color: white;
  font-weight: 700;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

:root.dark .watched-count {
  background: #818cf8;
}

.watched-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #6366f1;
  color: #0f172a;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}

:root.dark .watched-alert {
  background: #111827;
  border-color: #374151;
  border-left-color: #818cf8;
  color: #f3f4f6;
}

.watched-loading {
  text-align: center;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .watched-loading {
  color: #9ca3af;
}

.watched-skeleton {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.skeleton-card {
  aspect-ratio: 3/4;
  background: linear-gradient(120deg, #e2e8f0 30%, #f1f5f9 50%, #e2e8f0 70%);
  background-size: 200% 100%;
  animation: shimmer 1.4s ease infinite;
  border-radius: 0.75rem;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.watched-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #64748b;
  transition: color 0.3s;
}

:root.dark .watched-empty {
  color: #9ca3af;
}

.watched-empty i {
  font-size: 2.5rem;
  color: #6366f1;
  margin-bottom: 0.75rem;
  transition: color 0.3s;
}

:root.dark .watched-empty i {
  color: #818cf8;
}

.watched-empty-hint {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

:root.dark .watched-empty-hint {
  color: #6b7280;
}

.watched-browse-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  border-radius: 9999px;
  border: none;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.watched-browse-btn:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  transform: translateY(-1px);
}

.watched-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.25rem;
}

.remove-watched-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s;
  z-index: 10;
}

.watched-grid :deep(.performance-card):hover .remove-watched-btn {
  opacity: 1;
}

.remove-watched-btn:hover {
  background: rgba(220, 38, 38, 1);
  transform: scale(1.1);
}

/* 반응형 */
@media (max-width: 1024px) {
  .watched-skeleton,
  .watched-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .watched-skeleton,
  .watched-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style>
