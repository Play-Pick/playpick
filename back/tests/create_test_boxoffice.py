"""
테스트용 박스오피스 랭킹 데이터 생성 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import Performance, BoxOfficeRanking, GENRE_DISPLAY_ORDER, GENRE_CODE_MAPPING
from datetime import date

def create_test_boxoffice_data():
    """각 장르별로 상위 20개 공연으로 테스트 랭킹 생성"""

    print("테스트 박스오피스 데이터 생성 시작...\n")

    today = date.today()
    total_created = 0

    # 기존 테스트 데이터 삭제
    deleted_count = BoxOfficeRanking.objects.filter(ranking_date=today).delete()[0]
    print(f"기존 데이터 {deleted_count}건 삭제\n")

    for genre_code in GENRE_DISPLAY_ORDER:
        genre_name = GENRE_CODE_MAPPING[genre_code]
        print(f"[{genre_name}] 랭킹 생성 중...")

        # 해당 장르의 공연 중인 공연 조회 (최대 20개)
        # 장르명 매핑: 뮤지컬, 연극, 클래식, 대중음악, 무용
        genre_filter_map = {
            'BBBC': '뮤지컬',
            'AAAA': '연극',
            'CCCA': '클래식',
            'GGGA': '대중콘서트',  # DB에는 이렇게 저장되어 있을 수 있음
            'CCCD': '무용',
        }

        genre_kr = genre_filter_map.get(genre_code, genre_name)

        # 공연 중인 것 우선, 없으면 전체에서
        performances = Performance.objects.filter(
            genrenm__icontains=genre_kr,
            prfstate='공연중'
        )[:20]

        # 공연중인 것이 없으면 전체에서
        if performances.count() == 0:
            performances = Performance.objects.filter(
                genrenm__icontains=genre_kr
            )[:20]

        # 장르명으로도 없으면 아무 공연이나
        if performances.count() == 0:
            print(f"  경고: {genre_name} 장르의 공연이 없어 전체에서 선택합니다.")
            performances = Performance.objects.all()[:20]

        created_count = 0
        for idx, perf in enumerate(performances, 1):
            BoxOfficeRanking.objects.create(
                performance=perf,
                rank=idx,
                genre_code=genre_code,
                ranking_date=today,
                period_type='week',
                area=perf.area or '서울',
                seat_count=1000 - (idx * 30),  # 순위가 낮을수록 적음
                performance_count=50 - idx,
            )
            created_count += 1

        total_created += created_count
        print(f"  {genre_name}: {created_count}건 생성 완료")

    print(f"\n총 {total_created}건의 테스트 랭킹 데이터 생성 완료!")
    print(f"날짜: {today}")

    # 결과 확인
    print("\n=== 생성된 데이터 확인 ===")
    for genre_code in GENRE_DISPLAY_ORDER:
        genre_name = GENRE_CODE_MAPPING[genre_code]
        count = BoxOfficeRanking.objects.filter(
            genre_code=genre_code,
            ranking_date=today
        ).count()
        print(f"{genre_name}: {count}건")

if __name__ == '__main__':
    create_test_boxoffice_data()
