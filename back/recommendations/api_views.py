from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone

from .models import UserLog, RecommendationCache
from .serializers import (
    UserLogSerializer,
    RecommendationListSerializer,
    RecommendationItemSerializer
)
from .engine import RecommendationEngine
from performances.models import Performance


class UserLogViewSet(viewsets.ModelViewSet):
    """
    사용자 행동 로그 ViewSet

    - POST /api/recommendations/log/ : 로그 저장
    - GET /api/recommendations/log/ : 본인의 로그 조회
    """
    queryset = UserLog.objects.all()
    serializer_class = UserLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """본인의 로그만 조회 가능"""
        return super().get_queryset().filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        """로그 생성 시 자동으로 user 설정"""
        serializer.save(user=self.request.user)

        # 로그 생성 시 캐시 무효화 (선택사항)
        try:
            cache = RecommendationCache.objects.get(user=self.request.user)
            cache.delete()
        except RecommendationCache.DoesNotExist:
            pass

    def create(self, request, *args, **kwargs):
        """로그 생성 API"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'success': True,
            'message': '로그가 저장되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class RecommendationViewSet(viewsets.ViewSet):
    """
    추천 시스템 ViewSet

    - GET /api/recommendations/ : 추천 목록 조회
    - POST /api/recommendations/refresh/ : 캐시 갱신
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """
        GET /api/recommendations/
        사용자 맞춤 추천 목록 조회
        """
        if not request.user.is_authenticated:
            return Response({
                'error': '로그인이 필요한 서비스입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        top_n = int(request.query_params.get('top_n', 10))

        # 1. 캐시 확인
        try:
            cache = RecommendationCache.objects.get(user=user)
            if cache.is_fresh(max_age_hours=1):
                # 캐시가 유효하면 바로 반환
                recommendations = self._enrich_recommendations(cache.top_n_list[:top_n])
                return Response({
                    'recommendations': recommendations,
                    'cached': True,
                    'updated_at': cache.updated_at
                })
        except RecommendationCache.DoesNotExist:
            cache = None

        # 2. 캐시가 없거나 오래되면 엔진으로 계산
        engine = RecommendationEngine(user)
        raw_recommendations = engine.get_recommendations(top_n=top_n)

        # 3. 캐시 저장
        if cache:
            cache.top_n_list = raw_recommendations
            cache.save()
        else:
            RecommendationCache.objects.create(
                user=user,
                top_n_list=raw_recommendations
            )

        # 4. 공연 정보와 결합하여 반환
        recommendations = self._enrich_recommendations(raw_recommendations)

        return Response({
            'recommendations': recommendations,
            'cached': False,
            'updated_at': timezone.now()
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def refresh(self, request):
        """
        POST /api/recommendations/refresh/
        강제로 캐시 갱신
        """
        user = request.user
        top_n = int(request.data.get('top_n', 10))

        # 기존 캐시 삭제
        RecommendationCache.objects.filter(user=user).delete()

        # 새로 계산
        engine = RecommendationEngine(user)
        raw_recommendations = engine.get_recommendations(top_n=top_n)

        # 캐시 저장
        RecommendationCache.objects.create(
            user=user,
            top_n_list=raw_recommendations
        )

        # 공연 정보와 결합하여 반환
        recommendations = self._enrich_recommendations(raw_recommendations)

        return Response({
            'success': True,
            'message': '추천 목록이 갱신되었습니다.',
            'recommendations': recommendations,
            'updated_at': timezone.now()
        })

    def _enrich_recommendations(self, raw_recommendations):
        """
        추천 엔진의 결과에 공연 정보 추가

        Args:
            raw_recommendations: [
                {'mt20id': 'PF123', 'score': 0.85, 'reason': 'location', 'reason_text': '...'},
                ...
            ]

        Returns:
            list: 공연 정보가 포함된 추천 목록
        """
        enriched = []
        performance_ids = [item['mt20id'] for item in raw_recommendations]

        # 공연 정보 bulk 조회 (성능 최적화)
        performances = Performance.objects.filter(mt20id__in=performance_ids).in_bulk(field_name='mt20id')

        for item in raw_recommendations:
            performance = performances.get(item['mt20id'])
            if performance:
                enriched.append({
                    # 추천 메타 정보
                    'mt20id': item['mt20id'],
                    'score': item['score'],
                    'reason': item['reason'],
                    'reason_text': item['reason_text'],

                    # 공연 기본 정보
                    'prfnm': performance.prfnm,
                    'poster': performance.poster,
                    'prfpdfrom': performance.prfpdfrom,
                    'prfpdto': performance.prfpdto,
                    'fcltynm': performance.fcltynm,
                    'genrenm': performance.genrenm,
                    'area': performance.area,
                })

        return enriched
