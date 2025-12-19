import { ref, onMounted } from 'vue'
import { usePerformanceStore } from '@/stores/performanceStore'
import { storeToRefs } from 'pinia'

export function usePerformanceList() {
    const performanceStore = usePerformanceStore()
    const { performances, genres, loading, error } = storeToRefs(performanceStore)

    const selectedGenre = ref('')
    const searchQuery = ref('')

    // 필터링 함수
    const filterPerformances = async () => {
        const params = {}
        if (selectedGenre.value) params.genrenm = selectedGenre.value
        if (searchQuery.value) params.search = searchQuery.value

        await performanceStore.fetchPerformances(params)
    }

    // 초기 데이터 로드
    const loadInitialData = async () => {
        await performanceStore.fetchGenres()
        await performanceStore.fetchPerformances()
    }

    // 마운트 시 데이터 로드
    onMounted(async () => {
        await loadInitialData()
    })

    return {
        // 상태
        performances,
        genres,
        loading,
        error,
        selectedGenre,
        searchQuery,

        // 메서드
        filterPerformances,
        loadInitialData
    }
}
