import logging
from django.utils import timezone
from datetime import timedelta


class CollectionLogger:
    """데이터 수집 로거"""

    def __init__(self, command_name: str):
        self.logger = logging.getLogger(command_name)
        self.stats = {
            'created': 0,
            'updated': 0,
            'failed': 0,
            'total_periods': 0,
            'current_period': 0,
            'start_time': timezone.now(),
        }

    def log_period_start(self, start_date: str, end_date: str, period_num: int, total_periods: int):
        """기간 수집 시작 로그"""
        self.stats['current_period'] = period_num
        self.stats['total_periods'] = total_periods
        message = f"[{period_num}/{total_periods}] 기간: {start_date} ~ {end_date}"
        self.logger.info(message)

    def log_period_complete(self, start_date: str, end_date: str, count: int):
        """기간 수집 완료 로그"""
        message = f"기간 수집 완료: {start_date} ~ {end_date} ({count}건)"
        self.logger.info(message)

    def log_save_result(self, created: bool, mt20id: str):
        """개별 저장 결과 로그"""
        if created:
            self.stats['created'] += 1
        else:
            self.stats['updated'] += 1

    def log_error(self, message: str, error: Exception):
        """에러 로그"""
        self.stats['failed'] += 1
        error_message = f"{message}: {str(error)}"
        self.logger.error(error_message)

    def _get_current_time(self):
        """현재 시간 반환 (타임스탬프)"""
        return timezone.now().timestamp()

    @property
    def start_time(self):
        """시작 시간 (타임스탬프)"""
        return self.stats['start_time'].timestamp()

    def get_summary(self) -> str:
        """최종 요약 통계"""
        end_time = timezone.now()
        duration = end_time - self.stats['start_time']

        # 총 처리 건수
        total_processed = self.stats['created'] + self.stats['updated']

        # 평균 처리 속도
        if duration.total_seconds() > 0:
            rate = total_processed / duration.total_seconds()
        else:
            rate = 0

        # 소요 시간을 읽기 쉽게 포맷팅
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            duration_str = f"{int(hours)}시간 {int(minutes)}분 {int(seconds)}초"
        elif minutes > 0:
            duration_str = f"{int(minutes)}분 {int(seconds)}초"
        else:
            duration_str = f"{int(seconds)}초"

        summary = f"""
=== 최종 통계 ===
총 소요 시간: {duration_str}
생성: {self.stats['created']:,}건
업데이트: {self.stats['updated']:,}건
실패: {self.stats['failed']:,}건
처리 속도: 약 {rate:.2f}건/초
"""
        return summary
