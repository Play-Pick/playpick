"""
기존 DB의 performances 앱 데이터를 새 DB로 마이그레이션하는 스크립트
"""
import sqlite3
import os
import sys
from datetime import datetime

# Django 설정
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import (
    Performance,
    BoxOfficeRanking,
    PerformanceDetail,
    PerformanceImage,
    PerformanceMetric
)

def migrate_performances():
    """Performance 데이터 마이그레이션"""
    print("=== Migrating Performance data ===")

    old_db = sqlite3.connect('db.sqlite3.backup')
    old_db.row_factory = sqlite3.Row
    cursor = old_db.cursor()

    cursor.execute("""
        SELECT
            mt20id, prfnm, prfpdfrom, prfpdto, fcltynm,
            poster, area, genrenm, prfstate, openrun, rnum
        FROM performances_performance
    """)

    performances = cursor.fetchall()
    old_db.close()

    batch_size = 500
    created_count = 0

    for i in range(0, len(performances), batch_size):
        batch = performances[i:i + batch_size]
        objs = []

        for row in batch:
            objs.append(Performance(
                mt20id=row['mt20id'],
                prfnm=row['prfnm'],
                prfpdfrom=row['prfpdfrom'],
                prfpdto=row['prfpdto'],
                fcltynm=row['fcltynm'],
                poster=row['poster'],
                area=row['area'],
                genrenm=row['genrenm'],
                prfstate=row['prfstate'],
                openrun=row['openrun'],
                rnum=row['rnum'],
                cast_search_text=''  # 새 필드는 빈 값으로
            ))

        Performance.objects.bulk_create(objs, ignore_conflicts=True)
        created_count += len(objs)
        print(f"  Progress: {created_count}/{len(performances)}")

    print(f"Migrated {created_count} performances")


def migrate_boxoffice():
    """BoxOfficeRanking 데이터 마이그레이션"""
    print("\n=== Migrating BoxOfficeRanking data ===")

    old_db = sqlite3.connect('db.sqlite3.backup')
    old_db.row_factory = sqlite3.Row
    cursor = old_db.cursor()

    cursor.execute("""
        SELECT
            id, performance_id, rank, genre_code, ranking_date,
            period_type, area, seat_count, performance_count,
            collected_at, updated_at
        FROM performances_boxofficeranking
    """)

    rankings = cursor.fetchall()
    objs = []

    for row in rankings:
        try:
            performance = Performance.objects.get(mt20id=row['performance_id'])
            objs.append(BoxOfficeRanking(
                performance=performance,
                rank=row['rank'],
                genre_code=row['genre_code'],
                ranking_date=row['ranking_date'],
                period_type=row['period_type'],
                area=row['area'],
                seat_count=row['seat_count'],
                performance_count=row['performance_count'],
                collected_at=row['collected_at'],
                updated_at=row['updated_at']
            ))
        except Performance.DoesNotExist:
            continue

    BoxOfficeRanking.objects.bulk_create(objs, ignore_conflicts=True)
    old_db.close()
    print(f"Migrated {len(objs)} box office rankings")


def migrate_performance_details():
    """PerformanceDetail 데이터 마이그레이션"""
    print("\n=== Migrating PerformanceDetail data ===")

    old_db = sqlite3.connect('db.sqlite3.backup')
    old_db.row_factory = sqlite3.Row
    cursor = old_db.cursor()

    cursor.execute("""
        SELECT
            performance_id, prfcast, prfcrew, prfruntime, prfage,
            entrpsnm, pcseguidance, sty, dtguidance, relates,
            collected_at, updated_at
        FROM performances_performancedetail
    """)

    details = cursor.fetchall()
    batch_size = 1000
    created_count = 0

    for i in range(0, len(details), batch_size):
        batch = details[i:i + batch_size]
        objs = []

        for row in batch:
            try:
                performance = Performance.objects.get(mt20id=row['performance_id'])

                # relates는 JSON 필드
                relates_data = row['relates']
                if relates_data:
                    try:
                        import json
                        relates_data = json.loads(relates_data)
                    except:
                        relates_data = []
                else:
                    relates_data = []

                objs.append(PerformanceDetail(
                    performance=performance,
                    prfcast=row['prfcast'] or '',
                    prfcrew=row['prfcrew'] or '',
                    prfruntime=row['prfruntime'] or '',
                    prfage=row['prfage'] or '',
                    entrpsnm=row['entrpsnm'] or '',
                    pcseguidance=row['pcseguidance'] or '',
                    sty=row['sty'] or '',
                    dtguidance=row['dtguidance'] or '',
                    relates=relates_data,
                    collected_at=row['collected_at'],
                    updated_at=row['updated_at']
                ))
            except Performance.DoesNotExist:
                continue

        PerformanceDetail.objects.bulk_create(objs, ignore_conflicts=True)
        created_count += len(objs)
        print(f"  Progress: {created_count}/{len(details)}")

    old_db.close()
    print(f"Migrated {created_count} performance details")


def migrate_performance_images():
    """PerformanceImage 데이터 마이그레이션"""
    print("\n=== Migrating PerformanceImage data ===")

    old_db = sqlite3.connect('db.sqlite3.backup')
    old_db.row_factory = sqlite3.Row
    cursor = old_db.cursor()

    cursor.execute("""
        SELECT
            id, performance_id, image_url, "order", collected_at
        FROM performances_performanceimage
    """)

    images = cursor.fetchall()
    batch_size = 5000
    created_count = 0

    for i in range(0, len(images), batch_size):
        batch = images[i:i + batch_size]
        objs = []

        for row in batch:
            try:
                performance = Performance.objects.get(mt20id=row['performance_id'])
                objs.append(PerformanceImage(
                    performance=performance,
                    image_url=row['image_url'],
                    order=row['order'],
                    collected_at=row['collected_at']
                ))
            except Performance.DoesNotExist:
                continue

        PerformanceImage.objects.bulk_create(objs, ignore_conflicts=True)
        created_count += len(objs)
        print(f"  Progress: {created_count}/{len(images)}")

    old_db.close()
    print(f"Migrated {created_count} performance images")


def update_cast_search_text():
    """cast_search_text 필드 업데이트 (새 필드)"""
    print("\n=== Updating cast_search_text field ===")

    performances = Performance.objects.filter(detail__isnull=False)[:1000]

    for perf in performances:
        if hasattr(perf, 'detail'):
            cast_text = perf.detail.prfcast or ''
            # 공백과 쉼표로 구분된 배우 이름을 공백으로 연결
            perf.cast_search_text = cast_text.replace(',', ' ').replace('\n', ' ')
            perf.save(update_fields=['cast_search_text'])

    print(f"Updated cast_search_text for {performances.count()} performances")


if __name__ == '__main__':
    print("Starting data migration...")
    print(f"Time: {datetime.now()}\n")

    try:
        migrate_performances()
        migrate_boxoffice()
        migrate_performance_details()
        migrate_performance_images()
        update_cast_search_text()

        print("\n" + "="*50)
        print("Data migration completed successfully!")
        print("="*50)

        # 결과 확인
        print("\nFinal counts:")
        print(f"  Performances: {Performance.objects.count()}")
        print(f"  BoxOfficeRankings: {BoxOfficeRanking.objects.count()}")
        print(f"  PerformanceDetails: {PerformanceDetail.objects.count()}")
        print(f"  PerformanceImages: {PerformanceImage.objects.count()}")
        print(f"  PerformanceMetrics: {PerformanceMetric.objects.count()}")

    except Exception as e:
        print(f"\nError during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
