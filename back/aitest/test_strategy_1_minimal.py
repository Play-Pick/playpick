"""
임베딩 전략 1: 미니멀 (Minimal)
- 제목 + 장르 + 출연진만 포함
- 가장 경제적, 빠름
"""

import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import Performance
from dotenv import load_dotenv
import openai

# 환경변수 로드
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_embedding_text_minimal(performance):
    """
    전략 1: 미니멀
    기본 정보만 포함
    """
    parts = [
        performance.prfnm,              # 제목
        performance.genrenm,            # 장르
        performance.cast_search_text,   # 출연진
    ]

    # None 제거 후 결합
    text = " ".join(filter(None, parts))
    return text


def test_strategy_1():
    """전략 1 테스트"""
    print("=" * 80)
    print("전략 1: 미니멀 (Minimal)")
    print("포함 필드: 제목, 장르, 출연진")
    print("=" * 80)

    # 테스트할 공연 5개 가져오기
    performances = Performance.objects.filter(
        cast_search_text__isnull=False
    ).select_related('detail')[:5]

    if not performances.exists():
        print("❌ 테스트할 공연 데이터가 없습니다.")
        return

    print(f"\n테스트 공연: {performances.count()}개\n")

    total_tokens = 0
    total_chars = 0

    for idx, perf in enumerate(performances, 1):
        text = generate_embedding_text_minimal(perf)

        # 토큰 수 추정 (영어: 4자당 1토큰, 한글: 2자당 1토큰)
        estimated_tokens = len(text) // 2
        total_tokens += estimated_tokens
        total_chars += len(text)

        print(f"\n[{idx}] {perf.mt20id} - {perf.prfnm}")
        print("-" * 80)
        print(f"생성된 텍스트:\n{text}")
        print(f"\n문자 수: {len(text)}자")
        print(f"예상 토큰: ~{estimated_tokens} tokens")
        print("-" * 80)

    # 통계
    avg_tokens = total_tokens // performances.count()
    avg_chars = total_chars // performances.count()

    print("\n" + "=" * 80)
    print("전략 1 통계")
    print("=" * 80)
    print(f"평균 문자 수: {avg_chars}자")
    print(f"평균 토큰 수: ~{avg_tokens} tokens")
    print(f"\n60,000개 임베딩 시:")
    print(f"  - 총 토큰: ~{avg_tokens * 60000:,} tokens")
    print(f"  - 비용 (실시간): ${avg_tokens * 60000 / 1000000 * 0.02:.4f}")
    print(f"  - 비용 (Batch 50% 할인): ${avg_tokens * 60000 / 1000000 * 0.01:.4f}")
    print("=" * 80)

    # 실제 임베딩 생성 테스트 (선택)
    print("\n실제 임베딩 생성 테스트를 진행하시겠습니까? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        print("\n첫 번째 공연으로 임베딩 생성 중...")
        test_perf = performances.first()
        text = generate_embedding_text_minimal(test_perf)

        try:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding

            print(f"✅ 임베딩 생성 성공!")
            print(f"   - 벡터 차원: {len(embedding)}")
            print(f"   - 벡터 샘플: {embedding[:5]}...")
            print(f"   - 사용 토큰: {response.usage.total_tokens} tokens")

        except Exception as e:
            print(f"❌ 임베딩 생성 실패: {e}")


if __name__ == "__main__":
    test_strategy_1()
