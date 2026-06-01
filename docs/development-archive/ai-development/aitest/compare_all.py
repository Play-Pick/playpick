"""
3가지 임베딩 전략 비교 스크립트
한 번에 모든 전략의 결과를 비교합니다.
"""

import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import Performance


def generate_minimal(perf):
    """전략 1: 미니멀"""
    parts = [
        perf.prfnm,
        perf.genrenm,
        perf.cast_search_text,
    ]
    return " ".join(filter(None, parts))


def generate_standard(perf):
    """전략 2: 스탠다드"""
    parts = []

    if perf.prfnm:
        parts.append(perf.prfnm)
    if perf.genrenm:
        parts.append(perf.genrenm)
    if perf.cast_search_text:
        parts.append(perf.cast_search_text)
    if perf.area:
        parts.append(perf.area)
    if perf.fcltynm:
        parts.append(perf.fcltynm)

    try:
        if hasattr(perf, 'detail') and perf.detail:
            detail = perf.detail
            if detail.prfage:
                parts.append(f"관람연령 {detail.prfage}")
            if detail.prfruntime:
                parts.append(f"러닝타임 {detail.prfruntime}")
            if detail.entrpsnm:
                parts.append(f"제작 {detail.entrpsnm}")
            if detail.sty:
                parts.append(detail.sty[:200].strip())
    except:
        pass

    text = " ".join(parts)
    return text if text.strip() else f"{perf.prfnm} {perf.genrenm}"


def generate_maximum(perf):
    """전략 3: 맥시멈"""
    parts = [f"제목: {perf.prfnm}"]

    if perf.genrenm:
        parts.append(f"장르: {perf.genrenm}")
    if perf.cast_search_text:
        parts.append(f"출연: {perf.cast_search_text}")
    if perf.area:
        parts.append(f"지역: {perf.area}")
    if perf.fcltynm:
        parts.append(f"공연장: {perf.fcltynm}")
    if perf.prfstate:
        parts.append(f"상태: {perf.prfstate}")

    try:
        if hasattr(perf, 'detail') and perf.detail:
            detail = perf.detail
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
    except:
        pass

    return "\n".join(parts)


def compare_strategies():
    """3가지 전략 비교"""
    print("=" * 100)
    print(" " * 30 + "임베딩 전략 비교 테스트")
    print("=" * 100)

    # 테스트 공연 가져오기
    performances = Performance.objects.select_related('detail')[:5]

    if not performances.exists():
        print("❌ 테스트할 공연 데이터가 없습니다.")
        return

    print(f"\n테스트 공연: {performances.count()}개")
    print("-" * 100)

    # 각 전략별 통계
    stats = {
        '전략 1 (Minimal)': {'tokens': [], 'chars': []},
        '전략 2 (Standard)': {'tokens': [], 'chars': []},
        '전략 3 (Maximum)': {'tokens': [], 'chars': []},
    }

    # 공연별 비교
    for idx, perf in enumerate(performances, 1):
        print(f"\n[공연 {idx}] {perf.mt20id} - {perf.prfnm}")
        print("-" * 100)

        # 전략 1
        text1 = generate_minimal(perf)
        tokens1 = len(text1) // 2
        stats['전략 1 (Minimal)']['tokens'].append(tokens1)
        stats['전략 1 (Minimal)']['chars'].append(len(text1))
        print(f"\n전략 1 (Minimal): {len(text1)}자, ~{tokens1} tokens")
        print(f"  {text1[:100]}{'...' if len(text1) > 100 else ''}")

        # 전략 2
        text2 = generate_standard(perf)
        tokens2 = len(text2) // 2
        stats['전략 2 (Standard)']['tokens'].append(tokens2)
        stats['전략 2 (Standard)']['chars'].append(len(text2))
        print(f"\n전략 2 (Standard): {len(text2)}자, ~{tokens2} tokens")
        print(f"  {text2[:100]}{'...' if len(text2) > 100 else ''}")

        # 전략 3
        text3 = generate_maximum(perf)
        tokens3 = len(text3) // 2
        stats['전략 3 (Maximum)']['tokens'].append(tokens3)
        stats['전략 3 (Maximum)']['chars'].append(len(text3))
        print(f"\n전략 3 (Maximum): {len(text3)}자, ~{tokens3} tokens")
        print(f"  {text3[:100]}{'...' if len(text3) > 100 else ''}")

        print("-" * 100)

    # 최종 통계 비교
    print("\n" + "=" * 100)
    print(" " * 35 + "최종 통계 비교")
    print("=" * 100)

    print(f"\n{'전략':<20} {'평균 문자':<15} {'평균 토큰':<15} {'60,000개 비용 (실시간)':<25} {'60,000개 비용 (Batch)':<20}")
    print("-" * 100)

    for strategy_name, data in stats.items():
        avg_chars = sum(data['chars']) // len(data['chars'])
        avg_tokens = sum(data['tokens']) // len(data['tokens'])
        cost_realtime = avg_tokens * 60000 / 1000000 * 0.02
        cost_batch = avg_tokens * 60000 / 1000000 * 0.01

        marker = " ✨ 추천" if "Standard" in strategy_name else ""
        print(f"{strategy_name:<20} {avg_chars:<15} {avg_tokens:<15} ${cost_realtime:<24.4f} ${cost_batch:<19.4f}{marker}")

    print("=" * 100)

    # 추천 사항
    print("\n" + "🎯 추천: 전략 2 (Standard)")
    print("\n이유:")
    print("  ✅ 상세 검색 가능 (분위기, 테마 파악)")
    print("  ✅ 여전히 저렴한 비용")
    print("  ✅ Detail 없어도 기본 동작")
    print("  ✅ 대부분의 검색 시나리오 커버")
    print("\n다른 전략 선택 기준:")
    print("  - 전략 1: 비용이 최우선이고 기본 검색만 필요")
    print("  - 전략 3: 비용 상관없고 최고 품질의 검색 필요")
    print("=" * 100)

    # 개별 테스트 안내
    print("\n\n개별 전략 테스트:")
    print("  python aitest/test_strategy_1_minimal.py   - 전략 1 상세 테스트")
    print("  python aitest/test_strategy_2_standard.py  - 전략 2 상세 테스트 (추천)")
    print("  python aitest/test_strategy_3_maximum.py   - 전략 3 상세 테스트")
    print("\n각 스크립트에서 실제 OpenAI API 호출 테스트도 가능합니다.")
    print("=" * 100)


if __name__ == "__main__":
    compare_strategies()
