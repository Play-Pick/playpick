# AI 기능 구현 가이드 1단계

## 📌 구현 목표

2가지 핵심 AI 기능을 추가합니다:

1. **의미 기반 검색** (text-embedding-3-small)
2. **AI 추천 사유 설명** (GPT-5-mini)

---

## 🎯 1. 의미 기반 검색 (Semantic Search)

### 목적
키워드 매칭이 아닌 **의미로 검색**합니다.

```
예시:
검색: "감동적인 사랑 이야기"
→ 결과: 로맨틱 뮤지컬, 사랑 테마 연극 등
```

### 동작 방식

```
1. 공연 데이터 → 임베딩 벡터 변환 (1536차원 숫자 배열)
2. 검색어 → 임베딩 벡터 변환
3. 코사인 유사도 계산
4. 유사도 높은 순으로 정렬 → 결과 반환
```

### 구현 단계

#### Step 1: Performance 모델 수정

```python
# back/performances/models.py

class Performance(models.Model):
    # ... 기존 필드 ...

    # ✨ 새로 추가
    embedding_vector = models.JSONField(
        null=True,
        blank=True,
        help_text="text-embedding-3-small (1536차원)"
    )
    embedding_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="임베딩 마지막 업데이트 시각"
    )
```

**마이그레이션:**
```bash
cd back
python manage.py makemigrations
python manage.py migrate
```

---

#### Step 2: 임베딩 생성 유틸리티 함수

```python
# back/performances/utils/embedding.py (신규 파일)

import openai
from django.conf import settings
from django.utils import timezone

openai.api_key = settings.OPENAI_API_KEY

def generate_embedding(text):
    """
    텍스트를 임베딩 벡터로 변환

    Args:
        text (str): 변환할 텍스트

    Returns:
        list: 1536차원 임베딩 벡터
    """
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"임베딩 생성 실패: {e}")
        return None


def update_performance_embedding(performance):
    """
    공연 정보를 임베딩으로 변환하여 저장

    Args:
        performance: Performance 모델 인스턴스
    """
    # 공연 정보를 하나의 텍스트로 결합
    text_parts = [
        performance.prfnm or "",           # 제목
        performance.genrenm or "",         # 장르
        performance.cast_search_text or "" # 출연진
    ]

    # 상세 정보가 있으면 추가
    if hasattr(performance, 'detail') and performance.detail:
        detail = performance.detail
        text_parts.extend([
            detail.prfage or "",     # 관람연령
            detail.styurl_1 or "",   # 소개글 (있다면)
        ])

    # 결합
    combined_text = " ".join(filter(None, text_parts))

    if not combined_text.strip():
        print(f"공연 {performance.mt20id}: 임베딩할 텍스트 없음")
        return False

    # 임베딩 생성
    embedding = generate_embedding(combined_text)

    if embedding:
        performance.embedding_vector = embedding
        performance.embedding_updated_at = timezone.now()
        performance.save(update_fields=['embedding_vector', 'embedding_updated_at'])
        return True

    return False
```

---

#### Step 3: 기존 공연 데이터 일괄 임베딩

```python
# back/performances/management/commands/generate_embeddings.py (신규 파일)

from django.core.management.base import BaseCommand
from performances.models import Performance
from performances.utils.embedding import update_performance_embedding
import time

class Command(BaseCommand):
    help = '모든 공연 데이터의 임베딩 생성'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='처리할 최대 개수 (테스트용)'
        )

    def handle(self, *args, **options):
        limit = options.get('limit')

        # 임베딩이 없는 공연만 처리
        performances = Performance.objects.filter(
            embedding_vector__isnull=True
        )

        if limit:
            performances = performances[:limit]

        total = performances.count()
        self.stdout.write(f"처리할 공연: {total}개")

        success_count = 0
        fail_count = 0

        for idx, perf in enumerate(performances, 1):
            self.stdout.write(f"[{idx}/{total}] {perf.prfnm} 처리 중...")

            if update_performance_embedding(perf):
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f"  → 성공"))
            else:
                fail_count += 1
                self.stdout.write(self.style.ERROR(f"  → 실패"))

            # API Rate Limit 방지 (약간의 대기)
            if idx % 10 == 0:
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS(
            f"\n완료! 성공: {success_count}, 실패: {fail_count}"
        ))
```

**실행:**
```bash
# 테스트 (10개만)
python manage.py generate_embeddings --limit 10

# 전체 실행
python manage.py generate_embeddings
```

---

#### Step 4: 의미 기반 검색 API

```python
# back/performances/api_views.py

from rest_framework.decorators import action
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity
from .utils.embedding import generate_embedding
import numpy as np

class PerformanceViewSet(viewsets.ModelViewSet):
    # ... 기존 코드 ...

    @action(detail=False, methods=['get'])
    def semantic_search(self, request):
        """
        의미 기반 검색

        Query Params:
            q: 검색어 (필수)
            top_n: 결과 개수 (기본: 10)
        """
        query = request.query_params.get('q', '').strip()
        top_n = int(request.query_params.get('top_n', 10))

        if not query:
            return Response({
                'error': '검색어(q)를 입력해주세요.'
            }, status=400)

        # 1. 검색어를 임베딩으로 변환
        query_embedding = generate_embedding(query)

        if not query_embedding:
            return Response({
                'error': '임베딩 생성 실패'
            }, status=500)

        # 2. 임베딩이 있는 공연만 조회
        performances = Performance.objects.filter(
            embedding_vector__isnull=False
        ).select_related('detail')

        if not performances.exists():
            return Response({
                'results': [],
                'message': '임베딩 데이터가 없습니다. generate_embeddings 명령을 실행하세요.'
            })

        # 3. 모든 공연과 유사도 계산
        similarities = []

        for perf in performances:
            similarity = cosine_similarity(
                [query_embedding],
                [perf.embedding_vector]
            )[0][0]

            similarities.append({
                'performance': perf,
                'similarity': similarity
            })

        # 4. 유사도 높은 순 정렬
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        # 5. Top-N 추출
        top_results = similarities[:top_n]

        # 6. 직렬화
        from .serializers import PerformanceListSerializer
        results = []

        for item in top_results:
            perf_data = PerformanceListSerializer(
                item['performance'],
                context={'request': request}
            ).data
            perf_data['similarity_score'] = round(item['similarity'], 3)
            results.append(perf_data)

        return Response({
            'query': query,
            'count': len(results),
            'results': results
        })
```

**API 엔드포인트:**
```
GET /api/performances/semantic_search/?q=감동적인+사랑+이야기&top_n=5
```

---

## 🎯 2. AI 추천 사유 설명

### 목적
기존 템플릿 메시지 대신 **GPT가 자연스럽게 설명**합니다.

```
기존: "🏠 강남구 근처에서 공연해요!"
AI: "강남구에 거주하시는데 이 공연이 강남 블루스퀘어에서
     진행되어 접근성이 매우 좋아요! 게다가 최근 '엘리자벳'을
     찜하셨는데, 이 공연도 유럽 배경의 클래식 뮤지컬이라
     비슷한 감성을 느끼실 수 있을 거예요 😊"
```

### 구현 단계

#### Step 1: AI 설명 생성 함수

```python
# back/recommendations/utils/ai_explanation.py (신규 파일)

import openai
from django.conf import settings
from django.core.cache import cache

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_explanation(user, performance, score_breakdown):
    """
    GPT-5-mini로 추천 설명 생성

    Args:
        user: User 객체
        performance: Performance 객체
        score_breakdown: dict (f1~f6 점수)

    Returns:
        str: AI 생성 설명
    """
    # 캐싱 확인 (1시간)
    cache_key = f"ai_explanation_{user.id}_{performance.mt20id}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    # 점수 분석
    scores = {
        '위치': score_breakdown['f3'],
        '취향': score_breakdown['f2'],
        '최근 관심': score_breakdown['f1'],
        '인기도': score_breakdown['f4'],
        '임박도': score_breakdown['f5'],
        '유사성': score_breakdown['f6']
    }

    # 상위 3개 요인 추출
    top_factors = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    # 프롬프트 구성
    prompt = f"""당신은 공연 추천 큐레이터입니다. 사용자에게 추천 이유를 친근하게 설명해주세요.

사용자 정보:
- 이름: {user.username}
- 거주지: {user.region or '정보없음'}
- 선호 장르: {', '.join(user.preference_tags) if user.preference_tags else '정보없음'}

추천 공연:
- 제목: {performance.prfnm}
- 장르: {performance.genrenm}
- 지역: {performance.area}
- 공연장: {performance.fcltynm}

추천 주요 이유:
1. {top_factors[0][0]} (점수: {top_factors[0][1]:.2f})
2. {top_factors[1][0]} (점수: {top_factors[1][1]:.2f})
3. {top_factors[2][0]} (점수: {top_factors[2][1]:.2f})

위 정보를 바탕으로 이 공연을 추천하는 이유를 2-3문장으로 자연스럽게 설명해주세요.
친근한 말투로, 이모지 1-2개 사용."""

    try:
        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        explanation = response.choices[0].message.content.strip()

        # 캐싱 (1시간)
        cache.set(cache_key, explanation, timeout=3600)

        return explanation

    except Exception as e:
        print(f"AI 설명 생성 실패: {e}")
        # 실패 시 기본 메시지 반환
        return f"🎭 {performance.prfnm}을(를) 추천드립니다!"
```

---

#### Step 2: RecommendationEngine에 AI 설명 통합

```python
# back/recommendations/engine.py (수정)

from .utils.ai_explanation import generate_ai_explanation

class RecommendationEngine:
    # ... 기존 코드 ...

    def get_recommendations(self, top_n=10, use_ai_explanation=False):
        """
        Args:
            top_n (int): 추천 개수
            use_ai_explanation (bool): AI 설명 사용 여부
        """
        # ... 기존 코드 (점수 계산) ...

        # Top-N 추출 및 추천 사유 추가
        recommendations = []
        for item in scored_performances[:top_n]:
            performance = item['performance']
            breakdown = item['breakdown']

            # 기본 사유
            reason, reason_text = self._get_top_reason(breakdown, performance)

            recommendation = {
                'mt20id': performance.mt20id,
                'score': round(item['score'], 2),
                'reason': reason,
                'reason_text': reason_text
            }

            # AI 설명 추가 (옵션)
            if use_ai_explanation:
                recommendation['ai_explanation'] = generate_ai_explanation(
                    self.user,
                    performance,
                    breakdown
                )

            recommendations.append(recommendation)

        return recommendations
```

---

#### Step 3: API 수정

```python
# back/recommendations/api_views.py

class RecommendationViewSet(viewsets.ViewSet):
    # ... 기존 코드 ...

    def list(self, request):
        """
        추천 목록 조회

        Query Params:
            top_n: 개수 (기본: 10)
            use_ai: AI 설명 사용 (true/false, 기본: false)
        """
        top_n = int(request.query_params.get('top_n', 10))
        use_ai = request.query_params.get('use_ai', 'false').lower() == 'true'

        engine = RecommendationEngine(request.user)
        recommendations = engine.get_recommendations(
            top_n=top_n,
            use_ai_explanation=use_ai
        )

        # ... 나머지 코드 ...
```

**API 호출:**
```
# 기본 추천
GET /api/recommendations/?top_n=5

# AI 설명 포함
GET /api/recommendations/?top_n=5&use_ai=true
```

---

## 🔧 환경 설정

### 1. .env 파일

```bash
# back/.env
OPENAI_API_KEY=sk-proj-your-api-key-here
```

### 2. settings.py

```python
# back/mypjt/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 캐싱 설정 (선택)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### 3. requirements.txt

```txt
openai>=1.0.0
python-dotenv>=1.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

**설치:**
```bash
cd back
pip install -r requirements.txt
```

---

## 📋 구현 순서 체크리스트

### Phase 1: 환경 설정
- [ ] OpenAI API 키 발급
- [ ] .env 파일 생성 및 키 설정
- [ ] requirements.txt 패키지 설치
- [ ] settings.py 수정

### Phase 2: 의미 기반 검색
- [ ] Performance 모델에 embedding 필드 추가
- [ ] 마이그레이션 실행
- [ ] utils/embedding.py 생성
- [ ] generate_embeddings 명령 생성
- [ ] 임베딩 생성 실행 (테스트 10개)
- [ ] semantic_search API 구현
- [ ] API 테스트

### Phase 3: AI 추천 설명
- [ ] utils/ai_explanation.py 생성
- [ ] RecommendationEngine 수정
- [ ] API에 use_ai 파라미터 추가
- [ ] API 테스트

### Phase 4: 검증
- [ ] 의미 검색 정확도 확인
- [ ] AI 설명 품질 확인
- [ ] 캐싱 동작 확인
- [ ] 에러 핸들링 확인

---

## 🧪 테스트 예시

### 의미 검색 테스트

```bash
# 1. 임베딩 생성 (10개만)
python manage.py generate_embeddings --limit 10

# 2. API 호출
curl "http://localhost:8000/api/performances/semantic_search/?q=감동적인+로맨스&top_n=3"
```

**예상 응답:**
```json
{
  "query": "감동적인 로맨스",
  "count": 3,
  "results": [
    {
      "mt20id": "PF001",
      "prfnm": "뮤지컬 레베카",
      "genrenm": "뮤지컬",
      "similarity_score": 0.876
    },
    // ...
  ]
}
```

### AI 추천 설명 테스트

```bash
curl "http://localhost:8000/api/recommendations/?top_n=3&use_ai=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**예상 응답:**
```json
{
  "recommendations": [
    {
      "mt20id": "PF001",
      "score": 0.85,
      "reason": "location",
      "reason_text": "🏠 서울에서 공연해요!",
      "ai_explanation": "서울에 거주하시는데 이 공연이 강남 블루스퀘어에서 진행되어 접근성이 매우 좋아요! 게다가 최근 엘리자벳을 찜하셨는데, 이 공연도 유럽 배경의 클래식 뮤지컬이라 비슷한 감성을 느끼실 수 있을 거예요 😊"
    }
  ]
}
```

---

## 💡 최적화 팁

### 1. 캐싱 전략
- AI 설명: 1시간 캐싱 (동일 사용자-공연 조합)
- 임베딩: 영구 저장 (공연 정보 변경 시에만 재생성)

### 2. 비용 절감
- 상위 3개만 AI 설명 생성
- 나머지는 템플릿 사용
- Semantic Caching 활용 (GPT-5의 90% 할인)

### 3. 성능 향상
- 임베딩 DB 인덱싱
- 검색 시 배치 처리
- 결과 페이지네이션

---

## 📊 예상 비용 (GPT-5-mini + text-embedding-3-small)

### 월 사용자 1,000명 기준

| 작업 | 호출 수 | 비용 |
|------|---------|------|
| 공연 임베딩 (100개) | 100회 | $0.003 |
| 검색 임베딩 | 1,000회 | $0.02 |
| AI 추천 설명 | 3,000회 | $2.25 |
| **총계** | - | **약 $2.27** |

**6,000회 GPT 크레딧으로 약 2,666개월 사용 가능** ✅

---

## 🚀 다음 단계

이 문서 완료 후:
1. **협업 필터링 f6 강화** (임베딩 유사도 추가)
2. **리뷰 감정 분석 & 요약**
3. **대화형 추천 챗봇**

---

**작성일**: 2025-12-19
**버전**: 1.0
**작성자**: Claude Sonnet 4.5
