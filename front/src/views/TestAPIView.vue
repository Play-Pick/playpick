<template>
  <div class="test-api">
    <h1>API 연결 테스트</h1>

    <div class="test-section">
      <h2>1. 직접 Fetch 테스트</h2>
      <button @click="testFetch">Fetch로 API 호출</button>
      <pre v-if="fetchResult">{{ fetchResult }}</pre>
      <pre v-if="fetchError" class="error">{{ fetchError }}</pre>
    </div>

    <div class="test-section">
      <h2>2. Axios 인스턴스 테스트</h2>
      <button @click="testAxios">Axios로 API 호출</button>
      <pre v-if="axiosResult">{{ axiosResult }}</pre>
      <pre v-if="axiosError" class="error">{{ axiosError }}</pre>
    </div>

    <div class="test-section">
      <h2>3. API 모듈 테스트</h2>
      <button @click="testAPI">API 모듈로 호출</button>
      <pre v-if="apiResult">{{ apiResult }}</pre>
      <pre v-if="apiError" class="error">{{ apiError }}</pre>
    </div>

    <div class="test-section">
      <h2>4. Pinia 스토어 테스트</h2>
      <button @click="testStore">스토어로 API 호출</button>
      <pre v-if="storeResult">{{ storeResult }}</pre>
      <pre v-if="storeError" class="error">{{ storeError }}</pre>
    </div>

    <div class="info-section">
      <h2>현재 환경 정보</h2>
      <ul>
        <li><strong>현재 URL:</strong> {{ currentURL }}</li>
        <li><strong>Origin:</strong> {{ origin }}</li>
        <li><strong>API Base URL:</strong> http://127.0.0.1:8000/api</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import apiClient from '@/api/axios'
import performanceAPI from '@/api/performances'
import { usePerformanceStore } from '@/stores/performanceStore'

const performanceStore = usePerformanceStore()

// Fetch 테스트
const fetchResult = ref(null)
const fetchError = ref(null)

const testFetch = async () => {
  fetchResult.value = null
  fetchError.value = null

  try {
    console.log('Fetch 테스트 시작...')
    const response = await fetch('http://127.0.0.1:8000/api/performances/genres/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // CORS credentials
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    fetchResult.value = JSON.stringify(data, null, 2)
    console.log('✅ Fetch 성공:', data)
  } catch (err) {
    fetchError.value = err.message
    console.error('❌ Fetch 실패:', err)
  }
}

// Axios 인스턴스 테스트
const axiosResult = ref(null)
const axiosError = ref(null)

const testAxios = async () => {
  axiosResult.value = null
  axiosError.value = null

  try {
    console.log('Axios 테스트 시작...')
    const response = await apiClient.get('/performances/genres/')
    axiosResult.value = JSON.stringify(response.data, null, 2)
    console.log('✅ Axios 성공:', response.data)
  } catch (err) {
    axiosError.value = `${err.message}\n\n상세: ${JSON.stringify(err.response?.data || err, null, 2)}`
    console.error('❌ Axios 실패:', err)
    console.error('에러 상세:', err.response)
  }
}

// API 모듈 테스트
const apiResult = ref(null)
const apiError = ref(null)

const testAPI = async () => {
  apiResult.value = null
  apiError.value = null

  try {
    console.log('API 모듈 테스트 시작...')
    const response = await performanceAPI.getGenres()
    apiResult.value = JSON.stringify(response.data, null, 2)
    console.log('✅ API 모듈 성공:', response.data)
  } catch (err) {
    apiError.value = `${err.message}\n\n상세: ${JSON.stringify(err.response?.data || err, null, 2)}`
    console.error('❌ API 모듈 실패:', err)
  }
}

// Pinia 스토어 테스트
const storeResult = ref(null)
const storeError = ref(null)

const testStore = async () => {
  storeResult.value = null
  storeError.value = null

  try {
    console.log('Pinia 스토어 테스트 시작...')
    await performanceStore.fetchGenres()
    storeResult.value = JSON.stringify(performanceStore.genres, null, 2)
    console.log('✅ Pinia 스토어 성공:', performanceStore.genres)
  } catch (err) {
    storeError.value = `${err.message}\n\n상세: ${JSON.stringify(err.response?.data || err, null, 2)}`
    console.error('❌ Pinia 스토어 실패:', err)
  }
}

// 현재 환경 정보
const currentURL = computed(() => window.location.href)
const origin = computed(() => window.location.origin)
</script>

<style scoped>
.test-api {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.test-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.test-section h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.test-section button {
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.test-section button:hover {
  background-color: #359268;
}

pre {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.875rem;
}

.error {
  background-color: #fee;
  color: #c00;
  border: 1px solid #fcc;
}

.info-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #e8f5e9;
  border-radius: 8px;
}

.info-section h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.info-section ul {
  list-style: none;
  padding: 0;
}

.info-section li {
  margin: 0.5rem 0;
  font-size: 0.875rem;
}

.info-section strong {
  color: #2c3e50;
}
</style>
