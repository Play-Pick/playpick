import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // State
  const theme = ref(getInitialTheme())

  // Getters
  const isDarkMode = computed(() => theme.value === 'dark')

  // 초기 테마 감지
  function getInitialTheme() {
    // 1. localStorage 확인
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      return savedTheme
    }

    // 2. 시스템 설정 확인
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }

    return 'light'
  }

  // Actions
  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    applyTheme()
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
    applyTheme()
  }

  const applyTheme = () => {
    // DOM에 적용
    if (theme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }

    // localStorage 동기화
    localStorage.setItem('theme', theme.value)
  }

  // 초기화
  const initialize = () => {
    applyTheme()

    // 시스템 테마 변경 감지
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      // 사용자가 수동으로 설정하지 않았을 경우에만 자동 전환
      if (!localStorage.getItem('theme')) {
        theme.value = e.matches ? 'dark' : 'light'
        applyTheme()
      }
    })
  }

  return {
    theme,
    isDarkMode,
    toggleTheme,
    setTheme,
    initialize
  }
})
