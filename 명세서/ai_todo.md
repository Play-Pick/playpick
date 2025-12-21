📄 파일명: AI_SEARCH_SPEC.md
Markdown

# 🧠 AI 의미 기반 검색 및 추천 사유 생성 명세서

## 1. 개요 (Overview)
사용자의 자연어 입력(예: "우울할 때 위로가 되는 뮤지컬")을 분석하여, 단순 키워드 매칭이 아닌 **의미적 유사도(Semantic Similarity)**가 가장 높은 공연을 추천한다. 
또한, 가장 적합한 추천 결과(Top 1)에 대해 **생성형 AI(LLM)가 추천 사유**를 작성하여 제공한다.

---

## 2. 시스템 아키텍처 (Architecture)

### 📊 데이터 흐름도
1. **User Input:** "스트레스 풀리는 신나는 공연 추천해줘"
2. **Embedding:** 입력 텍스트를 벡터화 (OpenAI `text-embedding-3-small` 등 사용)
3. **Vector Search:** 미리 저장된 공연 벡터들과 **코사인 유사도(Cosine Similarity)** 계산
4. **Ranking:** 유사도 점수순으로 Top-N 추출
5. **Reasoning (LLM):** Top 1 공연에 대해 추천 멘트 생성
6. **Response:** 검색 결과 리스트 + AI 추천 멘트 반환

---

## 3. 구현 상세: 유사도 검색 (Similarity Search)

### ✅ 전략: In-Memory Calculation (Numpy)
데이터 규모가 수천 건 수준이므로, 별도의 Vector DB(Pinecone 등)를 구축하지 않고 **서버 메모리에서 Numpy 연산**을 수행한다. (속도: < 0.05s)

### 🛠 Backend 구현 가이드 (Django)

**1. 사전 준비 (Data Loading)**
서버 시작 시(`apps.py`의 `ready()`) DB에 저장된 벡터를 메모리에 로드한다.

```python
# performances/apps.py 또는 검색 전용 모듈
import numpy as np
import pickle
from django.apps import AppConfig

class SearchConfig(AppConfig):
    name = 'performances'
    vector_cache = None
    id_cache = None

    def ready(self):
        # DB나 pickle 파일에서 벡터 로드
        # vector_cache shape: (데이터개수, 1536)
        pass
2. 검색 로직 (Search Logic)

Python

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_similar_performances(user_vector, top_k=10):
    """
    user_vector: 사용자의 입력 텍스트 임베딩 (1, 1536)
    all_vectors: 전체 공연 임베딩 (N, 1536) - 메모리에 로드된 것
    """
    # 1. 코사인 유사도 계산 (행렬 연산으로 고속 처리)
    # 결과 shape: (1, N)
    sim_scores = cosine_similarity(user_vector, all_vectors)

    # 2. 상위 K개 인덱스 추출 (내림차순 정렬)
    # argsort는 오름차순이므로 [::-1]로 뒤집음
    top_indices = sim_scores[0].argsort()[::-1][:top_k]
    
    # 3. 결과 ID 반환
    return [all_ids[i] for i in top_indices]
4. 구현 상세: 추천 사유 생성 (Reason Generation)
✅ 전략: "Top 1 Focus" (속도/비용 최적화)
모든 검색 결과에 대해 AI를 호출하면 응답 시간이 너무 길어진다(3초 이상). 따라서 가장 유사도가 높은 1위 공연에 대해서만 실시간으로 멘트를 생성한다.

📝 Prompt Engineering
LLM에게 단순 요약이 아닌, 사용자의 니즈(Input)와 공연의 특징(Feature)을 연결하도록 지시한다.

Python

def generate_recommendation_reason(user_input, performance_title, performance_summary):
    prompt = f"""
    Role: 당신은 센스 있는 공연 큐레이터입니다.
    
    Task: 사용자의 검색 의도를 파악하고, 추천 공연이 왜 적합한지 한 문장으로 매력적으로 설명해주세요.
    
    User Input: "{user_input}"
    Recommended Performance: "{performance_title}"
    Summary: "{performance_summary}"
    
    Constraints:
    1. 반말 모드(친근하게)
    2. 이모지 1개 포함
    3. 50자 이내로 짧게
    4. "이 공연은~" 으로 시작하지 말 것. 바로 본론으로.
    
    Output Example:
    "답답한 속을 뻥 뚫어주는 록 사운드로 스트레스를 날려버려! 🎸"
    """
    
    # OpenAI ChatCompletion 호출 코드...
    return response
5. API 응답 구조 (Response Format)
프론트엔드에서 받게 될 데이터 구조이다.

JSON

{
  "ai_comment": "시험 기간 스트레스, 이 록 뮤지컬로 다 부숴버리세요! 🎸",
  "results": [
    {
      "id": "PF12345",
      "title": "뮤지컬 영웅",
      "poster": "http://...",
      "similarity_score": 0.89,
      "tags": ["#웅장한", "#역사", "#감동"]
    },
    {
      "id": "PF67890",
      "title": "레미제라블",
      "similarity_score": 0.85,
      ...
    }
  ]
}
6. Frontend UX 가이드 (Vue.js)
⏳ 로딩 처리 (Latency Handling)
LLM 응답(1~2초)을 기다리는 동안 사용자가 이탈하지 않도록 시각적 피드백을 제공한다.

스켈레톤 UI: 검색 버튼 클릭 즉시 리스트 영역에 스켈레톤 로더 표시.

AI 타이핑 효과: ai_comment가 도착하면 한 글자씩 타이핑되듯 나타나는 애니메이션 적용 (Typewriter Effect).

검색 결과 먼저 표시 (Optional): - 기술적으로 가능하다면, 벡터 검색 결과(0.1초)를 먼저 보여주고

상단 AI 코멘트 영역만 "AI가 분석 중입니다... 🤖" 로 띄운 뒤 나중에 텍스트를 갈아끼운다.

7. 개발 체크리스트 (Checklist)
[ ] Back: 전체 공연 임베딩 데이터 생성 및 DB 저장 (또는 .npy 파일 저장)

[ ] Back: 서버 구동 시 임베딩 데이터를 메모리에 로드하는 로직 구현 (apps.py)

[ ] Back: 사용자 입력 -> 임베딩 변환 -> 코사인 유사도 계산 함수 구현

[ ] Back: Top 1 결과에 대한 OpenAI API 프롬프트 연동

[ ] Front: 검색바 UI 및 로딩 인디케이터 구현

[ ] Test: "슬픈", "신나는", "데이트" 등 다양한 감정 키워드로 테스트하여 정확도 확인