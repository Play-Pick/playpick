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
            if (data.success) {
                allPerformances.value = data.data

                // 최종 업데이트 날짜 설정
                if (allPerformances.value.length > 0) {
                    const today = new Date()
                    latestDate.value = `${today.getFullYear()}년 ${today.getMonth() + 1}월 ${today.getDate()}일`
                }
            } else {
                error.value = '데이터를 불러올 수 없습니다.'
            }
        } catch (e) {
            console.error('Error:', e)
            error.value = '오류가 발생했습니다.'
        } finally {
            loading.value = false
        }
    }

    // 장르 변경을 담당하는 함수
    const changeGenre = async (nextGenre) => {
        if (genre.value === nextGenre) return
        genre.value = nextGenre
        currentPage.value = 0
        await load()
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