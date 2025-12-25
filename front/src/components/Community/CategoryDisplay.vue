<template>
  <div class="category-display-wrapper">
    <div class="form-group">
      <label>{{ label }}</label>
      <div class="category-pill">
        <i :class="icon"></i>
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: '카테고리'
  },
  icon: {
    type: String,
    default: 'fas fa-pen'
  },
  text: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.category-display-wrapper {
  display: flex;
  flex-direction: column;
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

.category-pill {
  padding: 0.875rem 1.25rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.0625rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  align-self: flex-start;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s;
}

:root.dark .category-pill {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}
</style>
