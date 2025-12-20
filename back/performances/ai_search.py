"""
AI 의미 기반 검색 유틸리티
- 코사인 유사도 계산
- LLM 추천 사유 생성
"""

import os
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()


class AISearchEngine:
    """AI 검색 엔진"""

    def __init__(self):
        self.client = OpenAI(
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
            api_key=os.getenv("GMS_KEY"),
        )

    def get_embedding(self, text):
        """텍스트를 임베딩 벡터로 변환"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def find_similar_performances(self, user_query, performances_qs, top_k=10):
        """
        사용자 쿼리와 유사한 공연을 찾아서 반환

        Args:
            user_query (str): 사용자 검색어
            performances_qs (QuerySet): 검색 대상 공연 QuerySet
            top_k (int): 반환할 공연 개수

        Returns:
            list: (Performance 객체, 유사도 점수) 튜플 리스트
        """
        # 1. 사용자 쿼리 임베딩
        user_vector = np.array(self.get_embedding(user_query)).reshape(1, -1)

        # 2. 임베딩이 있는 공연만 필터링
        performances = list(performances_qs.filter(embedding_vector__isnull=False))

        if not performances:
            return []

        # 3. 모든 공연의 임베딩 벡터 추출
        all_vectors = np.array([p.embedding_vector for p in performances])

        # 4. 코사인 유사도 계산
        similarities = cosine_similarity(user_vector, all_vectors)[0]

        # 5. 유사도 기준 정렬 후 Top K 추출
        top_indices = similarities.argsort()[::-1][:top_k]

        # 6. 결과 반환 (공연 객체, 유사도 점수)
        results = [(performances[i], float(similarities[i])) for i in top_indices]

        return results

    def generate_recommendation_reason(self, user_input, performance):
        """
        Top 1 공연에 대한 추천 사유를 LLM으로 생성

        Args:
            user_input (str): 사용자 검색어
            performance (Performance): 추천 공연 객체

        Returns:
            str: AI가 생성한 추천 멘트
        """
        # 공연 정보 추출
        title = performance.prfnm
        genre = performance.genrenm or "공연"

        summary = ""
        if hasattr(performance, 'detail') and performance.detail and performance.detail.sty:
            summary = performance.detail.sty[:200]

        # LLM 프롬프트
        prompt = f"""
Role: 당신은 센스 있는 공연 큐레이터입니다.

Task: 사용자의 검색 의도를 파악하고, 추천 공연이 왜 적합한지 한 문장으로 매력적으로 설명해주세요.

User Input: "{user_input}"
Recommended Performance: "{title}"
Genre: "{genre}"
Summary: "{summary}"

Constraints:
1. 반말 모드(친근하게)
2. 이모지 1개 포함
3. 50자 이내로 짧게
4. "이 공연은~" 으로 시작하지 말 것. 바로 본론으로.

Output Example:
"답답한 속을 뻥 뚫어주는 록 사운드로 스트레스를 날려버려! 🎸"
        """.strip()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 친근한 공연 추천 큐레이터입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM 생성 실패: {e}")
            return f"{title}을(를) 추천드려요! 🎭"
