from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from performances.models import Performance, BoxOfficeRanking, GENRE_CODE_MAPPING, GENRE_DISPLAY_ORDER
from .utils.kopis_client import KopisAPIClient
from .utils.logger import CollectionLogger
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'KOPIS 예매상황판 데이터 수집 (주간 기준)'

    # 수집할 장르 목록
    GENRE_CODES = GENRE_DISPLAY_ORDER

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='수집 날짜 (YYYYMMDD), 기본값: 오늘'
        )
        parser.add_argument(
            '--period',
            type=str,
            default='week',
            choices=['day', 'week', 'month'],
            help='기간 유형'
        )

    def handle(self, *args, **options):
        # 환경 변수 로드
        load_dotenv()
        api_key = os.getenv('KOPIS_API')

        if not api_key:
            self.stdout.write(self.style.ERROR('KOPIS_API 키가 설정되지 않았습니다.'))
            return

        # 날짜 설정
        if options['date']:
            target_date = options['date']
        else:
            target_date = datetime.now().strftime('%Y%m%d')
        print(target_date)
        period_type = options['period']

        client = KopisAPIClient(api_key)
        logger = CollectionLogger('collect_boxoffice')

        self.stdout.write(
            self.style.SUCCESS(f'\n박스오피스 데이터 수집 시작')
        )
        self.stdout.write(f'날짜: {target_date}, 기간유형: {period_type}\n')

        # 장르별 수집
        total_collected = 0

        for genre_code in self.GENRE_CODES:
            genre_name = GENRE_CODE_MAPPING.get(genre_code, genre_code)
            self.stdout.write(f'\n[{genre_name}] 수집 중...')
            # print('호출하는 날짜', target_date)
            try:
                # API 호출
                result = client.fetch_boxoffice(
                    date=target_date,
                    genre_code=genre_code,
                    period_type=period_type
                )

                boxoffice_list = result.get('boxoffice_list', [])
                base_date = result.get('base_date', target_date)

                # DB 저장
                saved_count = self._save_boxoffice_data(
                    boxoffice_list,
                    genre_code,
                    base_date,
                    period_type,
                    logger
                )

                total_collected += saved_count

                self.stdout.write(
                    self.style.SUCCESS(f'  {genre_name}: {saved_count}건 저장')
                )

            except Exception as e:
                logger.log_error(f'{genre_name} 수집 실패', e)
                self.stdout.write(
                    self.style.ERROR(f'  {genre_name} 실패: {str(e)}')
                )
                continue

        # 최종 결과
        self.stdout.write(
            self.style.SUCCESS(f'\n총 {total_collected}건 수집 완료\n')
        )

        summary = logger.get_summary()
        self.stdout.write(summary)

    def _save_boxoffice_data(
        self,
        boxoffice_list,
        genre_code,
        base_date,
        period_type,
        logger
    ):
        """박스오피스 데이터 DB 저장"""
        saved_count = 0

        # 날짜 변환: YYYY-MM-DD~YYYY-MM-DD -> YYYY-MM-DD
        ranking_date = self._parse_date(base_date)

        with transaction.atomic():
            # 기존 데이터 삭제 (같은 날짜, 같은 장르)
            BoxOfficeRanking.objects.filter(
                ranking_date=ranking_date,
                genre_code=genre_code,
                period_type=period_type
            ).delete()

            for item in boxoffice_list:
                try:
                    # 공연 ID 조회
                    mt20id = item.get('mt20id')
                    if not mt20id:
                        continue

                    # Performance 객체 조회 또는 생성
                    performance, created = Performance.objects.get_or_create(
                        mt20id=mt20id,
                        defaults={
                            'prfnm': item.get('prfnm', ''),
                        }
                    )

                    # 공연 정보 업데이트
                    if item.get('prfnm'):
                        performance.prfnm = item.get('prfnm')
                    if item.get('poster'):
                        performance.poster = item.get('poster')
                    if item.get('genrenm'):
                        performance.genrenm = item.get('genrenm')
                    performance.save()

                    # BoxOfficeRanking 생성
                    BoxOfficeRanking.objects.create(
                        performance=performance,
                        rank=int(item.get('rnum', 0)),
                        genre_code=genre_code,
                        ranking_date=ranking_date,
                        period_type=period_type,
                        area=item.get('area'),
                        seat_count=int(item.get('seatcnt', 0) or 0),
                        performance_count=int(item.get('prfdtcnt', 0) or 0),
                    )

                    saved_count += 1
                    logger.stats['created'] += 1

                except Exception as e:
                    logger.log_error(f'저장 실패: {mt20id}', e)
                    logger.stats['failed'] += 1
                    continue

        return saved_count

    def _parse_date(self, date_str):
        """날짜 문자열 파싱: YYYY-MM-DD~YYYY-MM-DD -> YYYY-MM-DD"""
        if not date_str:
            # 날짜가 없으면 오늘 날짜 사용
            return datetime.now().strftime('%Y-%m-%d')

        if '~' in date_str:
            # 기간의 종료일을 사용
            date_str = date_str.split('~')[1].strip()

        # YYYY-MM-DD 형식으로 변환
        if '-' in date_str:
            return date_str
        else:
            # YYYYMMDD -> YYYY-MM-DD
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
