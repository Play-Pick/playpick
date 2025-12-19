from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.core.management import call_command


class Command(BaseCommand):
    help = '주간 업데이트: 최근 7일치 공연 데이터 수집'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='수집할 일수 (기본 7일)'
        )

    def handle(self, *args, **options):
        # 1. 날짜 계산
        end_date = datetime.now()
        start_date = end_date - timedelta(days=options['days'])

        self.stdout.write(
            self.style.SUCCESS(
                f'{start_date.strftime("%Y-%m-%d")} ~ {end_date.strftime("%Y-%m-%d")} 업데이트 시작...\n'
            )
        )

        # 2. collect_performances 커맨드 호출
        call_command(
            'collect_performances',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            chunk_days=options['days'],  # 전체 기간을 한 번에 처리
            batch_size=100,
            stdout=self.stdout,
            stderr=self.stderr,
        )
