"""
Django 테이블별 fixture 추출 Management Command

사용법:
  python manage.py export_fixture performances Performance
  python manage.py export_fixture performances BoxOfficeRanking
  python manage.py export_fixture performances --all
  python manage.py export_fixture accounts User
"""
import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.apps import apps


class Command(BaseCommand):
    help = '특정 테이블의 데이터를 fixture JSON 파일로 추출'

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            type=str,
            help='Django 앱 이름 (예: performances, accounts, community)'
        )
        parser.add_argument(
            'model_name',
            type=str,
            nargs='?',
            default=None,
            help='모델 이름 (예: Performance, User) 또는 --all'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='fixtures',
            help='출력 디렉토리 (기본: fixtures)'
        )
        parser.add_argument(
            '--include-embedding',
            action='store_true',
            help='PerformanceEmbedding 모델도 포함 (기본: 제외)'
        )

    def handle(self, *args, **options):
        app_name = options['app_name']
        model_name = options['model_name']
        output_dir = options['output_dir']
        include_embedding = options['include_embedding']

        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)

        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f'앱 "{app_name}"을(를) 찾을 수 없습니다.')

        # --all 옵션: 앱의 모든 모델 추출
        if model_name == '--all' or model_name is None:
            self.export_all_models(app_config, output_dir, include_embedding)
        else:
            # 특정 모델만 추출
            self.export_single_model(app_config, model_name, output_dir, include_embedding)

    def export_all_models(self, app_config, output_dir, include_embedding):
        """앱의 모든 모델 추출"""
        self.stdout.write(self.style.SUCCESS(f'\n[{app_config.label}] 앱의 모든 모델 추출 시작...\n'))

        models = app_config.get_models()
        total_count = 0

        for model in models:
            # PerformanceEmbedding은 include_embedding 옵션이 있을 때만 추출
            if model.__name__ == 'PerformanceEmbedding' and not include_embedding:
                self.stdout.write(f'  [SKIP] PerformanceEmbedding: --include-embedding 옵션으로 활성화 가능')
                continue

            count = self.export_model_data(model, output_dir)
            total_count += count

        self.stdout.write(self.style.SUCCESS(f'\n총 {total_count}건의 데이터를 추출했습니다.'))
        self.stdout.write(f'저장 위치: {os.path.abspath(output_dir)}\n')

    def export_single_model(self, app_config, model_name, output_dir, include_embedding):
        """특정 모델만 추출"""
        try:
            model = app_config.get_model(model_name)
        except LookupError:
            raise CommandError(f'모델 "{model_name}"을(를) "{app_config.label}" 앱에서 찾을 수 없습니다.')

        self.stdout.write(self.style.SUCCESS(f'\n[{model.__name__}] 모델 추출 시작...\n'))
        count = self.export_model_data(model, output_dir)
        self.stdout.write(self.style.SUCCESS(f'\n총 {count}건의 데이터를 추출했습니다.'))
        self.stdout.write(f'저장 위치: {os.path.abspath(output_dir)}\n')

    def export_model_data(self, model, output_dir):
        """모델 데이터를 JSON 파일로 저장"""
        model_name = model.__name__
        app_label = model._meta.app_label

        # 데이터 조회
        queryset = model.objects.all()
        count = queryset.count()

        if count == 0:
            self.stdout.write(self.style.WARNING(f'  [WARN] {model_name}: 데이터 없음 (건너뜀)'))
            return 0

        # 직렬화
        serialized_data = serializers.serialize('json', queryset, indent=2)
        data = json.loads(serialized_data)

        # 파일명 생성: app_model.json
        filename = f'{app_label}_{model_name.lower()}.json'
        filepath = os.path.join(output_dir, filename)

        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 파일 크기 계산
        file_size = os.path.getsize(filepath)
        size_str = self.format_file_size(file_size)

        self.stdout.write(
            f'  [OK] {model_name}: {count}건 -> {filename} ({size_str})'
        )

        return count

    def format_file_size(self, size_bytes):
        """파일 크기를 사람이 읽기 쉬운 형식으로 변환"""
        if size_bytes < 1024:
            return f'{size_bytes} B'
        elif size_bytes < 1024 ** 2:
            return f'{size_bytes / 1024:.1f} KB'
        elif size_bytes < 1024 ** 3:
            return f'{size_bytes / (1024 ** 2):.1f} MB'
        else:
            return f'{size_bytes / (1024 ** 3):.1f} GB'
