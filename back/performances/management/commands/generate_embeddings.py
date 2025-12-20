"""
공연 데이터의 임베딩 벡터를 생성하여 DB에 저장하는 Management Command
python manage.py generate_embeddings
"""

import os
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from performances.models import Performance
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_embedding_text_standard(performance):
    """
    test_strategy_2_standard.py의 로직을 그대로 사용
    기본 정보 + 상세 정보 + 줄거리 200자
    """
    parts = []

    # 기본 정보
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

    # 상세 정보
    try:
        if hasattr(performance, 'detail') and performance.detail:
            detail = performance.detail
            if detail.prfage:
                parts.append(f"관람연령 {detail.prfage}")
            if detail.prfruntime:
                parts.append(f"러닝타임 {detail.prfruntime}")
            if detail.entrpsnm:
                parts.append(f"제작 {detail.entrpsnm}")
            if detail.sty:
                summary = detail.sty[:200].strip()
                if summary:
                    parts.append(summary)
    except Exception:
        pass

    text = " ".join(parts)

    # 빈 텍스트 방지
    if not text.strip():
        text = f"{performance.prfnm} {performance.genrenm}"

    return text


class Command(BaseCommand):
    help = "공연 데이터의 임베딩 벡터를 생성하여 DB에 저장"

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='배치 크기 (기본: 100)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='이미 임베딩이 있는 데이터도 재생성'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        force = options['force']

        # OpenAI 클라이언트 초기화
        client = OpenAI(
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
            api_key=os.getenv("GMS_KEY"),
        )

        # 임베딩이 없는 공연들만 선택 (force 옵션이면 전체)
        if force:
            queryset = Performance.objects.all()
        else:
            queryset = Performance.objects.filter(embedding_vector__isnull=True)

        queryset = queryset.select_related('detail')
        total_count = queryset.count()

        self.stdout.write(f"총 {total_count}개 공연의 임베딩을 생성합니다...")

        success_count = 0
        error_count = 0

        # 배치 처리
        for i in range(0, total_count, batch_size):
            batch = list(queryset[i:i + batch_size])

            self.stdout.write(f"\n[{i+1}~{min(i+batch_size, total_count)}/{total_count}] 처리 중...")

            for performance in batch:
                try:
                    # 임베딩 텍스트 생성
                    text = generate_embedding_text_standard(performance)

                    # OpenAI API 호출
                    response = client.embeddings.create(
                        model="text-embedding-3-small",
                        input=text
                    )

                    # 벡터 추출 및 저장
                    embedding = response.data[0].embedding
                    performance.embedding_vector = embedding
                    performance.embedding_updated_at = timezone.now()
                    performance.save(update_fields=['embedding_vector', 'embedding_updated_at'])

                    success_count += 1
                    self.stdout.write(f"  ✅ {performance.mt20id} - {performance.prfnm}")

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"  ❌ {performance.mt20id} - {performance.prfnm}: {e}")
                    )

                # API Rate Limit 방지 (0.05초 대기)
                time.sleep(0.05)

        # 결과 출력
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS(f"✅ 성공: {success_count}개"))
        self.stdout.write(self.style.ERROR(f"❌ 실패: {error_count}개"))
        self.stdout.write("=" * 80)
