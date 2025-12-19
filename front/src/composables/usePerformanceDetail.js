import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePerformanceStore } from '@/stores/performanceStore'
import { storeToRefs } from 'pinia'

export function usePerformanceDetail() {
    const route = useRoute()
    const router = useRouter()
    const performanceStore = usePerformanceStore()
    const { currentPerformance, loading, error } = storeToRefs(performanceStore)

    const goBack = () => {
        router.push({ name: 'performances' })
    }

    const goHome = () => {
        router.push('/')
    }

    onMounted(async () => {
        const id = route.params.id
        await performanceStore.fetchPerformance(id)
    })

    return {
        currentPerformance,
        loading,
        error,
        goBack,
        goHome
    }
}
