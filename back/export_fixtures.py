"""
전체 DB 데이터를 fixture로 추출하는 스크립트
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from django.core import serializers
from performances.models import Performance, BoxOfficeRanking, PerformanceDetail, PerformanceImage, PerformanceEmbedding
from accounts.models import User
from community.models import Article, Comment

def format_file_size(size_bytes):
    """파일 크기를 사람이 읽기 쉬운 형식으로 변환"""
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 ** 2:
        return f'{size_bytes / 1024:.1f} KB'
    elif size_bytes < 1024 ** 3:
        return f'{size_bytes / (1024 ** 2):.1f} MB'
    else:
        return f'{size_bytes / (1024 ** 3):.1f} GB'


def export_model_to_json(model_class, model_name, fixtures_dir):
    """모델 데이터를 개별 JSON 파일로 추출"""
    objects = list(model_class.objects.all())
    count = len(objects)

    if count == 0:
        print(f"  [SKIP] {model_name}: 데이터 없음")
        return 0

    data = json.loads(serializers.serialize('json', objects, indent=2))

    # 파일명: performances_performance.json 형식
    app_label = model_class._meta.app_label
    filename = f'{app_label}_{model_name.lower()}.json'
    filepath = os.path.join(fixtures_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(filepath)
    size_str = format_file_size(file_size)

    print(f"  [OK] {model_name}: {count}건 -> {filename} ({size_str})")
    return count


def export_fixtures():
    """모든 데이터를 모델별 fixture JSON 파일로 추출"""

    print("Fixture 추출 시작 (모델별 분리)...")

    # fixtures 디렉토리 생성
    fixtures_dir = 'fixtures'
    os.makedirs(fixtures_dir, exist_ok=True)

    total_count = 0

    # 1. Performances 앱 데이터 추출
    print("\n[1/4] Performances 앱 데이터 추출 중...")
    perf_count = export_model_to_json(Performance, 'Performance', fixtures_dir)
    box_count = export_model_to_json(BoxOfficeRanking, 'BoxOfficeRanking', fixtures_dir)
    detail_count = export_model_to_json(PerformanceDetail, 'PerformanceDetail', fixtures_dir)
    image_count = export_model_to_json(PerformanceImage, 'PerformanceImage', fixtures_dir)
    total_count += perf_count + box_count + detail_count + image_count

    # 2. Accounts 앱 데이터 추출
    print("\n[2/4] Accounts 앱 데이터 추출 중...")
    user_count = export_model_to_json(User, 'User', fixtures_dir)
    total_count += user_count

    # 3. Community 앱 데이터 추출
    print("\n[3/4] Community 앱 데이터 추출 중...")
    article_count = export_model_to_json(Article, 'Article', fixtures_dir)
    comment_count = export_model_to_json(Comment, 'Comment', fixtures_dir)
    total_count += article_count + comment_count

    # 4. 임베딩 데이터는 별도로 안내
    print("\n[4/4] PerformanceEmbedding 데이터 (건너뜀)")
    embeddings_count = PerformanceEmbedding.objects.count()
    print(f"  [INFO] PerformanceEmbedding: {embeddings_count}건 존재")
    print(f"  [INFO] 임베딩 데이터는 다음 명령어로 별도 추출하세요:")
    print(f"         python manage.py export_embeddings --export")

    # 전체 요약
    print("\n" + "="*60)
    print("Fixture 추출 완료!")
    print("="*60)
    print(f"총 데이터: {total_count}건")
    print(f"  - Performance: {perf_count}건")
    print(f"  - BoxOfficeRanking: {box_count}건")
    print(f"  - PerformanceDetail: {detail_count}건")
    print(f"  - PerformanceImage: {image_count}건")
    print(f"  - User: {user_count}건")
    print(f"  - Article: {article_count}건")
    print(f"  - Comment: {comment_count}건")
    print(f"  - Embeddings: {embeddings_count}건 (별도 추출 필요)")
    print(f"\n저장 위치: {os.path.abspath(fixtures_dir)}")
    print("\n로드 방법 (순서 중요):")
    print("  # 1. Performances 앱")
    print("  python manage.py loaddata fixtures/performances_performance.json")
    print("  python manage.py loaddata fixtures/performances_boxofficeranking.json")
    print("  python manage.py loaddata fixtures/performances_performancedetail.json")
    print("  python manage.py loaddata fixtures/performances_performanceimage.json")
    print("\n  # 2. Accounts 앱")
    print("  python manage.py loaddata fixtures/accounts_user.json")
    print("\n  # 3. Community 앱")
    print("  python manage.py loaddata fixtures/community_article.json")
    print("  python manage.py loaddata fixtures/community_comment.json")
    print("\n임베딩 로드 방법:")
    print("  python manage.py export_embeddings --import embeddings/performance_embeddings.npz")

if __name__ == '__main__':
    export_fixtures()
