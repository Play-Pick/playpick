import apiClient from './axios'

export default {
  /**
   * Get playlist videos for main page
   * @returns {Promise} Response with videos array
   */
  getPlaylistVideos() {
    return apiClient.get('/performances/youtube/playlist/')
  },

  /**
   * Get performance-related video
   * @param {string|number} performanceId - Performance database ID
   * @returns {Promise} Response with video data or fallback
   */
  getPerformanceVideo(performanceId) {
    return apiClient.get(`/performances/${performanceId}/youtube/`)
  }
}
