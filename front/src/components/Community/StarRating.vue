<template>
  <div class="star-rating">
    <div
      v-for="n in 5"
      :key="n"
      class="star-wrapper"
      @mousemove="handleStarHover($event, n)"
      @mouseleave="hoverRating = 0"
      @click="handleStarClick($event, n)"
    >
      <i
        class="fas fa-star star-full"
        :class="{ active: n <= (hoverRating || modelValue) }"
      ></i>
      <i
        class="fas fa-star-half-alt star-half"
        :class="{ active: n - 0.5 === (hoverRating || modelValue) }"
      ></i>
    </div>
    <span class="rating-text">{{ modelValue }}점</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['update:modelValue'])

const hoverRating = ref(0)

// 별점 호버 처리 (0.5 단위)
const handleStarHover = (event, starNumber) => {
  const target = event.currentTarget
  const rect = target.getBoundingClientRect()
  const x = event.clientX - rect.left
  const halfWidth = rect.width / 2

  if (x < halfWidth) {
    hoverRating.value = starNumber - 0.5
  } else {
    hoverRating.value = starNumber
  }
}

// 별점 클릭 처리 (0.5 단위)
const handleStarClick = (event, starNumber) => {
  const target = event.currentTarget
  const rect = target.getBoundingClientRect()
  const x = event.clientX - rect.left
  const halfWidth = rect.width / 2

  const newRating = x < halfWidth ? starNumber - 0.5 : starNumber
  emit('update:modelValue', newRating)
}
</script>

<style scoped>
.star-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.star-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.star-wrapper i {
  font-size: 2.5rem;
  transition: all 0.2s;
}

.star-full {
  color: #d1d5db;
  transition: color 0.3s;
}

:root.dark .star-full {
  color: #4b5563;
}

.star-full.active {
  color: #fbbf24;
}

.star-half {
  position: absolute;
  left: 0;
  top: 0;
  color: transparent;
  overflow: hidden;
  width: 50%;
}

.star-half.active {
  color: #fbbf24;
}

.star-wrapper:hover .star-full,
.star-wrapper:hover .star-half {
  transform: scale(1.15);
}

.rating-text {
  margin-left: 0.75rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: #6366f1;
  transition: color 0.3s;
}

:root.dark .rating-text {
  color: #818cf8;
}
</style>
