<template>
  <div class="genre-tabs-container">
    <div class="genre-tabs">
      <button
        v-for="genre in genres"
        :key="genre.code"
        @click="onClick(genre.code)"
        :class="['genre-tab', { active: currentGenre === genre.code }]"
      >
        {{ genre.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  genres: {
    type: Array,
    required: true
  },
  currentGenre: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['change'])

const onClick = (genreCode) => {
  emit('change', genreCode)
}
</script>

<style scoped>
/* 장르 탭 */
.genre-tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.genre-tabs {
  display: inline-flex;
  background: white;
  border-radius: 9999px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  gap: 0.5rem;
}

.genre-tab {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  background: none;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.genre-tab:hover {
  background: #f3f4f6;
  color: #111827;
}

.genre-tab.active {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

/* 반응형 */
@media (max-width: 768px) {
  .genre-tabs {
    flex-wrap: wrap;
  }
}
</style>
