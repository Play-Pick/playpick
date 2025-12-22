"""
관리자 전용 API - KOPIS 데이터 수집 관리
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.core.management import call_command
from datetime import datetime, timedelta
from ..models import Performance, BoxOfficeRanking, GENRE_DISPLAY_ORDER, GENRE_CODE_MAPPING
from datetime import date
import io


class CollectBoxOfficeAPIView(APIView):
    """박스오피스 데이터 수집"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            out = io.StringIO()
            target_date = request.data.get('date')  # YYYYMMDD
            period_type = request.data.get('period_type', 'week')

            # 수집 전 박스오피스 데이터 수 확인
            before_count = BoxOfficeRanking.objects.count()

            if target_date:
                call_command('collect_boxoffice', date=target_date, period=period_type, stdout=out)
            else:
                call_command('collect_boxoffice', stdout=out)

            # 수집 후 박스오피스 데이터 수 확인
            after_count = BoxOfficeRanking.objects.count()
            collected = after_count - before_count

            output = out.getvalue()

            return Response({
                'success': True,
                'message': f'박스오피스 데이터 수집 완료 ({collected}건 수집)',
                'output': output,
                'data': {
                    'collected': collected,
                    'total': after_count
                }
            })

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            return Response({
                'success': False,
                'message': f'오류 발생: {str(e)}',
                'output': out.getvalue() if 'out' in locals() else '',
                'error_detail': error_detail
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectPerformancesAPIView(APIView):
    """공연 정보 수집"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            out = io.StringIO()

            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            # 기본값: 최근 1개월
            if not start_date or not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            call_command(
                'collect_performances',
                start_date=start_date,
                end_date=end_date,
                stdout=out
            )

            output = out.getvalue()

            return Response({
                'success': True,
                'message': f'공연 정보 수집 완료 ({start_date} ~ {end_date})',
                'output': output
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'오류 발생: {str(e)}',
                'output': out.getvalue() if 'out' in locals() else ''
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectPerformanceDetailAPIView(APIView):
    """공연 상세 정보 수집"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            out = io.StringIO()

            limit = request.data.get('limit', 100)

            # 수집 전 상세정보 없는 공연 수 확인
            before_count = Performance.objects.filter(detail__isnull=True).count()

            call_command(
                'collect_performance_detail',
                missing_only=True,
                limit=limit,
                stdout=out
            )

            # 수집 후 상세정보 없는 공연 수 확인
            after_count = Performance.objects.filter(detail__isnull=True).count()
            collected = before_count - after_count

            output = out.getvalue()

            return Response({
                'success': True,
                'message': f'공연 상세 정보 수집 완료 (최대 {limit}건)',
                'output': output,
                'data': {
                    'collected': collected,
                    'remaining': after_count
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'오류 발생: {str(e)}',
                'output': out.getvalue() if 'out' in locals() else ''
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateTestBoxOfficeAPIView(APIView):
    """테스트 박스오피스 데이터 생성"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            today = date.today()
            total_created = 0

            # 기존 오늘 날짜 데이터 삭제
            deleted_count = BoxOfficeRanking.objects.filter(ranking_date=today).delete()[0]

            results = []

            for genre_code in GENRE_DISPLAY_ORDER:
                genre_name = GENRE_CODE_MAPPING[genre_code]

                # 해당 장르의 공연 조회
                genre_filter_map = {
                    'BBBC': '뮤지컬',
                    'AAAA': '연극',
                    'CCCA': '클래식',
                    'GGGA': '대중콘서트',
                    'CCCD': '무용',
                    'EEEB': '국악',
                    'EEEA': '복합',
                }

                genre_kr = genre_filter_map.get(genre_code, genre_name)

                performances = Performance.objects.filter(
                    genrenm__icontains=genre_kr,
                    prfstate='공연중'
                )[:20]

                if performances.count() == 0:
                    performances = Performance.objects.filter(
                        genrenm__icontains=genre_kr
                    )[:20]

                if performances.count() == 0:
                    performances = Performance.objects.all()[:20]

                created_count = 0
                for idx, perf in enumerate(performances, 1):
                    BoxOfficeRanking.objects.create(
                        performance=perf,
                        rank=idx,
                        genre_code=genre_code,
                        ranking_date=today,
                        period_type='week',
                        area=perf.area or '서울',
                        seat_count=1000 - (idx * 30),
                        performance_count=50 - idx,
                    )
                    created_count += 1
                    total_created += 1

                results.append({
                    'genre': genre_name,
                    'count': created_count
                })

            return Response({
                'success': True,
                'message': f'테스트 박스오피스 데이터 생성 완료',
                'data': {
                    'date': str(today),
                    'total_created': total_created,
                    'deleted': deleted_count,
                    'results': results
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'오류 발생: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataStatsAPIView(APIView):
    """데이터 통계 조회"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            stats = {
                'performances': {
                    'total': Performance.objects.count(),
                    'with_detail': Performance.objects.filter(detail__isnull=False).count(),
                    'without_detail': Performance.objects.filter(detail__isnull=True).count(),
                    'ongoing': Performance.objects.filter(prfstate='공연중').count(),
                },
                'boxoffice': {
                    'total': BoxOfficeRanking.objects.count(),
                    'latest_date': BoxOfficeRanking.objects.order_by('-ranking_date').values_list('ranking_date', flat=True).first(),
                    'by_genre': []
                }
            }

            # 장르별 박스오피스 통계
            for genre_code in GENRE_DISPLAY_ORDER:
                genre_name = GENRE_CODE_MAPPING[genre_code]
                count = BoxOfficeRanking.objects.filter(genre_code=genre_code).count()
                stats['boxoffice']['by_genre'].append({
                    'code': genre_code,
                    'name': genre_name,
                    'count': count
                })

            return Response({
                'success': True,
                'data': stats
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'오류 발생: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
