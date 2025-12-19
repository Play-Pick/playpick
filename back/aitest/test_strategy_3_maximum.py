"""
임베딩 전략 3: 맥시멈 (Maximum)
- 모든 정보를 포함 (줄거리 전체, 제작진 구조화된 형식)
- 최고 품질, 다소 높은 비용
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
from openai import OpenAI

# 환경변수 로드
load_dotenv()
client = OpenAI(
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
    api_key=os.getenv("GMS_KEY"),
)


def generate_embedding_text_maximum(performance):
    """
    전략 3: 맥시멈
    가능한 모든 정보를 구조화된 포맷으로 포함
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
            if detail.sty:
                parts.append(f"줄거리: {detail.sty}")
            if detail.pcseguidance:
                parts.append(f"가격: {detail.pcseguidance}")
    except Exception:
        pass

    text = "\n".join(parts)

    # 빈 텍스트 방지
    if not text.strip():
        text = f"제목: {performance.prfnm}\n장르: {performance.genrenm}"

    return text


def test_strategy_3():
    """전략 3 테스트"""
    print("=" * 80)
    print("전략 3: 맥시멈 (Maximum)")
    print("포함 필드: 모든 정보(줄거리 전체, 제작진, 가격 등)")
    print("=" * 80)

    # 테스트할 공연 5개 가져오기 (줄거리 있는 Detail 우선)
    performances_qs = Performance.objects.filter(
        detail__isnull=False,
        detail__sty__isnull=False
    ).select_related('detail').order_by('pk')
    performances = list(performances_qs[:5])

    if not performances:
        print("줄거리가 있는 공연 데이터가 없습니다.")
        print("Detail만 있는 공연으로 테스트합니다...")
        performances = list(
            Performance.objects.filter(detail__isnull=False)
            .select_related('detail')
            .order_by('pk')[:5]
        )

    if not performances:
        print("❌ 테스트할 공연 데이터가 없습니다.")
        return

    print(f"\n테스트할 공연: {len(performances)}개\n")

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
        print("생성된 텍스트")
        if len(text) > 500:
            print(text[:500])
            print(f"\n... (총 {len(text)}자 중 앞 500자만 표시)")
        else:
            print(text)

        print(f"\n문자 수 {len(text)}자")
        print(f"추정 토큰: ~{estimated_tokens} tokens")
        print("-" * 80)

    # 통계
    avg_tokens = total_tokens // len(performances)
    avg_chars = total_chars // len(performances)

    print("\n" + "=" * 80)
    print("전략 3 통계")
    print("=" * 80)
    print(f"평균 문자 수 {avg_chars}자")
    print(f"평균 토큰 수 ~{avg_tokens} tokens")
    print(f"\n60,000건 임베딩 시")
    print(f"  - 총토큰: ~{avg_tokens * 60000:,} tokens")
    print(f"  - 비용 (실시간): ${avg_tokens * 60000 / 1000000 * 0.02:.4f}")
    print(f"  - 비용 (Batch 50% 할인): ${avg_tokens * 60000 / 1000000 * 0.01:.4f}")
    print("=" * 80)

    # 실제 임베딩 생성 테스트(선택)
    print("\n실제 임베딩 생성 테스트를 진행하시겠습니까? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        print("\n첫번째 공연으로 임베딩 생성 시도...")
        test_perf = performances[0]
        text = generate_embedding_text_maximum(test_perf)

        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding

            print(f"✅ 임베딩 생성 성공!")
            print(f"   - 벡터 차원: {len(embedding)}")
            print(f"   - 벡터 샘플: {embedding[:5]}...")
            print(f"   - 사용 토큰: {response.usage.total_tokens} tokens")
            print(f"   - 비용(실시간 가정): ${response.usage.total_tokens / 1000000 * 0.02:.6f}")

        except Exception as e:
            print(f"❌ 임베딩 생성 실패: {e}")


if __name__ == "__main__":
    test_strategy_3()
