import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import onboardingAPI from '@/api/onboarding'

export const useOnboardingStore = defineStore('onboarding', () => {
  // State
  const performances = ref([])
  const signals = ref({}) // {"PF123": 1.5, "PF456": -1.0, ...}
  const loading = ref(false)
  const error = ref(null)
  const completed = ref(false)

  // Computed
  const signalCount = computed(() => Object.keys(signals.value).length)
  const canComplete = computed(() => signalCount.value >= 8)
  const progress = computed(() => Math.min((signalCount.value / 8) * 100, 100))

  // Actions
  const fetchCandidates = async (strategy = 'balanced', excludeIds = null) => {
    loading.value = true
    error.value = null

    try {
      const response = await onboardingAPI.getCandidates(strategy, excludeIds)
      performances.value = response.data.performances || []
    } catch (err) {
      console.error('Failed to fetch onboarding candidates:', err)
      error.value = '공연 목록을 불러오는데 실패했습니다.'
      performances.value = []
    } finally {
      loading.value = false
    }
  }

  const refreshUnselectedCards = async (maxRefresh = 4) => {
    // Identify unselected cards
    const unselectedIds = performances.value
      .filter(perf => !signals.value[perf.mt20id])
      .map(perf => perf.mt20id)
      .slice(0, maxRefresh)

    if (unselectedIds.length === 0) {
      error.value = '교체할 수 있는 공연이 없습니다. (모두 선택됨)'
      return false
    }

    // Get all current performance IDs to exclude
    const currentIds = performances.value.map(perf => perf.mt20id)

    loading.value = true
    error.value = null

    try {
      const response = await onboardingAPI.getCandidates('balanced', currentIds)
      const newPerformances = response.data.performances || []

      if (newPerformances.length === 0) {
        error.value = '새로운 공연을 불러올 수 없습니다.'
        loading.value = false
        return false
      }

      // Replace unselected cards with new ones
      const replacementCount = Math.min(unselectedIds.length, newPerformances.length)
      const updatedPerformances = [...performances.value]

      for (let i = 0; i < replacementCount; i++) {
        const indexToReplace = updatedPerformances.findIndex(
          perf => perf.mt20id === unselectedIds[i]
        )
        if (indexToReplace !== -1) {
          updatedPerformances[indexToReplace] = newPerformances[i]
        }
      }

      performances.value = updatedPerformances
      return true
    } catch (err) {
      console.error('Failed to refresh cards:', err)
      error.value = '공연 교체에 실패했습니다.'
      return false
    } finally {
      loading.value = false
    }
  }

  const setSignal = (performanceId, signalValue) => {
    if (signalValue === 0) {
      // Remove neutral signals
      delete signals.value[performanceId]
    } else {
      signals.value[performanceId] = signalValue
    }
  }

  const saveSignals = async () => {
    if (signalCount.value < 8) {
      error.value = '최소 8개의 공연을 선택해주세요.'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const signalsArray = Object.entries(signals.value).map(([performance_id, signal]) => ({
        performance_id,
        signal
      }))

      await onboardingAPI.saveSignals(signalsArray)
      return true
    } catch (err) {
      console.error('Failed to save signals:', err)
      error.value = '선호도 저장에 실패했습니다.'
      return false
    } finally {
      loading.value = false
    }
  }

  const complete = async () => {
    loading.value = true
    error.value = null

    try {
      await onboardingAPI.completeOnboarding()
      completed.value = true
      return true
    } catch (err) {
      console.error('Failed to complete onboarding:', err)
      error.value = '온보딩 완료에 실패했습니다.'
      return false
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    performances.value = []
    signals.value = {}
    loading.value = false
    error.value = null
    completed.value = false
  }

  return {
    // State
    performances,
    signals,
    loading,
    error,
    completed,

    // Computed
    signalCount,
    canComplete,
    progress,

    // Actions
    fetchCandidates,
    refreshUnselectedCards,
    setSignal,
    saveSignals,
    complete,
    reset
  }
})
