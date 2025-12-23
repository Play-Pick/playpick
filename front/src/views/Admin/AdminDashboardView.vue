<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1><i class="fas fa-cogs"></i> 관리자 대시보드</h1>
      <p class="subtitle">KOPIS 데이터 수집 및 관리</p>
    </div>

    <!-- 데이터 통계 -->
    <div class="stats-section">
      <h2><i class="fas fa-chart-bar"></i> 데이터 통계</h2>
      <div class="stats-grid" v-if="stats">
        <div class="stat-card">
          <div class="stat-icon performances">
            <i class="fas fa-theater-masks"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.performances?.total?.toLocaleString() }}</div>
            <div class="stat-label">전체 공연</div>
            <div class="stat-detail">
              상세정보: {{ stats.performances?.with_detail?.toLocaleString() }}건
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon boxoffice">
            <i class="fas fa-trophy"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.boxoffice?.total?.toLocaleString() }}</div>
            <div class="stat-label">박스오피스 랭킹</div>
            <div class="stat-detail">
              최신: {{ stats.boxoffice?.latest_date || 'N/A' }}
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon ongoing">
            <i class="fas fa-play-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.performances?.ongoing?.toLocaleString() }}</div>
            <div class="stat-label">공연 중</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon missing">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.performances?.without_detail?.toLocaleString() }}</div>
            <div class="stat-label">상세정보 없음</div>
          </div>
        </div>
      </div>
      <button @click="loadStats" class="btn-refresh" :disabled="loading">
        <i class="fas fa-sync-alt" :class="{ spinning: loading }"></i>
        새로고침
      </button>
    </div>

    <!-- 데이터 수집 액션 -->
    <div class="actions-section">
      <h2><i class="fas fa-download"></i> 데이터 수집</h2>

      <div class="action-cards">
        <!-- 박스오피스 수집 -->
        <div class="action-card">
          <div class="action-header">
            <i class="fas fa-trophy"></i>
            <h3>박스오피스 랭킹</h3>
          </div>
          <p class="action-desc">KOPIS API에서 최신 박스오피스 랭킹 데이터를 수집합니다.</p>
          <button
            @click="collectBoxOffice"
            :disabled="loading"
            class="btn-action primary"
          >
            <i class="fas fa-download"></i>
            박스오피스 수집
          </button>
        </div>

        <!-- 공연 정보 수집 -->
        <div class="action-card">
          <div class="action-header">
            <i class="fas fa-theater-masks"></i>
            <h3>공연 정보</h3>
          </div>
          <p class="action-desc">최근 1개월간의 공연 정보를 수집합니다.</p>
          <button
            @click="collectPerformances"
            :disabled="loading"
            class="btn-action success"
          >
            <i class="fas fa-download"></i>
            공연 정보 수집
          </button>
        </div>

        <!-- 상세 정보 수집 -->
        <div class="action-card">
          <div class="action-header">
            <i class="fas fa-info-circle"></i>
            <h3>공연 상세 정보</h3>
          </div>
          <p class="action-desc">상세 정보가 없는 공연의 상세 정보를 수집합니다 (최대 100건).</p>
          <button
            @click="collectDetails"
            :disabled="loading"
            class="btn-action info"
          >
            <i class="fas fa-download"></i>
            상세 정보 수집 (100건)
          </button>
        </div>

        <!-- 상세 정보 전체 수집 -->
        <div class="action-card">
          <div class="action-header">
            <i class="fas fa-sync"></i>
            <h3>상세 정보 전체 수집</h3>
          </div>
          <p class="action-desc">상세 정보가 없는 모든 공연을 100건씩 반복 수집합니다.</p>
          <button
            @click="collectAllDetails"
            :disabled="loading"
            class="btn-action info"
          >
            <i class="fas fa-sync"></i>
            전체 상세 정보 수집
          </button>
        </div>

        <!-- 테스트 데이터 생성 -->
        <div class="action-card">
          <div class="action-header">
            <i class="fas fa-flask"></i>
            <h3>테스트 데이터</h3>
          </div>
          <p class="action-desc">DB 내 공연 데이터로 테스트용 박스오피스 랭킹을 생성합니다.</p>
          <button
            @click="createTestBoxOffice"
            :disabled="loading"
            class="btn-action warning"
          >
            <i class="fas fa-flask"></i>
            테스트 데이터 생성
          </button>
        </div>
      </div>
    </div>

    <!-- 로그 출력 -->
    <div v-if="logs.length > 0" class="logs-section">
      <h2><i class="fas fa-terminal"></i> 실행 로그</h2>
      <div class="logs-container">
        <div
          v-for="(log, index) in logs"
          :key="index"
          :class="['log-entry', log.type]"
        >
          <div class="log-header">
            <span class="log-time">{{ log.time }}</span>
            <span :class="['log-status', log.type]">
              <i :class="getLogIcon(log.type)"></i>
              {{ log.type.toUpperCase() }}
            </span>
          </div>
          <div class="log-message">{{ log.message }}</div>
          <pre v-if="log.output" class="log-output">{{ log.output }}</pre>
        </div>
      </div>
      <button @click="clearLogs" class="btn-clear-logs">
        <i class="fas fa-trash"></i> 로그 지우기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import adminAPI from '@/api/admin'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref(null)
const loading = ref(false)
const logs = ref([])

// 관리자 권한 확인
onMounted(async () => {
  if (!authStore.isAdmin) {
    alert('관리자만 접근할 수 있습니다.')
    router.push('/')
    return
  }

  await loadStats()
})

const loadStats = async () => {
  try {
    loading.value = true
    const response = await adminAPI.getStats()
    stats.value = response.data.data
  } catch (error) {
    console.error('통계 로드 실패:', error)
    addLog('error', '통계 로드 실패', error.response?.data?.message || error.message)
  } finally {
    loading.value = false
  }
}

const collectBoxOffice = async () => {
  if (!confirm('박스오피스 데이터를 수집하시겠습니까?')) return

  try {
    loading.value = true
    addLog('info', '박스오피스 데이터 수집 시작...')

    const response = await adminAPI.collectBoxOffice()

    if (response.data.success) {
      const collected = response.data.data?.collected || 0
      const total = response.data.data?.total || 0
      addLog('success', `박스오피스 데이터 수집 완료 (${collected}건 수집, 전체: ${total}건)`, response.data.output)
      await loadStats()
    } else {
      const errorDetail = response.data.error_detail || response.data.output
      addLog('error', response.data.message, errorDetail)
    }
  } catch (error) {
    console.error('박스오피스 수집 실패:', error)
    const errorMsg = error.response?.data?.error_detail || error.response?.data?.message || error.message
    addLog('error', '박스오피스 수집 실패', errorMsg)
  } finally {
    loading.value = false
  }
}

const collectPerformances = async () => {
  if (!confirm('공연 정보를 수집하시겠습니까? (최근 1개월)')) return

  try {
    loading.value = true
    addLog('info', '공연 정보 수집 시작... (최근 1개월)')

    const response = await adminAPI.collectPerformances()

    if (response.data.success) {
      addLog('success', response.data.message, response.data.output)
      await loadStats()
    } else {
      addLog('error', response.data.message, response.data.output)
    }
  } catch (error) {
    console.error('공연 정보 수집 실패:', error)
    addLog('error', '공연 정보 수집 실패', error.response?.data?.message || error.message)
  } finally {
    loading.value = false
  }
}

const collectDetails = async () => {
  if (!confirm('공연 상세 정보를 수집하시겠습니까? (최대 100건)')) return

  try {
    loading.value = true
    addLog('info', '공연 상세 정보 수집 시작... (최대 100건)')

    const response = await adminAPI.collectDetails()

    if (response.data.success) {
      addLog('success', response.data.message, response.data.output)
      await loadStats()
    } else {
      addLog('error', response.data.message, response.data.output)
    }
  } catch (error) {
    console.error('상세 정보 수집 실패:', error)
    addLog('error', '상세 정보 수집 실패', error.response?.data?.message || error.message)
  } finally {
    loading.value = false
  }
}

const collectAllDetails = async () => {
  if (!confirm('상세 정보가 없는 모든 공연을 수집하시겠습니까?\n(100건씩 반복 수집합니다. 시간이 오래 걸릴 수 있습니다)')) return

  try {
    loading.value = true
    let round = 1
    let totalCollected = 0
    let hasMore = true

    addLog('info', '전체 공연 상세 정보 수집 시작... (100건씩 반복)')

    while (hasMore) {
      addLog('info', `[${round}차 수집] 상세 정보 수집 중... (최대 100건)`)

      const response = await adminAPI.collectDetails()

      if (response.data.success) {
        const collected = response.data.data?.collected || 0
        const remaining = response.data.data?.remaining || 0
        const output = response.data.output || ''

        totalCollected += collected

        addLog('success', `[${round}차 완료] ${collected}건 수집 완료 (남은 공연: ${remaining}건)`, output)

        // 수집된 건수가 0이거나 남은 공연이 없으면 종료
        if (collected === 0 || remaining === 0) {
          hasMore = false
          addLog('success', `전체 수집 완료! 총 ${totalCollected}건 수집됨 (${round}차 반복)`)
        } else {
          round++
          // 잠시 대기 (API 부하 방지)
          addLog('info', `2초 대기 후 ${round}차 수집 시작...`)
          await new Promise(resolve => setTimeout(resolve, 2000))
        }
      } else {
        addLog('error', `[${round}차 실패] ${response.data.message}`, response.data.output)
        hasMore = false
      }
    }

    await loadStats()
  } catch (error) {
    console.error('전체 상세 정보 수집 실패:', error)
    addLog('error', '전체 상세 정보 수집 실패', error.response?.data?.message || error.message)
  } finally {
    loading.value = false
  }
}

const createTestBoxOffice = async () => {
  if (!confirm('테스트 박스오피스 데이터를 생성하시겠습니까?\n(기존 오늘 날짜 데이터는 삭제됩니다)')) return

  try {
    loading.value = true
    addLog('info', '테스트 박스오피스 데이터 생성 시작...')

    const response = await adminAPI.createTestBoxOffice()

    if (response.data.success) {
      const data = response.data.data
      addLog(
        'success',
        response.data.message,
        `날짜: ${data.date}\n생성: ${data.total_created}건\n삭제: ${data.deleted}건`
      )
      await loadStats()
    } else {
      addLog('error', response.data.message)
    }
  } catch (error) {
    console.error('테스트 데이터 생성 실패:', error)
    addLog('error', '테스트 데이터 생성 실패', error.response?.data?.message || error.message)
  } finally {
    loading.value = false
  }
}

const addLog = (type, message, output = '') => {
  const now = new Date()
  logs.value.unshift({
    type,
    message,
    output,
    time: now.toLocaleTimeString('ko-KR')
  })
}

const clearLogs = () => {
  logs.value = []
}

const getLogIcon = (type) => {
  switch (type) {
    case 'success':
      return 'fas fa-check-circle'
    case 'error':
      return 'fas fa-times-circle'
    case 'info':
      return 'fas fa-info-circle'
    case 'warning':
      return 'fas fa-exclamation-triangle'
    default:
      return 'fas fa-circle'
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.dashboard-header h1 i {
  color: #6366f1;
  margin-right: 1rem;
}

.subtitle {
  color: #6b7280;
  font-size: 1.125rem;
}

/* 통계 섹션 */
.stats-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.stats-section h2 {
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stats-section h2 i {
  color: #6366f1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: #6366f1;
  transform: translateY(-2px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.performances {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.boxoffice {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.ongoing {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.missing {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.stat-detail {
  font-size: 0.875rem;
  color: #9ca3af;
}

.btn-refresh {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-refresh:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 액션 섹션 */
.actions-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.actions-section h2 {
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.actions-section h2 i {
  color: #6366f1;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s;
}

.action-card:hover {
  border-color: #6366f1;
}

.action-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.action-header i {
  font-size: 1.5rem;
  color: #6366f1;
}

.action-header h3 {
  color: #1f2937;
  margin: 0;
}

.action-desc {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.btn-action {
  width: 100%;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: white;
}

.btn-action.primary {
  background: #6366f1;
}

.btn-action.primary:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-action.success {
  background: #10b981;
}

.btn-action.success:hover:not(:disabled) {
  background: #059669;
}

.btn-action.info {
  background: #3b82f6;
}

.btn-action.info:hover:not(:disabled) {
  background: #2563eb;
}

.btn-action.warning {
  background: #f59e0b;
}

.btn-action.warning:hover:not(:disabled) {
  background: #d97706;
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 로그 섹션 */
.logs-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logs-section h2 {
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logs-section h2 i {
  color: #6366f1;
}

.logs-container {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.log-entry {
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: #f9fafb;
  border-left: 4px solid;
  border-radius: 4px;
}

.log-entry.success {
  border-left-color: #10b981;
}

.log-entry.error {
  border-left-color: #ef4444;
}

.log-entry.info {
  border-left-color: #3b82f6;
}

.log-entry.warning {
  border-left-color: #f59e0b;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.log-time {
  font-size: 0.875rem;
  color: #6b7280;
}

.log-status {
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.log-status.success {
  color: #10b981;
}

.log-status.error {
  color: #ef4444;
}

.log-status.info {
  color: #3b82f6;
}

.log-status.warning {
  color: #f59e0b;
}

.log-message {
  color: #1f2937;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.log-output {
  background: #1f2937;
  color: #10b981;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.btn-clear-logs {
  padding: 0.75rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-clear-logs:hover {
  background: #dc2626;
}
</style>
