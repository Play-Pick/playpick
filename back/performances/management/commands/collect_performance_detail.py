from django.core.management.base import BaseCommand
from django.db import transaction
from performances.models import Performance, PerformanceDetail, PerformanceImage
from .utils.kopis_client import KopisAPIClient
from .utils.logger import CollectionLogger
from dotenv import load_dotenv
import os


class Command(BaseCommand):
    help = 'KOPIS 공연 상세 정보 수집'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mt20id',
            type=str,
            help='특정 공연 ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='전체 공연 수집'
        )
        parser.add_argument(
            '--missing-only',
            action='store_true',
            help='상세 정보가 없는 공연만 수집 (기본값)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='수집 개수 제한 (테스트용)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='배치 크기 (기본: 100)'
        )

    def handle(self, *args, **options):
        # 환경 변수 로드
        load_dotenv()
        api_key = os.getenv('KOPIS_API')

        if not api_key:
            self.stdout.write(self.style.ERROR('KOPIS_API 키가 설정되지 않았습니다.'))
            return

        client = KopisAPIClient(api_key)
        logger = CollectionLogger('collect_performance_detail')

        # 수집 대상 결정
        if options['mt20id']:
            performances = Performance.objects.filter(mt20id=options['mt20id'])
        elif options['all']:
            performances = Performance.objects.all()
        else:
            # 기본: 상세 정보 없는 공연만
            performances = Performance.objects.filter(detail__isnull=True)

        # Limit 적용
        if options.get('limit'):
            performances = performances[:options['limit']]

        total_count = performances.count()
        batch_size = options['batch_size']

        self.stdout.write(
            self.style.SUCCESS(f'\n=== 공연 상세 정보 수집 시작 ===')
        )
        self.stdout.write(f'총 수집 대상: {total_count}건')
        self.stdout.write(f'배치 크기: {batch_size}건')
        self.stdout.write(f'예상 소요 시간: 약 {total_count * 0.15 / 60:.1f}분\n')

        success_count = 0
        batch_count = 0
        batch_start_time = logger.start_time

        for idx, performance in enumerate(performances, 1):
            try:
                # 진행 상황 표시 (간결하게)
                if idx % 10 == 0 or idx == 1:
                    elapsed = (logger._get_current_time() - logger.start_time)
                    avg_speed = idx / elapsed if elapsed > 0 else 0
                    remaining = (total_count - idx) / avg_speed if avg_speed > 0 else 0
                    self.stdout.write(
                        f'[{idx}/{total_count}] 진행중... '
                        f'(성공: {success_count}, 속도: {avg_speed:.1f}건/초, 남은시간: {remaining/60:.1f}분)'
                    )

                # API 호출
                detail_data = client.fetch_performance_detail(performance.mt20id)

                # DB 저장
                self._save_detail_data(performance, detail_data, logger)

                success_count += 1

                # 배치 단위 커밋 확인
                if idx % batch_size == 0:
                    batch_count += 1
                    batch_elapsed = logger._get_current_time() - batch_start_time
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [OK] 배치 {batch_count} 완료 ({batch_size}건, {batch_elapsed:.1f}초 소요)'
                        )
                    )
                    batch_start_time = logger._get_current_time()

            except Exception as e:
                error_msg = str(e)
                # 에러 메시지 간소화
                if len(error_msg) > 100:
                    error_msg = error_msg[:100] + '...'
                logger.log_error(f'{performance.mt20id} 수집 실패', e)

                # 주요 에러만 출력
                if 'API' in error_msg or 'XML' in error_msg:
                    self.stdout.write(
                        self.style.WARNING(f'  [WARN] [{idx}] {performance.mt20id}: {error_msg}')
                    )
                continue

        # 최종 결과
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'[완료] 총 {success_count}건 수집 완료 ({total_count}건 중)')
        )
        self.stdout.write('='*60 + '\n')
        self.stdout.write(logger.get_summary())

    def _convert_date(self, date_str):
        """날짜 형식 변환: YYYY.MM.DD -> YYYY-MM-DD"""
        if not date_str:
            return None
        return date_str.replace('.', '-')

    @transaction.atomic
    def _save_detail_data(self, performance, detail_data, logger):
        """상세 정보 저장"""

        # Performance 기본 정보 업데이트
        if detail_data.get('prfnm'):
            performance.prfnm = detail_data['prfnm']
        if detail_data.get('poster'):
            performance.poster = detail_data['poster']
        if detail_data.get('genrenm'):
            performance.genrenm = detail_data['genrenm']
        if detail_data.get('prfpdfrom'):
            performance.prfpdfrom = self._convert_date(detail_data['prfpdfrom'])
        if detail_data.get('prfpdto'):
            performance.prfpdto = self._convert_date(detail_data['prfpdto'])
        if detail_data.get('fcltynm'):
            performance.fcltynm = detail_data['fcltynm']
        performance.save()

        # PerformanceDetail 생성/업데이트
        detail, created = PerformanceDetail.objects.update_or_create(
            performance=performance,
            defaults={
                'prfcast': detail_data.get('prfcast', ''),
                'prfcrew': detail_data.get('prfcrew', ''),
                'prfruntime': detail_data.get('prfruntime', ''),
                'prfage': detail_data.get('prfage', ''),
                'entrpsnm': detail_data.get('entrpsnm', ''),
                'pcseguidance': detail_data.get('pcseguidance', ''),
                'sty': detail_data.get('sty', ''),
                'dtguidance': detail_data.get('dtguidance', ''),
                'relates': detail_data.get('relates', []),
            }
        )

        if created:
            logger.stats['created'] += 1
        else:
            logger.stats['updated'] += 1

        # PerformanceImage 처리
        styurls = detail_data.get('styurls', [])
        if styurls:
            # 기존 이미지 삭제
            PerformanceImage.objects.filter(performance=performance).delete()

            # 새 이미지 생성
            for idx, url in enumerate(styurls):
                PerformanceImage.objects.create(
                    performance=performance,
                    image_url=url,
                    order=idx
                )
