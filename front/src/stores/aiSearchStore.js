import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import performanceAPI from '@/api/performances'

const STORAGE_KEY = 'ai_search_state'

// localStorage에서 이전 검색 상태 복원
const loadSavedState = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      return JSON.parse(saved)
    }
  } catch (e) {
    console.error('Failed to load saved search state:', e)
  }
  return null
}

export const useAISearchStore = defineStore('aiSearch', () => {
  // 저장된 상태 불러오기
  const savedState = loadSavedState()

  // State
  const searchResults = ref(savedState?.searchResults || [])
  const aiComment = ref(savedState?.aiComment || '')
  const loading = ref(false)
  const error = ref(null)
  const lastQuery = ref(savedState?.lastQuery || '')

  // Actions
  const searchPerformances = async (query) => {
    if (!query || !query.trim()) {
      error.value = '검색어를 입력해주세요.'
      return
    }

    loading.value = true
    error.value = null
    lastQuery.value = query

    try {
      const response = await performanceAPI.aiSearch(query)

      if (response.data.success) {
        searchResults.value = response.data.results
        aiComment.value = response.data.ai_comment
      } else {
        error.value = response.data.message || '검색 중 오류가 발생했습니다.'
        searchResults.value = []
        aiComment.value = ''
      }

      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '검색 중 오류가 발생했습니다.'
      searchResults.value = []
      aiComment.value = ''
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearResults = () => {
    searchResults.value = []
    aiComment.value = ''
    error.value = null
    lastQuery.value = ''
  }

  // localStorage에 상태 저장 (검색 결과가 변경될 때마다)
  const saveState = () => {
    try {
      const state = {
        searchResults: searchResults.value,
        aiComment: aiComment.value,
        lastQuery: lastQuery.value
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
    } catch (e) {
      console.error('Failed to save search state:', e)
    }
  }

  // 상태 변경 감지 및 자동 저장
  watch([searchResults, aiComment, lastQuery], () => {
    saveState()
  }, { deep: true })

  return {
    // State
    searchResults,
    aiComment,
    loading,
    error,
    lastQuery,
    // Actions
    searchPerformances,
    clearResults
  }
})
