from django.core.management.base import BaseCommand
from django.db import transaction
from performances.models import Performance
from .utils.kopis_client import KopisAPIClient
from .utils.date_helper import split_date_range
from .utils.logger import CollectionLogger
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional


class Command(BaseCommand):
    help = 'KOPIS API에서 3년치 공연 데이터 수집 (2023-01-01 ~ 2025-11-29)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='수집 시작일 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2025-11-29',
            help='수집 종료일 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--chunk-days',
            type=int,
            default=31,
            help='기간 분할 단위 (기본 31일)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='트랜잭션 배치 크기'
        )

    def handle(self, *args, **options):
        # 1. 환경 변수 로드
        load_dotenv()
        api_key = os.getenv('KOPIS_API')

        if not api_key:
            self.stdout.write(self.style.ERROR('KOPIS_API 키가 .env 파일에 없습니다.'))
            self.stdout.write(self.style.WARNING('09-pjt/.env 파일을 확인하고 KOPIS_API 값을 설정해주세요.'))
            return

        # 2. 초기화
        client = KopisAPIClient(api_key)
        logger = CollectionLogger('collect_performances')

        # 3. 날짜 범위 분할
        start_date = options['start_date']
        end_date = options['end_date']
        chunk_days = options['chunk_days']

        date_ranges = split_date_range(start_date, end_date, chunk_days)
        logger.stats['total_periods'] = len(date_ranges)

        self.stdout.write(
            self.style.SUCCESS(f'총 {len(date_ranges)}개 기간으로 분할하여 수집 시작...\n')
        )

        # 4. 각 기간별 데이터 수집
        for idx, (period_start, period_end) in enumerate(date_ranges, 1):
            logger.log_period_start(period_start, period_end, idx, len(date_ranges))
            self.stdout.write(f'\n[{idx}/{len(date_ranges)}] 기간: {period_start} ~ {period_end}')

            try:
                # API 호출
                performances = client.fetch_all_performances(
                    period_start,
                    period_end,
                    callback=lambda p, tp, c: self._log_progress(p, tp, c)
                )

                # DB 저장
                self._save_performances(performances, logger, options['batch_size'])

                logger.log_period_complete(period_start, period_end, len(performances))
                self.stdout.write(self.style.SUCCESS(f'  기간 수집 완료: {len(performances)}건\n'))

            except Exception as e:
                logger.log_error(f'기간 {period_start}~{period_end} 수집 실패', e)
                self.stdout.write(
                    self.style.ERROR(f'  기간 수집 실패: {period_start}~{period_end} - {str(e)}\n')
                )
                continue

        # 5. 최종 통계 출력
        summary = logger.get_summary()
        self.stdout.write(self.style.SUCCESS(summary))

    def _save_performances(self, performances: List[Dict], logger: CollectionLogger, batch_size: int):
        """공연 데이터 DB 저장"""
        for i in range(0, len(performances), batch_size):
            batch = performances[i:i+batch_size]

            with transaction.atomic():
                for perf_data in batch:
                    try:
                        mt20id = perf_data.get('mt20id')
                        if not mt20id:
                            continue

                        # 날짜 형식 변환
                        date_from = self._format_date(perf_data.get('prfpdfrom'))
                        date_to = self._format_date(perf_data.get('prfpdto'))

                        defaults = {
                            'prfnm': perf_data.get('prfnm'),
                            'prfpdfrom': date_from,
                            'prfpdto': date_to,
                            'fcltynm': perf_data.get('fcltynm'),
                            'poster': perf_data.get('poster'),
                            'area': perf_data.get('area'),
                            'genrenm': perf_data.get('genrenm'),
                            'prfstate': perf_data.get('prfstate'),
                            'openrun': perf_data.get('openrun'),
                        }

                        obj, created = Performance.objects.update_or_create(
                            mt20id=mt20id,
                            defaults=defaults
                        )

                        logger.log_save_result(created, mt20id)

                    except Exception as e:
                        logger.log_error(f'저장 실패: {mt20id}', e)
                        logger.stats['failed'] += 1

    def _format_date(self, date_str: Optional[str]) -> Optional[str]:
        """날짜 형식 변환: YYYY.MM.DD → YYYY-MM-DD"""
        if date_str:
            return date_str.replace('.', '-')
        return None

    def _log_progress(self, page: int, total_pages: int, count: int):
        """진행 상황 출력"""
        self.stdout.write(f'  페이지 {page}/{total_pages} 처리 중... (현재까지 {count}건)')
