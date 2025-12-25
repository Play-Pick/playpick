<template>
  <div>
    <!-- 탭 메뉴 -->
    <div class="tabs">
      <button
        :class="['tab', { active: activeTab === 'articles' }]"
        @click="$emit('update:activeTab', 'articles')"
      >
        <i class="fas fa-comment-dots"></i> 내가 쓴 리뷰 ({{ articles.length }})
      </button>
      <button
        :class="['tab', { active: activeTab === 'comments' }]"
        @click="$emit('update:activeTab', 'comments')"
      >
        <i class="fas fa-comments"></i> 내가 쓴 댓글 ({{ comments.length }})
      </button>
    </div>

    <!-- 탭 컨텐츠 -->
    <div class="tab-content">
      <!-- 내가 쓴 리뷰 -->
      <div v-if="activeTab === 'articles'" class="articles-list">
        <div v-if="articles.length === 0" class="empty-state">
          <i class="fas fa-inbox"></i>
          <p>작성한 리뷰가 없습니다</p>
        </div>
        <div
          v-for="article in articles"
          :key="article.id"
          class="article-card"
          @click="$emit('article-click', article.performance)"
        >
          <div class="article-header">
            <h3>{{ article.title }}</h3>
            <div v-if="article.rank" class="rating">
              <i
                v-for="n in 5"
                :key="n"
                :class="['fas fa-star', { filled: n <= article.rank }]"
              ></i>
            </div>
          </div>
          <p class="article-content">{{ truncate(article.content, 100) }}</p>
          <div class="article-meta">
            <span class="performance-name">
              <i class="fas fa-ticket-alt"></i> {{ article.performance_name }}
            </span>
            <span class="date">{{ formatDate(article.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 내가 쓴 댓글 -->
      <div v-else class="comments-list">
        <div v-if="comments.length === 0" class="empty-state">
          <i class="fas fa-inbox"></i>
          <p>작성한 댓글이 없습니다</p>
        </div>
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="comment-card"
          @click="$emit('comment-click', comment.article)"
        >
          <p class="comment-content">{{ comment.content }}</p>
          <div class="comment-meta">
            <span class="article-title">
              <i class="fas fa-file-alt"></i> {{ getArticleTitle(comment.article) }}
            </span>
            <span class="date">{{ formatDate(comment.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  activeTab: {
    type: String,
    default: 'articles'
  },
  articles: {
    type: Array,
    default: () => []
  },
  comments: {
    type: Array,
    default: () => []
  },
  allArticles: {
    type: Array,
    default: () => []
  }
})

defineEmits(['update:activeTab', 'article-click', 'comment-click'])

// 유틸리티 함수
const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getArticleTitle = (articleId) => {
  const article = props.allArticles.find(a => a.id === articleId)
  return article ? article.title : '삭제된 게시글'
}
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .tabs {
  border-bottom-color: #374151;
}

.tab {
  padding: 1rem 2rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.3s;
  margin-bottom: -2px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .tab {
  color: #9ca3af;
}

.tab:hover {
  color: #6366f1;
}

:root.dark .tab:hover {
  color: #818cf8;
}

.tab.active {
  color: #6366f1;
  border-bottom-color: #6366f1;
}

:root.dark .tab.active {
  color: #818cf8;
  border-bottom-color: #818cf8;
}

.tab-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .tab-content {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1.125rem;
}

/* 리뷰 카드 */
.articles-list,
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-card,
.comment-card {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f9fafb, #ffffff);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

:root.dark .article-card,
:root.dark .comment-card {
  background: linear-gradient(135deg, #1a1a1a, #2c2c2c);
}

.article-card:hover,
.comment-card:hover {
  border-color: #6366f1;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(99, 102, 241, 0.2);
}

:root.dark .article-card:hover,
:root.dark .comment-card:hover {
  border-color: #818cf8;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.article-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  transition: color 0.3s;
}

:root.dark .article-header h3 {
  color: #f3f4f6;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.rating .fa-star {
  color: #d1d5db;
  font-size: 0.875rem;
  transition: color 0.3s;
}

:root.dark .rating .fa-star {
  color: #4b5563;
}

.rating .fa-star.filled {
  color: #fbbf24;
}

.article-content {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .article-content {
  color: #9ca3af;
}

.article-meta,
.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #9ca3af;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  transition: all 0.3s;
}

:root.dark .article-meta,
:root.dark .comment-meta {
  border-top-color: #374151;
  color: #6b7280;
}

.performance-name,
.article-title {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #6366f1;
  font-weight: 600;
  transition: color 0.3s;
}

:root.dark .performance-name,
:root.dark .article-title {
  color: #818cf8;
}

.comment-content {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

:root.dark .comment-content {
  color: #d1d5db;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    gap: 0;
  }

  .tab {
    padding: 0.75rem 1rem;
    border-bottom: none;
    border-left: 3px solid transparent;
  }

  .tab.active {
    border-left-color: #6366f1;
    border-bottom-color: transparent;
  }

  :root.dark .tab.active {
    border-left-color: #818cf8;
  }

  .tab-content {
    padding: 1rem;
  }

  .article-meta,
  .comment-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
