import apiClient from './axios'

export default {
  /**
   * Get 16 performances for onboarding
   * @param {string} strategy - 'balanced', 'popular', or 'recent'
   * @param {Array|null} excludeIds - Array of mt20ids to exclude
   * @returns {Promise}
   */
  getCandidates(strategy = 'balanced', excludeIds = null) {
    const params = { strategy }

    // Add exclude parameter if provided
    if (excludeIds && excludeIds.length > 0) {
      params.exclude = excludeIds.join(',')
    }

    return apiClient.get('/accounts/onboarding/candidates/', { params })
  },

  /**
   * Save user reaction signals
   * @param {Array} signals - [{"performance_id": "PF123", "signal": 1.5}, ...]
   * @returns {Promise}
   */
  saveSignals(signals) {
    return apiClient.post('/accounts/onboarding/signals/', {
      signals
    })
  },

  /**
   * Complete onboarding process
   * @returns {Promise}
   */
  completeOnboarding() {
    return apiClient.post('/accounts/onboarding/complete/')
  }
}
