<template>
  <div class="preference-form">
    <div class="form-group">
      <label>선호 장르 선택</label>
      <div class="genre-grid">
        <label
          v-for="genre in availableGenres"
          :key="genre.code"
          class="genre-checkbox"
        >
          <input
            type="checkbox"
            :value="genre.name"
            :checked="modelValue.includes(genre.name)"
            @change="toggleGenre(genre.name)"
          />
          <span class="genre-label">{{ genre.name }}</span>
        </label>
      </div>
      <span class="field-help">
        <i class="fas fa-info-circle"></i>
        선호하는 장르를 선택해주세요 (중복 선택 가능)
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

// 사용 가능한 장르 목록
const availableGenres = [
  { code: 'BBBC', name: '뮤지컬' },
  { code: 'AAAA', name: '연극' },
  { code: 'CCCA', name: '클래식' },
  { code: 'CCCC', name: '오페라' },
  { code: 'CCCD', name: '무용' },
  { code: 'EEEA', name: '복합' },
  { code: 'EEEB', name: '서커스/마술' },
  { code: 'GGGA', name: '대중음악' },
  { code: 'KID', name: '아동' },
]

const toggleGenre = (genreName) => {
  const newValue = [...props.modelValue]
  const index = newValue.indexOf(genreName)

  if (index > -1) {
    newValue.splice(index, 1)
  } else {
    newValue.push(genreName)
  }

  emit('update:modelValue', newValue)
}
</script>

<style scoped>
.preference-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #e5e7eb;
}

.genre-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.genre-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

:root.dark .genre-checkbox {
  background: #374151;
  border-color: #4b5563;
}

.genre-checkbox:hover {
  border-color: #6366f1;
  background: #f9fafb;
}

:root.dark .genre-checkbox:hover {
  border-color: #818cf8;
  background: #4b5563;
}

.genre-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #6366f1;
}

.genre-checkbox input[type="checkbox"]:checked + .genre-label {
  color: #6366f1;
  font-weight: 600;
}

:root.dark .genre-checkbox input[type="checkbox"]:checked + .genre-label {
  color: #818cf8;
}

.genre-label {
  font-size: 0.875rem;
  color: #374151;
  transition: all 0.3s;
}

:root.dark .genre-label {
  color: #e5e7eb;
}

.field-help {
  color: #6b7280;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

:root.dark .field-help {
  color: #9ca3af;
}

.field-help i {
  color: #9ca3af;
  transition: color 0.3s;
}

:root.dark .field-help i {
  color: #6b7280;
}

@media (max-width: 640px) {
  .genre-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
