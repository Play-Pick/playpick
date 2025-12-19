"""
임베딩 전략 3: 맥시멈 (Maximum)
- 모든 정보 포함 (줄거리 전체, 제작진, 구조화된 형식)
- 최고 품질, 높은 비용
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


def generate_embedding_text_maximum(performance):
    """
    전략 3: 맥시멈
    모든 정보를 구조화된 형식으로 포함
    """
    parts = []

    # === 기본 정보 ===
    parts.append(f"제목: {performance.prfnm}")

    if performance.genrenm:
        parts.append(f"장르: {performance.genrenm}")

    if performance.cast_search_text:
        parts.append(f"출연: {performance.cast_search_text}")

    if performance.area:
        parts.append(f"지역: {performance.area}")

    if performance.fcltynm:
        parts.append(f"공연장: {performance.fcltynm}")

    if performance.prfstate:
        parts.append(f"상태: {performance.prfstate}")

    # === 상세 정보 ===
    try:
        if hasattr(performance, 'detail') and performance.detail:
            detail = performance.detail

            if detail.prfage:
                parts.append(f"관람연령: {detail.prfage}")

            if detail.prfruntime:
                parts.append(f"러닝타임: {detail.prfruntime}")

            if detail.entrpsnm:
                parts.append(f"제작사: {detail.entrpsnm}")

            if detail.prfcrew:
                parts.append(f"제작진: {detail.prfcrew}")

            # 줄거리 전체
            if detail.sty:
                parts.append(f"줄거리: {detail.sty}")

            if detail.pcseguidance:
                parts.append(f"가격: {detail.pcseguidance}")
    except:
        pass

    # 구조화된 형식으로 결합
    text = "\n".join(parts)

    # 빈 텍스트 방지
    if not text.strip():
        text = f"제목: {performance.prfnm}\n장르: {performance.genrenm}"

    return text


def test_strategy_3():
    """전략 3 테스트"""
    print("=" * 80)
    print("전략 3: 맥시멈 (Maximum)")
    print("포함 필드: 모든 정보 (줄거리 전체, 제작진, 가격 등)")
    print("=" * 80)

    # 테스트할 공연 5개 가져오기 (Detail 있는 것)
    performances = Performance.objects.filter(
        detail__isnull=False,
        detail__sty__isnull=False  # 줄거리 있는 것
    ).select_related('detail')[:5]

    if not performances.exists():
        print("❌ 줄거리가 있는 공연 데이터가 없습니다.")
        print("Detail 있는 공연으로 테스트합니다...")
        performances = Performance.objects.filter(
            detail__isnull=False
        ).select_related('detail')[:5]

    if not performances.exists():
        print("❌ 상세정보가 있는 공연이 없습니다.")
        return

    print(f"\n테스트 공연: {performances.count()}개\n")

    total_tokens = 0
    total_chars = 0

    for idx, perf in enumerate(performances, 1):
        text = generate_embedding_text_maximum(perf)

        # 토큰 수 추정
        estimated_tokens = len(text) // 2
        total_tokens += estimated_tokens
        total_chars += len(text)

        print(f"\n[{idx}] {perf.mt20id} - {perf.prfnm}")
        print("-" * 80)
        print(f"생성된 텍스트:")
        # 너무 길면 일부만 표시
        if len(text) > 500:
            print(text[:500])
            print(f"\n... (총 {len(text)}자 중 500자만 표시)")
        else:
            print(text)

        print(f"\n문자 수: {len(text)}자")
        print(f"예상 토큰: ~{estimated_tokens} tokens")
        print("-" * 80)

    # 통계
    avg_tokens = total_tokens // performances.count()
    avg_chars = total_chars // performances.count()

    print("\n" + "=" * 80)
    print("전략 3 통계")
    print("=" * 80)
    print(f"평균 문자 수: {avg_chars}자")
    print(f"평균 토큰 수: ~{avg_tokens} tokens")
    print(f"\n60,000개 임베딩 시:")
    print(f"  - 총 토큰: ~{avg_tokens * 60000:,} tokens")
    print(f"  - 비용 (실시간): ${avg_tokens * 60000 / 1000000 * 0.02:.4f}")
    print(f"  - 비용 (Batch 50% 할인): ${avg_tokens * 60000 / 1000000 * 0.01:.4f}")
    print("\n⚠️  주의사항:")
    print("  - 토큰 사용량이 많아 비용 증가")
    print("  - Detail 없는 공연은 정보 부족")
    print("  - 처리 시간 증가")
    print("\n💡 적합한 경우:")
    print("  - 최고 품질의 검색 필요")
    print("  - 비용이 문제되지 않음")
    print("  - 모든 공연에 상세정보 있음")
    print("=" * 80)

    # 실제 임베딩 생성 테스트
    print("\n실제 임베딩 생성 테스트를 진행하시겠습니까? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        print("\n첫 번째 공연으로 임베딩 생성 중...")
        test_perf = performances.first()
        text = generate_embedding_text_maximum(test_perf)

        try:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding

            print(f"✅ 임베딩 생성 성공!")
            print(f"   - 벡터 차원: {len(embedding)}")
            print(f"   - 벡터 샘플: {embedding[:5]}...")
            print(f"   - 실제 사용 토큰: {response.usage.total_tokens} tokens")
            print(f"   - 실제 비용: ${response.usage.total_tokens / 1000000 * 0.02:.6f}")

        except Exception as e:
            print(f"❌ 임베딩 생성 실패: {e}")


if __name__ == "__main__":
    test_strategy_3()
