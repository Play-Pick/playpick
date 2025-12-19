<template>
  <div class="fab-container">
    <DarkModeToggle />
    <ScrollToTop />
  </div>
</template>

<script setup>
import DarkModeToggle from './DarkModeToggle.vue'
import ScrollToTop from './ScrollToTop.vue'
</script>

<style scoped>
.fab-container {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  z-index: 1000;
  display: flex;
  flex-direction: row;
  gap: 0.75rem;
  align-items: center;
}

@media (max-width: 768px) {
  .fab-container {
    right: 1rem;
    bottom: 1rem;
    gap: 0.5rem;
  }
}
</style>
