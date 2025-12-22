import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useWelcomeStore = defineStore('welcome', () => {
  // State
  const showWelcomeOverlay = ref(false)
  const welcomeData = ref(null)

  // Computed
  const shouldShowWelcome = computed(() => showWelcomeOverlay.value && welcomeData.value)

  // Actions
  const showWelcome = (data) => {
    console.log('[WelcomeStore] showWelcome called with data:', data)

    // Check if userId is valid
    const userId = data.userId
    if (!userId) {
      console.error('[WelcomeStore] userId is undefined or null! Cannot show welcome.')
      // Still show welcome, but use username as fallback for storage key
      const fallbackKey = `welcome_shown_${data.username || 'unknown'}`
      console.log('[WelcomeStore] Using fallback storage key:', fallbackKey)

      if (localStorage.getItem(fallbackKey)) {
        console.log('[WelcomeStore] Skipping welcome (already shown with fallback key)')
        return false
      }

      // Continue with fallback
      const topKeywords = extractTopKeywords(data.selectedPerformances || [])
      welcomeData.value = {
        username: data.username || data.displayName,
        userId: null,
        keywords: topKeywords
      }

      showWelcomeOverlay.value = true
      localStorage.setItem(fallbackKey, '1')
      return true
    }

    // Check if already shown using localStorage
    const storageKey = `welcome_shown_${userId}`

    console.log('[WelcomeStore] Checking localStorage key:', storageKey)
    const alreadyShown = localStorage.getItem(storageKey)
    console.log('[WelcomeStore] Already shown:', alreadyShown)

    if (alreadyShown) {
      // Already shown, skip
      console.log('[WelcomeStore] Skipping welcome (already shown)')
      return false
    }

    // Extract top genres and areas from selected performances
    const topKeywords = extractTopKeywords(data.selectedPerformances || [])
    console.log('[WelcomeStore] Top keywords extracted:', topKeywords)

    welcomeData.value = {
      username: data.username || data.displayName,
      userId: data.userId,
      keywords: topKeywords
    }

    console.log('[WelcomeStore] Welcome data set:', welcomeData.value)

    showWelcomeOverlay.value = true
    console.log('[WelcomeStore] Overlay visibility set to true')

    // Mark as shown
    localStorage.setItem(storageKey, '1')
    console.log('[WelcomeStore] Marked as shown in localStorage')

    return true
  }

  const hideWelcome = () => {
    showWelcomeOverlay.value = false
    // Keep data for a moment in case of animation
    setTimeout(() => {
      welcomeData.value = null
    }, 1000)
  }

  // Extract top 2-3 keywords from selected performances
  const extractTopKeywords = (performances) => {
    if (!performances || performances.length === 0) {
      return []
    }

    // Count genres
    const genreCounts = {}
    const areaCounts = {}

    performances.forEach(perf => {
      if (perf.genrenm) {
        genreCounts[perf.genrenm] = (genreCounts[perf.genrenm] || 0) + 1
      }
      if (perf.area) {
        areaCounts[perf.area] = (areaCounts[perf.area] || 0) + 1
      }
    })

    // Get top genres
    const topGenres = Object.entries(genreCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 2)
      .map(([genre]) => genre)

    // Get top area
    const topArea = Object.entries(areaCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 1)
      .map(([area]) => area)

    // Combine and limit to 3
    return [...topGenres, ...topArea].slice(0, 3)
  }

  const reset = () => {
    showWelcomeOverlay.value = false
    welcomeData.value = null
  }

  return {
    // State
    showWelcomeOverlay,
    welcomeData,

    // Computed
    shouldShowWelcome,

    // Actions
    showWelcome,
    hideWelcome,
    reset
  }
})
