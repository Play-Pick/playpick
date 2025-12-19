<template>
  <div class="community">
    <div class="community-header">
      <h1>커뮤니티</h1>
      <FilterButton @filter="handleFilter" />
    </div>

    <ArticleList
      :articles="filteredArticles"
      :loading="loading"
      :error="error"
      @like="toggleLike"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCommunityStore } from '@/stores/communityStore'
import { storeToRefs } from 'pinia'
import ArticleList from '@/components/Community/ArticleList.vue'
import FilterButton from '@/components/Community/FilterButton.vue'

const communityStore = useCommunityStore()
const { articles, loading, error } = storeToRefs(communityStore)

const selectedCategory = ref(null)

// 필터링된 게시글
const filteredArticles = computed(() => {
  if (!selectedCategory.value) {
    return articles.value
  }
  return articles.value.filter(article => article.category === selectedCategory.value)
})

const handleFilter = (filterOptions) => {
  selectedCategory.value = filterOptions.category
}

const toggleLike = async (id) => {
  try {
    await communityStore.likeArticle(id)
  } catch (err) {
    console.error('좋아요 처리 실패:', err)
  }
}

onMounted(async () => {
  await communityStore.fetchArticles()
})
</script>

<style scoped>
.community {
  padding: 2rem;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  margin: 0;
  color: #2c3e50;
}
</style>
