from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Performance, BoxOfficeRanking, PerformanceDetail
from .serializers import (
    PerformanceListSerializer,
    PerformanceDetailViewSerializer,
    BoxOfficeRankingSerializer
)
from .ai_search import AISearchEngine


class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """공연 정보 ViewSet (읽기 전용)"""
    queryset = Performance.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genrenm', 'prfstate', 'area']
    search_fields = ['prfnm', 'fcltynm']
    ordering_fields = ['prfpdfrom', 'prfpdto']
    ordering = ['-prfpdfrom']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerformanceDetailViewSerializer
        return PerformanceListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 장르 필터링
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genrenm=genre)

        # 검색어 필터링
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(prfnm__icontains=search) |
                Q(fcltynm__icontains=search)
            )

        if self.action == 'retrieve':
            queryset = queryset.select_related('detail').prefetch_related('intro_images')

        return queryset

    # 👇 [여기] 이 부분을 추가하세요 👇
    @action(detail=False, methods=['get'], url_path='boxoffice-genre')
    def boxoffice_genre(self, request):
        """
        URL: GET /api/performances/boxoffice-genre/?genre=BBBC
        설명: 특정 장르의 박스오피스 랭킹을 조회
        """
        # 1. 쿼리 파라미터 받기 (?genre=BBBC)
        genre_code = request.query_params.get('genre', 'BBBC')

        # genre_code를 genrenm으로 매핑 (KOPIS API가 잘못된 데이터를 반환하므로 genrenm으로 필터링)
        GENRE_TO_GENRENM = {
            'AAAA': '연극',
            'BBBC': '뮤지컬',
            'CCCA': '서양음악(클래식)',
            'CCCD': '무용(서양/한국무용)',
            'GGGA': '대중음악',
        }

        target_genrenm = GENRE_TO_GENRENM.get(genre_code)
        if not target_genrenm:
            return Response({
                'success': False,
                'data': []
            })

        # 2. 박스오피스 랭킹 데이터 조회 (genrenm으로 필터링, 최신순, 랭킹순)
        rankings = BoxOfficeRanking.objects.filter(
            performance__genrenm=target_genrenm
        ).select_related('performance').order_by('-ranking_date', 'rank')[:10]

        # 3. 시리얼라이징하고 플랫한 구조로 변환 (context에 request 전달하여 is_liked 계산)
        serializer = BoxOfficeRankingSerializer(rankings, many=True, context={'request': request})

        # 4. 프론트엔드가 기대하는 형식으로 데이터 변환 (performance 필드를 최상위로 병합)
        flattened_data = []
        for item in serializer.data:
            performance_data = item.get('performance', {})
            flattened_item = {
                **performance_data,  # 공연 정보를 최상위로
                'rank': item.get('rank'),  # 랭킹 정보 추가
                'ranking_date': item.get('ranking_date'),
            }
            flattened_data.append(flattened_item)

        # 5. 프론트엔드가 기대하는 형식으로 반환
        return Response({
            'success': True,
            'data': flattened_data
        })
    
    # 👆 [여기까지] 추가 👆

    @action(detail=False, methods=['get'], url_path='boxoffice-all')
    def boxoffice_all(self, request):
        """
        URL: GET /api/performances/boxoffice-all/
        설명: 좌석수 기준 전체 박스오피스 랭킹 조회 (Top 10)
        """
        # 최신 ranking_date의 데이터를 좌석수 기준으로 정렬
        from django.db.models import Max

        # 최신 날짜 찾기
        latest_date = BoxOfficeRanking.objects.aggregate(Max('ranking_date'))['ranking_date__max']

        if not latest_date:
            return Response({
                'success': False,
                'data': []
            })

        # 최신 날짜의 데이터를 좌석수 기준으로 정렬하여 Top 10
        rankings = BoxOfficeRanking.objects.filter(
            ranking_date=latest_date
        ).select_related('performance').order_by('-seat_count')[:10]

        # 시리얼라이징 (context에 request 전달하여 is_liked 계산)
        serializer = BoxOfficeRankingSerializer(rankings, many=True, context={'request': request})

        # 플랫한 구조로 변환
        flattened_data = []
        for idx, item in enumerate(serializer.data, 1):
            performance_data = item.get('performance', {})
            flattened_item = {
                **performance_data,
                'rank': idx,  # 좌석수 기준 순위 재부여
                'original_rank': item.get('rank'),  # 원래 장르별 순위
                'ranking_date': item.get('ranking_date'),
                'seat_count': item.get('seat_count'),
                'performance_count': item.get('performance_count'),
            }
            flattened_data.append(flattened_item)

        return Response({
            'success': True,
            'data': flattened_data
        })

    @action(detail=False, methods=['get'], url_path='boxoffice-highlight')
    def boxoffice_highlight(self, request):
        """
        URL: GET /api/performances/boxoffice-highlight/
        설명: 하이라이트 캐러셀용 박스오피스 Top 6~8
        """
        from django.db.models import Max

        # 최신 날짜 찾기
        latest_date = BoxOfficeRanking.objects.aggregate(Max('ranking_date'))['ranking_date__max']

        if not latest_date:
            return Response({
                'success': False,
                'data': []
            })

        # 최신 날짜의 데이터를 좌석수 기준으로 정렬하여 Top 8
        rankings = BoxOfficeRanking.objects.filter(
            ranking_date=latest_date
        ).select_related('performance').order_by('-seat_count')[:8]

        # 시리얼라이징 (context에 request 전달하여 is_liked 계산)
        serializer = BoxOfficeRankingSerializer(rankings, many=True, context={'request': request})

        # 플랫한 구조로 변환
        flattened_data = []
        for idx, item in enumerate(serializer.data, 1):
            performance_data = item.get('performance', {})
            flattened_item = {
                **performance_data,
                'rank': idx,
                'ranking_date': item.get('ranking_date'),
                'seat_count': item.get('seat_count'),
                'performance_count': item.get('performance_count'),
            }
            flattened_data.append(flattened_item)

        return Response({
            'success': True,
            'data': flattened_data
        })

    @action(detail=False, methods=['get'])
    def genres(self, request):
        """모든 장르 목록 조회"""
        genres = Performance.objects.values_list('genrenm', flat=True).distinct().order_by('genrenm')
        return Response({'genres': list(genres)})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='liked')
    def liked(self, request):
        """
        내가 찜한 공연 목록 조회
        GET /api/performances/liked/
        """
        queryset = Performance.objects.filter(like_users=request.user).select_related('detail')
        serializer = PerformanceListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        공연 찜하기/취소 토글
        POST /api/performances/{mt20id}/like/
        """
        performance = self.get_object()
        user = request.user

        if user in performance.like_users.all():
            # 찜 취소
            performance.like_users.remove(user)
            is_liked = False
        else:
            # 찜하기
            performance.like_users.add(user)
            is_liked = True

            # 추천 시스템 로그 저장
            from recommendations.models import UserLog
            UserLog.objects.create(
                user=user,
                performance=performance,
                action_type='like'
            )

        return Response({
            'success': True,
            'is_liked': is_liked,
            'like_count': performance.like_users.count()
        })

    @action(detail=False, methods=['post'], url_path='ai-search', permission_classes=[])
    def ai_search(self, request):
        """
        AI 의미 기반 검색
        POST /api/performances/ai-search/
        Body: { "query": "신나는 공연 추천해줘" }
        """
        query = request.data.get('query', '').strip()

        if not query:
            return Response({
                'success': False,
                'message': '검색어를 입력해주세요.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # AI 검색 엔진 초기화
            search_engine = AISearchEngine()

            # 유사한 공연 검색 (Top 10)
            results = search_engine.find_similar_performances(
                user_query=query,
                performances_qs=Performance.objects.all(),
                top_k=10
            )

            if not results:
                return Response({
                    'success': False,
                    'message': '검색 결과가 없습니다. 먼저 임베딩을 생성해주세요. (python manage.py generate_embeddings)'
                })

            # Top 1에 대한 AI 추천 사유 생성
            top_performance, top_score = results[0]
            ai_comment = search_engine.generate_recommendation_reason(
                user_input=query,
                performance=top_performance
            )

            # 시리얼라이징
            serialized_results = []

            for performance, score in results:
                serializer = PerformanceListSerializer(performance, context={'request': request})
                data = serializer.data
                data['similarity_score'] = round(score, 4)
                serialized_results.append(data)

            return Response({
                'success': True,
                'ai_comment': ai_comment,
                'results': serialized_results
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'검색 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BoxOfficeRankingViewSet(viewsets.ReadOnlyModelViewSet):
    """박스오피스 랭킹 ViewSet (읽기 전용)"""
    queryset = BoxOfficeRanking.objects.all()
    serializer_class = BoxOfficeRankingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['genre_code', 'ranking_date', 'period_type']
    ordering_fields = ['ranking_date', 'rank']
    ordering = ['-ranking_date', 'rank']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('performance')

        # 장르 코드로 필터링
        genre_code = self.request.query_params.get('genre_code', None)
        if genre_code:
            queryset = queryset.filter(genre_code=genre_code)

        return queryset

    @action(detail=False, methods=['get'])
    def latest_by_genre(self, request):
        """장르별 최신 랭킹 조회"""
        genre_code = request.query_params.get('genre_code', 'BBBC')

        rankings = self.get_queryset().filter(
            genre_code=genre_code
        ).order_by('-ranking_date', 'rank')[:20]

        serializer = self.get_serializer(rankings, many=True)
        return Response(serializer.data)
