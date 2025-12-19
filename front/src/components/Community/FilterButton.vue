<template>
  <div class="filter-container">
    <button @click="toggleFilter" class="filter-button" :class="{ active: isOpen }">
      <span class="filter-icon">🔍</span>
      <span class="filter-text">필터</span>
      <span class="arrow" :class="{ open: isOpen }">▼</span>
    </button>

    <transition name="slide-fade">
      <div v-if="isOpen" class="filter-dropdown">
        <div class="filter-section">
          <h4>카테고리</h4>
          <div class="filter-options">
            <button
              v-for="category in categories"
              :key="category.value"
              @click="selectCategory(category.value)"
              class="filter-option"
              :class="{ selected: selectedCategory === category.value }"
            >
              {{ category.label }}
            </button>
          </div>
        </div>

        <div class="filter-actions">
          <button @click="resetFilter" class="reset-button">초기화</button>
          <button @click="applyFilter" class="apply-button">적용</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['filter'])

const isOpen = ref(false)
const selectedCategory = ref(null)

const categories = [
  { value: null, label: '전체' },
  { value: 'REVIEW', label: '후기' },
  { value: 'QNA', label: '질문' },
  { value: 'FREE', label: '자유게시판' },
  { value: 'INFO', label: '정보공유' },
  { value: 'EXPECT', label: '기대평' }
]

const toggleFilter = () => {
  isOpen.value = !isOpen.value
}

const selectCategory = (value) => {
  selectedCategory.value = value
}

const resetFilter = () => {
  selectedCategory.value = null
}

const applyFilter = () => {
  emit('filter', { category: selectedCategory.value })
  isOpen.value = false
}
</script>

<style scoped>
.filter-container {
  position: relative;
  display: inline-block;
}

.filter-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.filter-button:hover {
  border-color: #3498db;
  background-color: #f8f9fa;
}

.filter-button.active {
  border-color: #3498db;
  background-color: #e3f2fd;
}

.filter-icon {
  font-size: 1.1rem;
}

.filter-text {
  font-weight: 600;
  color: #2c3e50;
}

.arrow {
  font-size: 0.7rem;
  color: #666;
  transition: transform 0.2s;
}

.arrow.open {
  transform: rotate(180deg);
}

.filter-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  min-width: 280px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  z-index: 100;
}

.filter-section {
  margin-bottom: 1rem;
}

.filter-section h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-option {
  padding: 0.4rem 0.8rem;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.filter-option:hover {
  border-color: #3498db;
  background-color: #e3f2fd;
}

.filter-option.selected {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
  font-weight: 600;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.reset-button,
.apply-button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-button {
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.reset-button:hover {
  background-color: #e0e0e0;
}

.apply-button {
  background-color: #3498db;
  color: white;
}

.apply-button:hover {
  background-color: #2980b9;
}

/* 애니메이션 */
.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.15s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-5px);
  opacity: 0;
}
</style>
