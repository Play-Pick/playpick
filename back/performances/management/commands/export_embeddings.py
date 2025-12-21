"""
임베딩 벡터를 NumPy 파일로 추출/로드하는 Management Command

사용법:
  # 추출
  python manage.py export_embeddings --export

  # 로드
  python manage.py export_embeddings --import embeddings/performance_embeddings.npz
"""
import os
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from performances.models import Performance, PerformanceEmbedding


class Command(BaseCommand):
    help = '임베딩 벡터를 NumPy 파일로 추출하거나 로드'

    def add_arguments(self, parser):
        parser.add_argument(
            '--export',
            action='store_true',
            help='임베딩을 NumPy 파일로 추출'
        )
        parser.add_argument(
            '--import',
            type=str,
            help='NumPy 파일에서 임베딩 로드'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='embeddings',
            help='출력 디렉토리 (기본: embeddings)'
        )

    def handle(self, *args, **options):
        if options['export']:
            self.export_embeddings(options['output_dir'])
        elif options['import']:
            self.import_embeddings(options['import'])
        else:
            raise CommandError('--export 또는 --import 옵션을 지정해주세요.')

    def export_embeddings(self, output_dir):
        """임베딩을 NumPy 파일로 추출"""
        self.stdout.write(self.style.SUCCESS('\n임베딩 추출 시작...\n'))

        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)

        # PerformanceEmbedding 테이블에서 조회
        embeddings_qs = PerformanceEmbedding.objects.select_related('performance').order_by('performance__mt20id')

        total_count = embeddings_qs.count()

        if total_count == 0:
            self.stdout.write(self.style.WARNING('임베딩이 있는 공연이 없습니다.'))
            return

        self.stdout.write(f'총 {total_count}개 공연의 임베딩을 추출합니다...')

        # 데이터 추출
        mt20ids = []
        embeddings = []
        updated_ats = []

        for emb in embeddings_qs:
            mt20ids.append(emb.performance.mt20id)
            embeddings.append(emb.vector)
            updated_ats.append(
                emb.updated_at.isoformat() if emb.updated_at else None
            )

        # NumPy 배열로 변환
        embeddings_array = np.array(embeddings, dtype=np.float32)

        # 압축 파일로 저장 (.npz)
        output_file = os.path.join(output_dir, 'performance_embeddings.npz')
        np.savez_compressed(
            output_file,
            mt20ids=np.array(mt20ids),
            embeddings=embeddings_array,
            updated_ats=np.array(updated_ats)
        )

        # 파일 크기
        file_size = os.path.getsize(output_file)
        size_mb = file_size / (1024 ** 2)

        self.stdout.write(self.style.SUCCESS(
            f'\n[SUCCESS] 추출 완료!\n'
            f'   - 공연 수: {total_count}개\n'
            f'   - 벡터 차원: {embeddings_array.shape[1]}\n'
            f'   - 파일 크기: {size_mb:.1f} MB\n'
            f'   - 저장 위치: {os.path.abspath(output_file)}\n'
        ))

        # JSON 비교
        json_size_estimate = total_count * 1536 * 8 / (1024 ** 2)  # 대략적인 JSON 크기
        self.stdout.write(
            f'[INFO] JSON 형식 대비 약 {json_size_estimate / size_mb:.1f}배 작습니다.\n'
        )

    def import_embeddings(self, input_file):
        """NumPy 파일에서 임베딩 로드"""
        self.stdout.write(self.style.SUCCESS(f'\n임베딩 로드 시작: {input_file}\n'))

        if not os.path.exists(input_file):
            raise CommandError(f'파일을 찾을 수 없습니다: {input_file}')

        # NumPy 파일 로드
        data = np.load(input_file, allow_pickle=True)
        mt20ids = data['mt20ids']
        embeddings = data['embeddings']
        updated_ats = data.get('updated_ats', None)

        total_count = len(mt20ids)
        self.stdout.write(f'총 {total_count}개 공연의 임베딩을 로드합니다...\n')

        success_count = 0
        not_found_count = 0
        skip_count = 0

        for i, mt20id in enumerate(mt20ids):
            try:
                performance = Performance.objects.get(mt20id=mt20id)

                # 이미 임베딩이 있으면 스킵 (선택사항)
                if hasattr(performance, 'embedding'):
                    skip_count += 1
                    if i % 100 == 0:
                        self.stdout.write(f'  [SKIP] [{i+1}/{total_count}] {mt20id} - 이미 임베딩 존재 (스킵)')
                    continue

                # PerformanceEmbedding 생성 또는 업데이트
                if updated_ats is not None and updated_ats[i]:
                    from datetime import datetime
                    updated_at = datetime.fromisoformat(updated_ats[i])
                else:
                    updated_at = timezone.now()

                PerformanceEmbedding.objects.update_or_create(
                    performance=performance,
                    defaults={
                        'vector': embeddings[i].tolist(),
                        'updated_at': updated_at
                    }
                )
                success_count += 1

                if (i + 1) % 100 == 0:
                    self.stdout.write(f'  [OK] [{i+1}/{total_count}] 처리 중...')

            except Performance.DoesNotExist:
                not_found_count += 1
                self.stdout.write(self.style.WARNING(f'  [WARN] {mt20id} - DB에 없음 (건너뜀)'))

        # 결과 출력
        self.stdout.write(self.style.SUCCESS(
            f'\n{"="*60}\n'
            f'임베딩 로드 완료!\n'
            f'{"="*60}\n'
            f'  [OK] 성공: {success_count}개\n'
            f'  [SKIP] 스킵: {skip_count}개 (이미 존재)\n'
            f'  [WARN] 미발견: {not_found_count}개\n'
            f'{"="*60}\n'
        ))
