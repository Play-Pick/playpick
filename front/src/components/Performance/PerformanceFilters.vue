<template>
  <div class="filters">
    <select
      :value="selectedGenre"
      @change="handleGenreChange"
      class="filter-select"
    >
      <option value="">전체 장르</option>
      <option v-for="genre in genres" :key="genre" :value="genre">
        {{ genre }}
      </option>
    </select>

    <input
      :value="searchQuery"
      @input="handleSearchInput"
      type="text"
      placeholder="공연명 또는 장소 검색"
      class="filter-input"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  genres: {
    type: Array,
    default: () => []
  },
  selectedGenre: {
    type: String,
    default: ''
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:selectedGenre', 'update:searchQuery', 'filter'])

const handleGenreChange = (event) => {
  emit('update:selectedGenre', event.target.value)
  emit('filter')
}

const handleSearchInput = (event) => {
  emit('update:searchQuery', event.target.value)
  emit('filter')
}
</script>

<style scoped>
.filters {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
}

.filter-select,
.filter-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.3s;
  background: white;
  color: #111827;
}

:root.dark .filter-select,
:root.dark .filter-input {
  background: #2c2c2c;
  border-color: #374151;
  color: #f3f4f6;
}

.filter-select:hover,
.filter-input:hover {
  border-color: #9ca3af;
}

:root.dark .filter-select:hover,
:root.dark .filter-input:hover {
  border-color: #6b7280;
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .filter-select:focus,
:root.dark .filter-input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.filter-select {
  min-width: 150px;
  cursor: pointer;
}

.filter-input {
  flex: 1;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }
}
</style>
