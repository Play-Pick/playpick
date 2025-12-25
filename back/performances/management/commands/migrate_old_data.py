"""
Django Management Command: 기존 DB의 performances 데이터를 새 DB로 마이그레이션
"""
from django.core.management.base import BaseCommand
from django.db import transaction
import sqlite3
from datetime import datetime

from performances.models import (
    Performance,
    BoxOfficeRanking,
    PerformanceDetail,
    PerformanceImage,
)


class Command(BaseCommand):
    help = 'Migrate performance data from old database to new database'

    def handle(self, *args, **options):
        self.stdout.write("Starting data migration...")
        self.stdout.write(f"Time: {datetime.now()}\n")

        try:
            self.migrate_performances()
            self.migrate_boxoffice()
            self.migrate_performance_details()
            self.migrate_performance_images()

            self.stdout.write("\n" + "="*50)
            self.stdout.write(self.style.SUCCESS("Data migration completed successfully!"))
            self.stdout.write("="*50)

            # 결과 확인
            self.stdout.write("\nFinal counts:")
            self.stdout.write(f"  Performances: {Performance.objects.count()}")
            self.stdout.write(f"  BoxOfficeRankings: {BoxOfficeRanking.objects.count()}")
            self.stdout.write(f"  PerformanceDetails: {PerformanceDetail.objects.count()}")
            self.stdout.write(f"  PerformanceImages: {PerformanceImage.objects.count()}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\nError during migration: {e}"))
            import traceback
            traceback.print_exc()
            raise

    def migrate_performances(self):
        """Performance 데이터 마이그레이션"""
        self.stdout.write("=== Migrating Performance data ===")

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

        with transaction.atomic():
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
                        cast_search_text=''
                    ))

                Performance.objects.bulk_create(objs, ignore_conflicts=True)
                created_count += len(objs)
                self.stdout.write(f"  Progress: {created_count}/{len(performances)}")

        self.stdout.write(self.style.SUCCESS(f"Migrated {created_count} performances"))

    def migrate_boxoffice(self):
        """BoxOfficeRanking 데이터 마이그레이션"""
        self.stdout.write("\n=== Migrating BoxOfficeRanking data ===")

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
        old_db.close()

        objs = []
        skipped = 0

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
                skipped += 1
                continue

        with transaction.atomic():
            BoxOfficeRanking.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Migrated {len(objs)} box office rankings (skipped {skipped})"))

    def migrate_performance_details(self):
        """PerformanceDetail 데이터 마이그레이션"""
        self.stdout.write("\n=== Migrating PerformanceDetail data ===")

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
        old_db.close()

        batch_size = 1000
        created_count = 0
        skipped = 0

        with transaction.atomic():
            for i in range(0, len(details), batch_size):
                batch = details[i:i + batch_size]
                objs = []

                for row in batch:
                    try:
                        performance = Performance.objects.get(mt20id=row['performance_id'])

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
                        skipped += 1
                        continue

                PerformanceDetail.objects.bulk_create(objs, ignore_conflicts=True)
                created_count += len(objs)
                self.stdout.write(f"  Progress: {created_count}/{len(details)}")

        self.stdout.write(self.style.SUCCESS(f"Migrated {created_count} performance details (skipped {skipped})"))

    def migrate_performance_images(self):
        """PerformanceImage 데이터 마이그레이션"""
        self.stdout.write("\n=== Migrating PerformanceImage data ===")

        old_db = sqlite3.connect('db.sqlite3.backup')
        old_db.row_factory = sqlite3.Row
        cursor = old_db.cursor()

        cursor.execute("""
            SELECT
                id, performance_id, image_url, "order", collected_at
            FROM performances_performanceimage
        """)

        images = cursor.fetchall()
        old_db.close()

        batch_size = 5000
        created_count = 0
        skipped = 0

        with transaction.atomic():
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
                        skipped += 1
                        continue

                PerformanceImage.objects.bulk_create(objs, ignore_conflicts=True)
                created_count += len(objs)
                self.stdout.write(f"  Progress: {created_count}/{len(images)}")

        self.stdout.write(self.style.SUCCESS(f"Migrated {created_count} performance images (skipped {skipped})"))
