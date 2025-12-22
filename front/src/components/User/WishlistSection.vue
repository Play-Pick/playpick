<template>
  <div class="wishlist-section">
    <div class="section-header">
      <h2>
        <i class="fas fa-heart"></i>
        찜한 공연
      </h2>
      <span class="count">{{ items.length }}</span>
    </div>

    <!-- 로딩 -->
    <div v-if="loading" class="loading-skeleton">
      <div v-for="n in 4" :key="n" class="skeleton-card"></div>
    </div>

    <!-- 에러 -->
    <div v-else-if="errorMessage" class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ errorMessage }}</p>
    </div>

    <!-- 빈 상태 -->
    <div v-else-if="items.length === 0" class="empty-state">
      <i class="fas fa-heart-broken"></i>
      <p>찜한 공연이 없습니다</p>
      <button @click="$emit('browse')" class="btn-browse">
        <i class="fas fa-search"></i> 공연 둘러보기
      </button>
    </div>

    <!-- 찜한 공연 그리드 -->
    <div v-else class="wishlist-grid">
      <div
        v-for="item in items"
        :key="item.mt20id"
        class="wishlist-card"
        @click="$emit('click-performance', item.mt20id)"
      >
        <div class="card-image">
          <img :src="item.poster || '/placeholder.png'" :alt="item.prfnm" />
          <button
            @click.stop="$emit('toggle-like', item.mt20id)"
            class="like-button active"
          >
            <i class="fas fa-heart"></i>
          </button>
        </div>
        <div class="card-content">
          <h3 class="card-title">{{ item.prfnm }}</h3>
          <p class="card-venue">
            <i class="fas fa-map-marker-alt"></i>
            {{ item.fcltynm }}
          </p>
          <p class="card-date">
            <i class="fas fa-calendar"></i>
            {{ item.prfpdfrom }} ~ {{ item.prfpdto }}
          </p>
          <p class="card-state" :class="getStateClass(item.prfstate)">
            {{ item.prfstate }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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
    default: ''
  }
})

defineEmits(['browse', 'click-performance', 'toggle-like'])

const getStateClass = (state) => {
  const stateMap = {
    '공연중': 'ongoing',
    '공연예정': 'upcoming',
    '공연완료': 'completed'
  }
  return stateMap[state] || ''
}
</script>

<style scoped>
.wishlist-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .wishlist-section {
  background: #1f2937;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .section-header {
  border-bottom-color: #374151;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  transition: color 0.3s;
}

:root.dark .section-header h2 {
  color: #f3f4f6;
}

.section-header h2 i {
  color: #ef4444;
  transition: color 0.3s;
}

:root.dark .section-header h2 i {
  color: #f87171;
}

.count {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;
}

:root.dark .count {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

/* 로딩 스켈레톤 */
.loading-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.skeleton-card {
  height: 300px;
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 8px;
}

:root.dark .skeleton-card {
  background: linear-gradient(90deg, #374151 25%, #4b5563 50%, #374151 75%);
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 에러 */
.error-message {
  text-align: center;
  padding: 2rem;
  color: #ef4444;
}

:root.dark .error-message {
  color: #f87171;
}

.error-message i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .empty-state {
  color: #6b7280;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state p {
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.btn-browse {
  padding: 0.75rem 2rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .btn-browse {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-browse:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* 찜한 공연 그리드 */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.wishlist-card {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  background: #f9fafb;
  transition: all 0.3s;
}

:root.dark .wishlist-card {
  background: #111827;
}

.wishlist-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  width: 100%;
  padding-top: 140%;
  overflow: hidden;
  background: #e5e7eb;
}

:root.dark .card-image {
  background: #374151;
}

.card-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.like-button {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: #d1d5db;
}

.like-button.active {
  color: #ef4444;
}

.like-button:hover {
  transform: scale(1.1);
  background: white;
}

.card-content {
  padding: 1rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  transition: color 0.3s;
}

:root.dark .card-title {
  color: #f3f4f6;
}

.card-venue,
.card-date {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0.25rem 0;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: color 0.3s;
}

:root.dark .card-venue,
:root.dark .card-date {
  color: #9ca3af;
}

.card-venue i,
.card-date i {
  font-size: 0.75rem;
  color: #9ca3af;
}

.card-state {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  display: inline-block;
  margin-top: 0.5rem;
}

.card-state.ongoing {
  background: #dcfce7;
  color: #166534;
}

:root.dark .card-state.ongoing {
  background: #14532d;
  color: #86efac;
}

.card-state.upcoming {
  background: #dbeafe;
  color: #1e40af;
}

:root.dark .card-state.upcoming {
  background: #1e3a8a;
  color: #93c5fd;
}

.card-state.completed {
  background: #f3f4f6;
  color: #6b7280;
}

:root.dark .card-state.completed {
  background: #374151;
  color: #9ca3af;
}

/* 반응형 */
@media (max-width: 768px) {
  .wishlist-section {
    padding: 1.5rem;
  }

  .wishlist-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>
