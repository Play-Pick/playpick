"""
임베딩 전략 2: 스탠다드 (Standard)
- 기본 정보 + 상세 정보 + 줄거리 일부
- 품질과 비용 균형 (추천)
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


def generate_embedding_text_standard(performance):
    """
    전략 2: 스탠다드
    기본 정보 + 상세 정보 + 줄거리 일부
    """
    parts = []

    # === 기본 정보 ===
    if performance.prfnm:
        parts.append(performance.prfnm)
    if performance.genrenm:
        parts.append(performance.genrenm)
    if performance.cast_search_text:
        parts.append(performance.cast_search_text)
    if performance.area:
        parts.append(performance.area)
    if performance.fcltynm:
        parts.append(performance.fcltynm)

    # === 상세 정보 ===
    try:
        if hasattr(performance, 'detail') and performance.detail:
            detail = performance.detail

            if detail.prfage:
                parts.append(f"관람연령 {detail.prfage}")
            if detail.prfruntime:
                parts.append(f"러닝타임 {detail.prfruntime}")
            if detail.entrpsnm:
                parts.append(f"제작 {detail.entrpsnm}")
            # 줄거리 (200자까지)
            if detail.sty:
                summary = detail.sty[:200].strip()
                if summary:
                    parts.append(summary)
    except Exception:
        pass

    # 결합
    text = " ".join(parts)

    # 빈 텍스트 방지
    if not text.strip():
        text = f"{performance.prfnm} {performance.genrenm}"

    return text


def test_strategy_2():
    """전략 2 테스트"""
    print("=" * 80)
    print("전략 2: 스탠다드 (Standard) - 균형형")
    print("포함 필드: 제목, 장르, 출연진, 지역, 공연장, 관람연령, 러닝타임, 제작, 줄거리 200자")
    print("=" * 80)

    # 테스트할 공연 5개 가져오기 (Detail 있는 것 우선)
    performances_qs = Performance.objects.filter(
        detail__isnull=False
    ).select_related('detail').order_by('pk')
    performances = list(performances_qs[:5])

    if not performances:
        print("상세정보가 있는 공연 데이터가 없습니다.")
        print("Detail 없는 공연으로 테스트합니다...")
        performances = list(
            Performance.objects.all().order_by('pk')[:5]
        )

    if not performances:
        print("❌ 테스트할 공연 데이터가 없습니다.")
        return

    print(f"\n테스트할 공연: {len(performances)}개\n")

    total_tokens = 0
    total_chars = 0

    for idx, perf in enumerate(performances, 1):
        text = generate_embedding_text_standard(perf)

        # 토큰 수 추정
        estimated_tokens = len(text) // 2
        total_tokens += estimated_tokens
        total_chars += len(text)

        print(f"\n[{idx}] {perf.mt20id} - {perf.prfnm}")
        print("-" * 80)
        print("생성된 텍스트")
        print(text)
        print(f"\n문자 수 {len(text)}자")
        print(f"추정 토큰: ~{estimated_tokens} tokens")

        # Detail 정보 여부 표시
        has_detail = hasattr(perf, 'detail') and perf.detail
        print(f"상세정보: {'있음' if has_detail else '없음'}")
        print("-" * 80)

    # 통계
    avg_tokens = total_tokens // len(performances)
    avg_chars = total_chars // len(performances)

    print("\n" + "=" * 80)
    print("전략 2 통계")
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
        text = generate_embedding_text_standard(test_perf)

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
    test_strategy_2()
