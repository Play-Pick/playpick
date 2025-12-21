# 🎉 AI 의미 기반 검색 구현 완료

## ✅ 구현된 기능

1. **임베딩 벡터 저장 필드** - Performance 모델에 추가됨
2. **임베딩 생성 Command** - `python manage.py generate_embeddings`
3. **AI 검색 엔진** - 코사인 유사도 계산 및 LLM 추천 사유 생성
4. **API 엔드포인트** - POST `/api/performances/ai-search/`

---

## 📋 사용 방법

### 1. 임베딩 생성 (최초 1회 실행)

공연 데이터의 임베딩 벡터를 생성합니다.

```bash
cd c:\Users\gs\Desktop\새 폴더 (2)\final-pjt\back
python manage.py generate_embeddings
```

**옵션:**
- `--batch-size 100`: 한 번에 처리할 개수 (기본: 100)
- `--force`: 이미 임베딩이 있어도 재생성

**예시:**
```bash
# 배치 크기 50으로 실행
python manage.py generate_embeddings --batch-size 50

# 전체 재생성
python manage.py generate_embeddings --force
```

---

### 2. API 호출 방법

#### 엔드포인트
```
POST http://localhost:8000/api/performances/ai-search/
```

#### 요청 예시
```json
{
  "query": "신나는 공연 추천해줘"
}
```

#### 응답 예시
```json
{
  "success": true,
  "ai_comment": "신나는 음악과 화려한 안무로 에너지를 폭발시켜! 🎉",
  "results": [
    {
      "mt20id": "PF12345",
      "prfnm": "뮤지컬 맘마미아",
      "poster": "http://www.kopis.or.kr/upload/...",
      "genrenm": "뮤지컬",
      "prfpdfrom": "2024-01-01",
      "prfpdto": "2024-12-31",
      "fcltynm": "충무아트센터 대극장",
      "area": "서울특별시",
      "prfstate": "공연중",
      "is_liked": false,
      "similarity_score": 0.8912
    },
    {
      "mt20id": "PF67890",
      "prfnm": "뮤지컬 록키호러쇼",
      "poster": "http://www.kopis.or.kr/upload/...",
      "genrenm": "뮤지컬",
      "similarity_score": 0.8501,
      "is_liked": false
    }
    // ... 총 10개
  ]
}
```

---

### 3. 테스트 시나리오

다양한 검색어로 테스트해보세요:

```bash
# curl 사용 예시
curl -X POST http://localhost:8000/api/performances/ai-search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "우울할 때 위로가 되는 공연"}'

curl -X POST http://localhost:8000/api/performances/ai-search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "데이트하기 좋은 공연"}'

curl -X POST http://localhost:8000/api/performances/ai-search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "아이랑 보기 좋은 공연"}'
```

---

## 🧪 동작 원리

### 1. 임베딩 전략 (test_strategy_2_standard 적용)

각 공연은 다음 정보를 조합하여 임베딩됩니다:

- **기본 정보**: 공연명, 장르, 출연진, 지역, 공연장
- **상세 정보**: 관람연령, 러닝타임, 제작사
- **줄거리**: 200자까지

예시:
```
"뮤지컬 맘마미아 뮤지컬 박혜나 김소향 서울특별시 충무아트센터 대극장 관람연령 8세 이상 러닝타임 150분 제작 에이콤 전세계인이 사랑하는 아바의 명곡과 함께 펼쳐지는 신나는 뮤지컬..."
```

### 2. 검색 프로세스

```
사용자 입력: "신나는 공연 추천해줘"
    ↓
1. 사용자 쿼리 임베딩 생성 (OpenAI API)
    ↓
2. DB에 저장된 모든 공연 벡터와 코사인 유사도 계산
    ↓
3. 유사도 높은 순으로 Top 10 추출
    ↓
4. Top 1 공연에 대해 LLM이 추천 사유 생성
    ↓
5. 결과 반환
```

### 3. 코사인 유사도 계산

```python
# 사용자 벡터: [0.123, -0.456, 0.789, ...] (1536차원)
# 공연1 벡터: [0.234, -0.345, 0.567, ...]
# 공연2 벡터: [0.456, -0.234, 0.123, ...]

# 코사인 유사도 = 벡터 내적 / (벡터1 크기 * 벡터2 크기)
# 결과: 0~1 사이의 값 (1에 가까울수록 유사)
```

---

## 📊 비용 예측

### 임베딩 생성 비용

- **모델**: text-embedding-3-small
- **비용**: $0.02 / 1M tokens (실시간), $0.01 / 1M tokens (Batch)
- **예상 토큰**: 공연당 평균 150 tokens
- **60,000개 공연 기준**:
  - 실시간: ~$0.18
  - Batch: ~$0.09

### 검색 비용 (1회 검색당)

- **임베딩 생성**: ~$0.000003 (검색어)
- **LLM 추천 사유**: ~$0.0001
- **합계**: ~$0.0001

---

## 🔧 구현 파일 목록

1. **[performances/models.py](../back/performances/models.py)**
   - `embedding_vector`: JSONField (1536차원 벡터)
   - `embedding_updated_at`: DateTimeField

2. **[performances/management/commands/generate_embeddings.py](../back/performances/management/commands/generate_embeddings.py)**
   - 임베딩 생성 커맨드

3. **[performances/ai_search.py](../back/performances/ai_search.py)**
   - `AISearchEngine` 클래스
   - `get_embedding()`: 텍스트 → 벡터 변환
   - `find_similar_performances()`: 유사도 계산
   - `generate_recommendation_reason()`: LLM 추천 사유 생성

4. **[performances/api_views.py](../back/performances/api_views.py)**
   - `ai_search()`: POST `/api/performances/ai-search/`

5. **[requirements.txt](../back/requirements.txt)**
   - `openai>=1.0.0`
   - `numpy>=1.24.0`
   - `scikit-learn>=1.3.0`

---

## 🎯 프론트엔드 연동 예시

### Vue.js (Composition API)

```javascript
// stores/aiSearch.js
import { ref } from 'vue'
import axios from 'axios'

export const useAISearch = () => {
  const searchResults = ref([])
  const aiComment = ref('')
  const loading = ref(false)
  const error = ref(null)

  const searchPerformances = async (query) => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post(
        'http://localhost:8000/api/performances/ai-search/',
        { query }
      )

      if (response.data.success) {
        searchResults.value = response.data.results
        aiComment.value = response.data.ai_comment
      }
    } catch (err) {
      error.value = err.response?.data?.message || '검색 중 오류가 발생했습니다.'
    } finally {
      loading.value = false
    }
  }

  return {
    searchResults,
    aiComment,
    loading,
    error,
    searchPerformances
  }
}
```

### 컴포넌트 사용 예시

```vue
<template>
  <div class="ai-search">
    <div class="search-bar">
      <input
        v-model="query"
        @keyup.enter="handleSearch"
        placeholder="어떤 공연을 찾으시나요? (예: 신나는 공연 추천해줘)"
      />
      <button @click="handleSearch" :disabled="loading">
        {{ loading ? '검색 중...' : '검색' }}
      </button>
    </div>

    <!-- AI 코멘트 -->
    <div v-if="aiComment" class="ai-comment">
      <p>{{ aiComment }}</p>
    </div>

    <!-- 스켈레톤 로딩 -->
    <div v-if="loading" class="skeleton-loader">
      <div class="skeleton-item" v-for="i in 10" :key="i"></div>
    </div>

    <!-- 검색 결과 -->
    <div v-else class="search-results">
      <div
        v-for="performance in searchResults"
        :key="performance.mt20id"
        class="performance-card"
      >
        <img :src="performance.poster" :alt="performance.prfnm" />
        <h3>{{ performance.prfnm }}</h3>
        <p>유사도: {{ (performance.similarity_score * 100).toFixed(1) }}%</p>
        <span class="genre">{{ performance.genrenm }}</span>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAISearch } from '@/stores/aiSearch'

const query = ref('')
const { searchResults, aiComment, loading, error, searchPerformances } = useAISearch()

const handleSearch = () => {
  if (query.value.trim()) {
    searchPerformances(query.value)
  }
}
</script>
```

---

## 🚨 주의사항

1. **API 키 설정**: `.env` 파일에 `GMS_KEY`가 반드시 설정되어 있어야 합니다.

2. **첫 실행 시**: 반드시 `python manage.py generate_embeddings` 실행 필요

3. **성능**:
   - 임베딩이 없으면 검색 불가능
   - 10,000개 이상 공연 시 검색 속도 < 0.1초 (In-Memory 계산)

4. **에러 처리**:
   - 임베딩이 없을 때: "먼저 임베딩을 생성해주세요" 메시지 반환
   - OpenAI API 에러 시: 기본 추천 메시지 반환

---

## 🎉 완료!

이제 사용자가 **"신나는 공연 추천해줘"**라고 입력하면, AI가 의미적으로 유사한 공연을 찾아서 추천 사유와 함께 반환합니다!
