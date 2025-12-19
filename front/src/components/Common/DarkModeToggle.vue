<template>
  <button
    @click="toggleDarkMode"
    class="fab-button dark-mode-toggle"
    :aria-label="isDarkMode ? '라이트 모드로 전환' : '다크 모드로 전환'"
  >
    <i :class="isDarkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/themeStore'

const themeStore = useThemeStore()

const isDarkMode = computed(() => themeStore.isDarkMode)

const toggleDarkMode = () => {
  themeStore.toggleTheme()
}
</script>

<style scoped>
.fab-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: all 0.3s;
}

.fab-button:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.4);
}

/* 다크모드 시 버튼 색상 변경 */
:root.dark .dark-mode-toggle {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

/* 반응형 */
@media (max-width: 768px) {
  .fab-button {
    width: 2rem;
    height: 2rem;
    font-size: 0.875rem;
  }
}
</style>
