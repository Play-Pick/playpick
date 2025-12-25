from datetime import datetime, timedelta
from typing import List, Tuple


def split_date_range(start_date: str, end_date: str, chunk_days: int = 31) -> List[Tuple[str, str]]:
    """
    날짜 범위를 chunk_days 단위로 분할

    Args:
        start_date: 시작일 (YYYY-MM-DD)
        end_date: 종료일 (YYYY-MM-DD)
        chunk_days: 분할 단위 (기본 31일)

    Returns:
        [(start1, end1), (start2, end2), ...] 형식의 튜플 리스트 (YYYYMMDD 형식)
    """
    # 문자열을 datetime 객체로 변환
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')

    date_ranges = []
    current_start = start_dt

    while current_start <= end_dt:
        # chunk_days만큼 증가
        current_end = current_start + timedelta(days=chunk_days - 1)

        # 마지막 청크가 end_date를 초과하지 않도록 처리
        if current_end > end_dt:
            current_end = end_dt

        # YYYYMMDD 형식으로 변환하여 추가
        date_ranges.append((
            current_start.strftime('%Y%m%d'),
            current_end.strftime('%Y%m%d')
        ))

        # 다음 기간의 시작일 설정 (현재 종료일 + 1일)
        current_start = current_end + timedelta(days=1)

    return date_ranges
