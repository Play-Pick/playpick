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
from performances.models import Performance, BoxOfficeRanking, PerformanceDetail, PerformanceImage
from accounts.models import User
from community.models import Article, Comment

def export_fixtures():
    """모든 데이터를 fixture JSON 파일로 추출"""

    print("Fixture 추출 시작...")

    # fixtures 디렉토리 생성
    fixtures_dir = 'fixtures'
    os.makedirs(fixtures_dir, exist_ok=True)

    # 1. Performances 앱 데이터 추출
    print("\n[1/3] Performances 데이터 추출 중...")
    performances = list(Performance.objects.all())
    boxoffice = list(BoxOfficeRanking.objects.all())
    details = list(PerformanceDetail.objects.all())
    images = list(PerformanceImage.objects.all())

    performances_data = json.loads(serializers.serialize('json', performances + boxoffice + details + images, indent=2))

    with open(f'{fixtures_dir}/performances.json', 'w', encoding='utf-8') as f:
        json.dump(performances_data, f, ensure_ascii=False, indent=2)

    print(f"  - Performance: {len(performances)}건")
    print(f"  - BoxOfficeRanking: {len(boxoffice)}건")
    print(f"  - PerformanceDetail: {len(details)}건")
    print(f"  - PerformanceImage: {len(images)}건")
    print(f"  -> fixtures/performances.json 저장 완료")

    # 2. Accounts 앱 데이터 추출
    print("\n[2/3] Accounts 데이터 추출 중...")
    users = list(User.objects.all())

    accounts_data = json.loads(serializers.serialize('json', users, indent=2))

    with open(f'{fixtures_dir}/accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts_data, f, ensure_ascii=False, indent=2)

    print(f"  - User: {len(users)}건")
    print(f"  -> fixtures/accounts.json 저장 완료")

    # 3. Community 앱 데이터 추출
    print("\n[3/3] Community 데이터 추출 중...")
    articles = list(Article.objects.all())
    comments = list(Comment.objects.all())

    community_data = json.loads(serializers.serialize('json', articles + comments, indent=2))

    with open(f'{fixtures_dir}/community.json', 'w', encoding='utf-8') as f:
        json.dump(community_data, f, ensure_ascii=False, indent=2)

    print(f"  - Article: {len(articles)}건")
    print(f"  - Comment: {len(comments)}건")
    print(f"  -> fixtures/community.json 저장 완료")

    # 전체 요약
    print("\n" + "="*60)
    print("Fixture 추출 완료!")
    print("="*60)
    print(f"총 데이터:")
    print(f"  - Performances: {len(performances + boxoffice + details + images)}건")
    print(f"  - Accounts: {len(users)}건")
    print(f"  - Community: {len(articles + comments)}건")
    print(f"\n저장 위치: {os.path.abspath(fixtures_dir)}")
    print("\n로드 방법:")
    print("  python manage.py loaddata fixtures/performances.json")
    print("  python manage.py loaddata fixtures/accounts.json")
    print("  python manage.py loaddata fixtures/community.json")

if __name__ == '__main__':
    export_fixtures()
