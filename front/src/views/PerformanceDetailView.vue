<template>
  <div class="performance-detail">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <div v-else-if="currentPerformance" class="detail-content">
      <!-- 공연 기본 정보 -->
      <HeaderSection
        :performance="currentPerformance"
        :like-loading="likeLoading"
        @open-map="handleOpenMap"
        @toggle-like="handleToggleLike"
      >
        <template #rating-chart>
          <RatingChart :reviews="reviews" />
        </template>
      </HeaderSection>

      <!-- 탭 네비게이션 -->
      <div class="tab-navigation">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
        </button>
      </div>

      <!-- 탭 컨텐츠 -->
      <div class="tab-content">
        <!-- 1. 공연정보 탭 -->
        <div v-show="activeTab === 'info'" class="tab-pane">
          <div v-if="currentPerformance.detail">
        <!-- 줄거리 -->
        <div v-if="currentPerformance.detail.sty" class="section-card">
          <h2><i class="fas fa-book-open"></i> 줄거리</h2>
          <p class="description">{{ currentPerformance.detail.sty }}</p>
        </div>

        <!-- 출연진/제작진 -->
        <div class="grid-sections">
          <div v-if="currentPerformance.detail.prfcast" class="section-card">
            <h3><i class="fas fa-users"></i> 출연진</h3>
            <p class="description">{{ currentPerformance.detail.prfcast }}</p>
          </div>

          <div v-if="currentPerformance.detail.prfcrew" class="section-card">
            <h3><i class="fas fa-user-tie"></i> 제작진</h3>
            <p class="description">{{ currentPerformance.detail.prfcrew }}</p>
          </div>
        </div>

        <!-- 가격 및 공연시간 정보 -->
        <div class="grid-sections">
          <div v-if="currentPerformance.detail.pcseguidance" class="section-card">
            <h3><i class="fas fa-won-sign"></i> 티켓 가격</h3>
            <p class="description">{{ currentPerformance.detail.pcseguidance }}</p>
          </div>

          <div v-if="currentPerformance.detail.dtguidance" class="section-card">
            <h3><i class="fas fa-calendar-check"></i> 공연 시간 안내</h3>
            <p class="description">{{ currentPerformance.detail.dtguidance }}</p>
          </div>
        </div>

        <!-- 소개 이미지 -->
        <div v-if="currentPerformance.intro_images?.length" class="section-card">
          <h3><i class="fas fa-images"></i> 소개 이미지</h3>
          <div class="images-grid">
            <img
              v-for="image in currentPerformance.intro_images"
              :key="image.id"
              :src="image.image_url"
              :alt="`소개 이미지 ${image.order + 1}`"
              class="intro-image"
              @error="(e) => (e.target.style.display = 'none')"
            />
          </div>
        </div>

        <!-- YouTube 관련 영상 -->
        <YouTubeVideoSection :performanceId="route.params.id" />
          </div>

          <div v-else class="no-detail">
            <i class="fas fa-info-circle"></i>
            <p>상세 정보가 아직 수집되지 않았습니다.</p>
            <p class="sub-text">기본 정보만 표시됩니다.</p>
          </div>
        </div>

        <!-- 2. 관람후기 탭 -->
        <div v-show="activeTab === 'review'" class="tab-pane">
          <div class="review-header">
            <div class="review-controls">
              <button @click="reviewSortOrder = 'latest'" :class="['sort-button', { active: reviewSortOrder === 'latest' }]">
                <i class="fas fa-clock"></i> 최신순
              </button>
              <button @click="reviewSortOrder = 'views'" :class="['sort-button', { active: reviewSortOrder === 'views' }]">
                <i class="fas fa-eye"></i> 조회순
              </button>
            </div>
            <button @click="goToWrite('REVIEW')" class="btn-write">
              <i class="fas fa-pen"></i> 관람후기 작성
            </button>
          </div>

          <ReviewList
            :reviews="filteredReviews('관람 후기')"
            @review-updated="loadReviews"
          />
        </div>

        <!-- 3. 기대평 탭 -->
        <div v-show="activeTab === 'expectation'" class="tab-pane">
          <div class="review-header">
            <div class="review-controls">
              <button @click="expectationSortOrder = 'latest'" :class="['sort-button', { active: expectationSortOrder === 'latest' }]">
                <i class="fas fa-clock"></i> 최신순
              </button>
              <button @click="expectationSortOrder = 'views'" :class="['sort-button', { active: expectationSortOrder === 'views' }]">
                <i class="fas fa-eye"></i> 조회순
              </button>
            </div>
            <button @click="goToWrite('EXPECT')" class="btn-write">
              <i class="fas fa-pen"></i> 기대평 작성
            </button>
          </div>

          <ReviewList
            :reviews="filteredReviews('기대평')"
            @review-updated="loadReviews"
          />
        </div>

        <!-- 4. Q&A 탭 -->
        <div v-show="activeTab === 'qna'" class="tab-pane">
          <div class="review-header">
            <div class="review-controls">
              <button @click="qnaSortOrder = 'latest'" :class="['sort-button', { active: qnaSortOrder === 'latest' }]">
                <i class="fas fa-clock"></i> 최신순
              </button>
              <button @click="qnaSortOrder = 'views'" :class="['sort-button', { active: qnaSortOrder === 'views' }]">
                <i class="fas fa-eye"></i> 조회순
              </button>
            </div>
            <button @click="goToWrite('QNA')" class="btn-write">
              <i class="fas fa-pen"></i> Q&A 작성
            </button>
          </div>

          <ReviewList
            :reviews="filteredReviews('질문')"
            @review-updated="loadReviews"
          />
        </div>
      </div>

      <!-- 목록으로 돌아가기 -->
      <div class="actions">
        <button @click="goBack" class="btn-back">
          <i class="fas fa-list"></i> 전체 공연 목록
        </button>
        <button @click="goHome" class="btn-home">
          <i class="fas fa-home"></i> 홈으로
        </button>
      </div>
    </div>

    <!-- 카카오맵 모달 -->
    <MapModal
      :show="showMapModal"
      :venueName="currentPerformance?.fcltynm"
      @close="closeMapModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePerformanceDetail } from '@/composables/usePerformanceDetail'
import { useKakaoMap } from '@/composables/useKakaoMap'
import { useUserTracking } from '@/composables/useUserTracking'
import { usePerformanceStore } from '@/stores/performanceStore'
import HeaderSection from '@/components/PerformanceDetail/HeaderSection.vue'
import MapModal from '@/components/PerformanceDetail/MapModal.vue'
import RatingChart from '@/components/PerformanceDetail/RatingChart.vue'
import ReviewList from '@/components/PerformanceDetail/ReviewList.vue'
import YouTubeVideoSection from '@/components/PerformanceDetail/YouTubeVideoSection.vue'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()
const { currentPerformance, loading, error, goBack, goHome } = usePerformanceDetail()
const { showMapModal, openMapModal, closeMapModal, initMap } = useKakaoMap()
const { logView } = useUserTracking()
const performanceStore = usePerformanceStore()
const { toggleLike, likeLoading } = performanceStore

const reviews = ref([])

// 탭 관련 상태
const activeTab = ref('info')
const tabs = [
  { id: 'info', label: '공연정보', icon: 'fas fa-info-circle' },
  { id: 'review', label: '관람후기', icon: 'fas fa-star' },
  { id: 'expectation', label: '기대평', icon: 'fas fa-heart' },
  { id: 'qna', label: 'Q&A', icon: 'fas fa-question-circle' }
]

// 정렬 순서 상태
const reviewSortOrder = ref('latest')
const expectationSortOrder = ref('latest')
const qnaSortOrder = ref('latest')

// 카테고리별 필터링 및 정렬
const filteredReviews = (category) => {
  // 카테고리 매핑: 한글 -> 영문 코드
  const categoryMap = {
    '관람 후기': 'REVIEW',
    '기대평': 'EXPECT',
    '질문': 'QNA'
  }

  const categoryCode = categoryMap[category] || category
  let filtered = reviews.value.filter(review => review.category === categoryCode)

  const sortOrder = category === '관람 후기' ? reviewSortOrder.value
                  : category === '기대평' ? expectationSortOrder.value
                  : qnaSortOrder.value

  if (sortOrder === 'latest') {
    return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else {
    return filtered.sort((a, b) => b.view_count - a.view_count)
  }
}

// 리뷰 데이터 로드
const loadReviews = async () => {
  try {
    const response = await apiClient.get('/articles/')
    const allArticles = response.data.results || response.data

    // 현재 공연의 리뷰만 필터링
    reviews.value = allArticles.filter(
      article => article.performance === route.params.id
    )
  } catch (err) {
    console.error('리뷰 로드 실패:', err)
  }
}

onMounted(async () => {
  await loadReviews()

  // 공연 상세 페이지 조회 로그 전송
  if (currentPerformance.value?.mt20id) {
    await logView(currentPerformance.value.mt20id)
  }
})

const handleOpenMap = async () => {
  await openMapModal()
  setTimeout(() => {
    if (currentPerformance.value?.fcltynm) {
      initMap(currentPerformance.value.fcltynm)
    }
  }, 150)
}

// 찜하기 토글 핸들러 (Store 통해 전역 상태 관리)
const handleToggleLike = async () => {
  if (!currentPerformance.value?.mt20id) return

  try {
    await toggleLike(currentPerformance.value.mt20id)
    // Store가 자동으로 모든 목록의 상태를 업데이트
  } catch (err) {
    if (err.message === '로그인이 필요합니다.') {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('찜하기 토글 실패:', err)
      alert(err.message || '찜하기 처리 중 오류가 발생했습니다.')
    }
  }
}

// 맵 모달이 열릴 때 지도 초기화
watch(showMapModal, (newVal) => {
  if (newVal && currentPerformance.value?.fcltynm) {
    setTimeout(() => {
      initMap(currentPerformance.value.fcltynm)
    }, 150)
  }
})

// refresh 쿼리 변경 감지 (글 작성 후 돌아왔을 때)
watch(
  () => route.query.refresh,
  (newVal) => {
    if (newVal) {
      loadReviews()
      // 쿼리 파라미터 제거 (URL 정리)
      router.replace({ name: 'performance-detail', params: { id: route.params.id } })
    }
  }
)

// 글쓰기 페이지로 이동
const goToWrite = (category) => {
  router.push({
    name: 'community-write',
    query: {
      category: category,
      performanceId: currentPerformance.value.mt20id
    }
  })
}
</script>

<style scoped>
.performance-detail {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  transition: background 0.3s;
}

:root.dark .performance-detail {
  background: linear-gradient(to bottom, #1a1a1a, #0f0f0f);
}

.loading,
.error {
  text-align: center;
  padding: 5rem 2rem;
}

.loading .spinner {
  display: inline-block;
  width: 4rem;
  height: 4rem;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #6b7280;
  font-size: 1.125rem;
  transition: color 0.3s;
}

:root.dark .loading p {
  color: #9ca3af;
}

.error {
  color: #dc2626;
}

.error i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.detail-content {
  background: transparent;
}

/* 섹션 카드 */
.section-card {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .section-card {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.section-card h2,
.section-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
  transition: color 0.3s, border-color 0.3s;
}

:root.dark .section-card h2,
:root.dark .section-card h3 {
  color: #f3f4f6;
  border-bottom-color: #374151;
}

.section-card h2 {
  font-size: 1.5rem;
}

.section-card h3 {
  font-size: 1.2rem;
}

.section-card h2 i,
.section-card h3 i {
  color: #42b983;
  margin-right: 0.5rem;
  transition: color 0.3s;
}

:root.dark .section-card h2 i,
:root.dark .section-card h3 i {
  color: #818cf8;
}

.description {
  line-height: 1.8;
  color: #555;
  white-space: pre-wrap;
  transition: color 0.3s;
}

:root.dark .description {
  color: #9ca3af;
}

/* 그리드 섹션 */
.grid-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

/* 이미지 그리드 */
.images-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.intro-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
}

:root.dark .intro-image {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.intro-image:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

:root.dark .intro-image:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.7);
}

/* 상세 정보 없음 */
.no-detail {
  text-align: center;
  padding: 4rem 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 2rem;
  transition: background 0.3s;
}

:root.dark .no-detail {
  background: #2c2c2c;
}

.no-detail i {
  font-size: 4rem;
  color: #ccc;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .no-detail i {
  color: #4b5563;
}

.no-detail p {
  font-size: 1.1rem;
  color: #666;
  margin: 0.5rem 0;
  transition: color 0.3s;
}

:root.dark .no-detail p {
  color: #9ca3af;
}

.no-detail .sub-text {
  font-size: 0.9rem;
  color: #999;
  transition: color 0.3s;
}

:root.dark .no-detail .sub-text {
  color: #6b7280;
}

/* 탭 네비게이션 */
.tab-navigation {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
  padding: 0.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .tab-navigation {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.tab-button {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

:root.dark .tab-button {
  color: #9ca3af;
}

.tab-button:hover {
  background: #f3f4f6;
  color: #111827;
}

:root.dark .tab-button:hover {
  background: #374151;
  color: #f3f4f6;
}

.tab-button.active {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

:root.dark .tab-button.active {
  background: linear-gradient(to right, #818cf8, #a78bfa);
  box-shadow: 0 4px 12px rgba(129, 140, 248, 0.3);
}

.tab-button i {
  font-size: 1.125rem;
}

/* 탭 컨텐츠 */
.tab-content {
  margin-top: 2rem;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 리뷰 헤더 (정렬 + 작성 버튼) */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.review-controls {
  display: flex;
  gap: 0.5rem;
}

.sort-button {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

:root.dark .sort-button {
  background: #2c2c2c;
  border-color: #374151;
  color: #9ca3af;
}

.sort-button:hover {
  border-color: #6366f1;
  color: #6366f1;
}

:root.dark .sort-button:hover {
  border-color: #818cf8;
  color: #818cf8;
}

/* 작성 버튼 */
.btn-write {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 0.9375rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

:root.dark .btn-write {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-write:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  transform: translateY(-2px);
}

:root.dark .btn-write:hover {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.sort-button.active {
  border-color: #6366f1;
  background: #6366f1;
  color: white;
}

:root.dark .sort-button.active {
  border-color: #818cf8;
  background: #818cf8;
}

/* 액션 버튼 */
.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-back,
.btn-home {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-back {
  background-color: #6c757d;
  color: white;
}

.btn-back:hover {
  background-color: #5a6268;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

:root.dark .btn-back:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.btn-home {
  background-color: #42b983;
  color: white;
}

:root.dark .btn-home {
  background-color: #818cf8;
}

.btn-home:hover {
  background-color: #359268;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

:root.dark .btn-home:hover {
  background-color: #6366f1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

/* 반응형 */
@media (max-width: 768px) {
  .performance-detail {
    padding: 1rem;
  }

  .grid-sections {
    grid-template-columns: 1fr;
  }

  .tab-navigation {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .tab-button {
    flex: 1 1 calc(50% - 0.25rem);
    padding: 0.875rem 1rem;
    font-size: 0.875rem;
  }

  .tab-button i {
    font-size: 1rem;
  }

  .review-header {
    flex-direction: column;
    align-items: stretch;
  }

  .review-controls {
    justify-content: center;
  }

  .sort-button {
    flex: 1;
  }

  .btn-write {
    width: 100%;
    justify-content: center;
  }

  .actions {
    flex-direction: column;
  }

  .btn-back,
  .btn-home {
    width: 100%;
  }
}

</style>
