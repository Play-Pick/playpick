<template>
  <div class="article-form-fields">
    <!-- 제목 -->
    <div class="form-group">
      <label>제목</label>
      <input
        :value="title"
        @input="$emit('update:title', $event.target.value)"
        type="text"
        placeholder="제목을 입력하세요"
        required
        class="input-title"
      />
    </div>

    <!-- 별점 (조건부) -->
    <div v-if="showRating" class="form-group">
      <label>별점</label>
      <div class="rating-input">
        <button
          v-for="star in 5"
          :key="star"
          type="button"
          :class="['star', { active: star <= rating }]"
          @click="$emit('update:rating', star)"
        >
          <i :class="star <= rating ? 'fas fa-star' : 'far fa-star'"></i>
        </button>
        <span class="rating-value">{{ rating.toFixed(1) }}</span>
      </div>
    </div>

    <!-- 내용 -->
    <div class="form-group">
      <label>내용</label>
      <textarea
        :value="content"
        @input="$emit('update:content', $event.target.value)"
        placeholder="내용을 입력하세요"
        :rows="rows"
        required
        class="textarea-content"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  },
  rating: {
    type: Number,
    default: 5
  },
  showRating: {
    type: Boolean,
    default: false
  },
  rows: {
    type: Number,
    default: 12
  }
})

defineEmits(['update:title', 'update:content', 'update:rating'])
</script>

<style scoped>
.article-form-fields {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-weight: 700;
  font-size: 1.0625rem;
  color: #374151;
  transition: color 0.3s;
}

:root.dark .form-group label {
  color: #d1d5db;
}

/* 입력 필드 */
.input-title,
.textarea-content {
  padding: 0.875rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #111827;
}

:root.dark .input-title,
:root.dark .textarea-content {
  background: #1a1a1a;
  border-color: #374151;
  color: #f3f4f6;
}

.input-title:focus,
.textarea-content:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:root.dark .input-title:focus,
:root.dark .textarea-content:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.textarea-content {
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

/* 별점 입력 */
.rating-input {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.star {
  background: none;
  border: none;
  cursor: pointer;
  color: #d1d5db;
  font-size: 1.5rem;
  transition: all 0.2s;
}

.star:hover {
  transform: scale(1.1);
}

.star.active {
  color: #fbbf24;
}

.rating-value {
  margin-left: 0.5rem;
  font-weight: 700;
  color: #6366f1;
  font-size: 1.125rem;
  transition: color 0.3s;
}

:root.dark .rating-value {
  color: #c7d2fe;
}
</style>
