import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import userAPI from '@/api/users'

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref(null)
  const users = ref([])
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const userId = computed(() => currentUser.value?.id)
  const username = computed(() => currentUser.value?.username)

  // Actions
  const fetchCurrentUser = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await userAPI.getCurrentUser()
      currentUser.value = response.data
      isAuthenticated.value = true
      return response.data
    } catch (err) {
      error.value = err.message
      isAuthenticated.value = false
      currentUser.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await userAPI.getUsers()
      users.value = response.data.results || response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchUser = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await userAPI.getUser(id)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const followUser = async (id) => {
    try {
      const response = await userAPI.followUser(id)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
  }

  return {
    // State
    currentUser,
    users,
    isAuthenticated,
    loading,
    error,
    // Getters
    userId,
    username,
    // Actions
    fetchCurrentUser,
    fetchUsers,
    fetchUser,
    followUser,
    logout
  }
})
