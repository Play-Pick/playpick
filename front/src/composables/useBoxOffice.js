import { ref, computed } from 'vue'
import performanceApi from '@/api/performances'

// 전역 상태 (모든 컴포넌트가 공유)
const genre = ref('BBBC')
const allPerformances = ref([])
const currentPage = ref(0)
const itemsPerPage = 5
const loading = ref(false)
const error = ref(null)
const latestDate = ref('')
const hasLoadedOnce = ref(false) // 최초 1회 로드 여부 추적

export function useBoxOffice() {
    // 페이지별 데이터
    const pageData = computed(() => {
        const start = currentPage.value * itemsPerPage
        const end = start + itemsPerPage
        return allPerformances.value.slice(start, end)
    })

    // 전체 페이지 수
    const totalPages = computed(() => {
        return Math.ceil(allPerformances.value.length / itemsPerPage)
    })

    // 장르에 따른 데이터를 로드하는 함수
    const load = async () => {
        loading.value = true
        error.value = null

        try {
            const { data } = await performanceApi.getBoxOfficeByGenre(genre.value)

            // success 여부와 관계없이 data 배열을 설정 (빈 배열도 정상 처리)
            allPerformances.value = data.data || []

            // 최종 업데이트 날짜 설정
            if (allPerformances.value.length > 0) {
                const today = new Date()
                latestDate.value = `${today.getFullYear()}년 ${today.getMonth() + 1}월 ${today.getDate()}일`
            }
            // 데이터가 없는 경우는 에러가 아님 (빈 배열 정상 처리)
        } catch (e) {
            console.error('Error:', e)
            // 네트워크 에러 등 실제 오류만 error로 표시
            if (e.response && e.response.status >= 500) {
                error.value = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
            } else if (e.message === 'Network Error' || !e.response) {
                error.value = '네트워크 연결을 확인해주세요.'
            } else {
                error.value = '데이터를 불러오는 중 오류가 발생했습니다.'
            }
        } finally {
            loading.value = false
        }
    }

    // 장르 변경을 담당하는 함수
    const changeGenre = async (nextGenre) => {
        // 장르가 다를 때 OR 한 번도 로드하지 않았을 때 로드
        const shouldLoad = genre.value !== nextGenre || !hasLoadedOnce.value

        genre.value = nextGenre
        currentPage.value = 0

        if (shouldLoad) {
            await load()
            hasLoadedOnce.value = true // 로드 완료 표시
        }
    }

    // 페이지 네비게이션
    const prevPage = () => {
        if (currentPage.value > 0) {
            currentPage.value--
            window.scrollTo({ top: 0, behavior: 'smooth' })
        }
    }

    const nextPage = () => {
        if (currentPage.value < totalPages.value - 1) {
            currentPage.value++
            window.scrollTo({ top: 0, behavior: 'smooth' })
        }
    }

    return {
        genre,
        allPerformances,
        pageData,
        currentPage,
        totalPages,
        loading,
        error,
        latestDate,
        load,
        changeGenre,
        prevPage,
        nextPage,
    }
}