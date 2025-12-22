import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import onboardingAPI from '@/api/onboarding'

export const useOnboardingStore = defineStore('onboarding', () => {
  // State - Tinder-style single card navigation
  const candidates = ref([])        // All available performances
  const currentIndex = ref(0)       // Current card index
  const likes = ref([])             // mt20ids that user liked (1.5)
  const dislikes = ref([])          // mt20ids that user disliked (-1.0)
  const skips = ref([])             // mt20ids that user skipped (0)
  const loading = ref(false)
  const error = ref(null)
  const completed = ref(false)

  // Computed
  const currentCard = computed(() => candidates.value[currentIndex.value] || null)
  const hasMore = computed(() => currentIndex.value < candidates.value.length - 1)
  const likeCount = computed(() => likes.value.length)
  const canComplete = computed(() => likeCount.value >= 8)
  const progress = computed(() => Math.min((likeCount.value / 8) * 100, 100))
  const totalResponses = computed(() => likes.value.length + dislikes.value.length + skips.value.length)

  const advanceCard = () => {
    // Move to next card; if we're at the end, advance past the last item
    // so the UI can show the completion state or load more cards.
    if (hasMore.value) {
      currentIndex.value++
    } else {
      currentIndex.value = candidates.value.length
    }
  }

  // Actions
  const fetchCandidates = async (strategy = 'balanced', excludeIds = null) => {
    loading.value = true
    error.value = null

    try {
      const response = await onboardingAPI.getCandidates(strategy, excludeIds)
      candidates.value = response.data.performances || []
      currentIndex.value = 0
    } catch (err) {
      console.error('Failed to fetch onboarding candidates:', err)
      error.value = '공연 목록을 불러오는데 실패했습니다.'
      candidates.value = []
    } finally {
      loading.value = false
    }
  }

  // Load more candidates when running out
  const loadMoreCandidates = async (strategy = 'balanced') => {
    // Get all current mt20ids to exclude
    const allCurrentIds = candidates.value.map(p => p.mt20id)

    try {
      const response = await onboardingAPI.getCandidates(strategy, allCurrentIds)
      const newPerformances = response.data.performances || []

      if (newPerformances.length > 0) {
        // Append new performances to existing candidates
        candidates.value = [...candidates.value, ...newPerformances]
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to load more candidates:', err)
      return false
    }
  }

  const chooseLike = () => {
    if (!currentCard.value) return false

    const mt20id = currentCard.value.mt20id

    // Remove from other arrays if exists
    dislikes.value = dislikes.value.filter(id => id !== mt20id)
    skips.value = skips.value.filter(id => id !== mt20id)

    // Add to likes if not already there
    if (!likes.value.includes(mt20id)) {
      likes.value.push(mt20id)
    }

    advanceCard()

    return true
  }

  const chooseDislike = () => {
    if (!currentCard.value) return false

    const mt20id = currentCard.value.mt20id

    // Remove from other arrays if exists
    likes.value = likes.value.filter(id => id !== mt20id)
    skips.value = skips.value.filter(id => id !== mt20id)

    // Add to dislikes if not already there
    if (!dislikes.value.includes(mt20id)) {
      dislikes.value.push(mt20id)
    }

    advanceCard()

    return true
  }

  const chooseSkip = () => {
    if (!currentCard.value) return false

    const mt20id = currentCard.value.mt20id

    // Remove from other arrays if exists
    likes.value = likes.value.filter(id => id !== mt20id)
    dislikes.value = dislikes.value.filter(id => id !== mt20id)

    // Add to skips if not already there
    if (!skips.value.includes(mt20id)) {
      skips.value.push(mt20id)
    }

    advanceCard()

    return true
  }

  const submit = async () => {
    if (likeCount.value < 8) {
      error.value = '최소 8개의 공연을 "보고싶어요"로 선택해주세요.'
      return false
    }

    loading.value = true
    error.value = null

    try {
      // Convert to signals format expected by backend
      const signalsArray = []

      likes.value.forEach(mt20id => {
        signalsArray.push({ performance_id: mt20id, signal: 1.5 })
      })

      dislikes.value.forEach(mt20id => {
        signalsArray.push({ performance_id: mt20id, signal: -1.0 })
      })

      // Skips are not sent (neutral = 0, backend ignores)
      // skips.value.forEach(mt20id => {
      //   signalsArray.push({ performance_id: mt20id, signal: 0 })
      // })

      // Save signals
      await onboardingAPI.saveSignals(signalsArray)

      // Complete onboarding
      await onboardingAPI.completeOnboarding()

      completed.value = true
      return true
    } catch (err) {
      console.error('Failed to submit onboarding:', err)
      error.value = '온보딩 완료에 실패했습니다. 다시 시도해주세요.'
      return false
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    candidates.value = []
    currentIndex.value = 0
    likes.value = []
    dislikes.value = []
    skips.value = []
    loading.value = false
    error.value = null
    completed.value = false
  }

  return {
    // State
    candidates,
    currentIndex,
    likes,
    dislikes,
    skips,
    loading,
    error,
    completed,

    // Computed
    currentCard,
    hasMore,
    likeCount,
    canComplete,
    progress,
    totalResponses,

    // Actions
    fetchCandidates,
    loadMoreCandidates,
    chooseLike,
    chooseDislike,
    chooseSkip,
    submit,
    reset
  }
})
