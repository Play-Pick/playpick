import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import performanceAPI from '@/api/performances'

export const usePerformanceStore = defineStore('performance', () => {
  // State
  const performances = ref([])
  const currentPerformance = ref(null)
  const genres = ref([])
  const boxOfficeRankings = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const performanceCount = computed(() => performances.value.length)

  // Actions
  const fetchPerformances = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getPerformances(params)
      performances.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchPerformance = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getPerformance(id)
      currentPerformance.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchGenres = async () => {
    try {
      const response = await performanceAPI.getGenres()
      genres.value = response.data.genres
      return response.data.genres
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const fetchBoxOffice = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getBoxOffice(params)
      boxOfficeRankings.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchLatestBoxOfficeByGenre = async (genreCode) => {
    loading.value = true
    error.value = null
    try {
      const response = await performanceAPI.getLatestBoxOfficeByGenre(genreCode)
      boxOfficeRankings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    performances,
    currentPerformance,
    genres,
    boxOfficeRankings,
    loading,
    error,
    // Getters
    performanceCount,
    // Actions
    fetchPerformances,
    fetchPerformance,
    fetchGenres,
    fetchBoxOffice,
    fetchLatestBoxOfficeByGenre
  }
})
