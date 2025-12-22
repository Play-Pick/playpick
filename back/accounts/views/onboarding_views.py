from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..models import UserPerformanceSignal
from ..services.onboarding_service import (
    get_onboarding_candidates,
    save_user_signals,
    complete_onboarding
)
from performances.serializers import PerformanceListSerializer


class OnboardingViewSet(viewsets.ViewSet):
    """
    API endpoints for user onboarding
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def candidates(self, request):
        """
        Get 16 performances for onboarding selection

        GET /api/onboarding/candidates/

        Query params:
        - strategy: 'balanced' (default), 'popular', 'recent'
        - exclude: Comma-separated mt20ids to exclude (e.g., 'PF123,PF456,PF789')

        Response:
        {
            "performances": [
                {
                    "mt20id": "PF123",
                    "prfnm": "뮤지컬 <위키드>",
                    "poster": "http://...",
                    "genrenm": "뮤지컬",
                    ...
                },
                ...
            ],
            "count": 16
        }
        """
        strategy = request.query_params.get('strategy', 'balanced')

        # Parse exclude parameter
        exclude_param = request.query_params.get('exclude', '')
        exclude_ids = None
        if exclude_param:
            # Split by comma and filter out empty strings
            exclude_ids = [mt20id.strip() for mt20id in exclude_param.split(',') if mt20id.strip()]

        performances = get_onboarding_candidates(
            count=16,
            strategy=strategy,
            exclude_ids=exclude_ids
        )

        serializer = PerformanceListSerializer(performances, many=True)

        return Response({
            'performances': serializer.data,
            'count': len(serializer.data)
        })

    @action(detail=False, methods=['post'])
    def signals(self, request):
        """
        Save user reaction signals

        POST /api/onboarding/signals/

        Request body:
        {
            "signals": [
                {"performance_id": "PF123", "signal": 1.5},
                {"performance_id": "PF456", "signal": -1.0},
                ...
            ]
        }

        Response:
        {
            "success": true,
            "saved": 8,
            "message": "8개의 선호도가 저장되었습니다."
        }
        """
        user = request.user
        signals_data = request.data.get('signals', [])

        if not signals_data or len(signals_data) < 8:
            return Response(
                {'error': '최소 8개의 공연을 선택해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                saved_count = save_user_signals(user, signals_data)

            return Response({
                'success': True,
                'saved': saved_count,
                'message': f'{saved_count}개의 선호도가 저장되었습니다.'
            })

        except Exception as e:
            return Response(
                {'error': f'저장 실패: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def complete(self, request):
        """
        Complete onboarding process

        POST /api/onboarding/complete/

        Response:
        {
            "success": true,
            "has_onboarded": true,
            "signal_count": 10,
            "message": "온보딩이 완료되었습니다!"
        }
        """
        user = request.user

        # Check minimum signals
        signal_count = UserPerformanceSignal.objects.filter(user=user).count()
        if signal_count < 8:
            return Response(
                {'error': '최소 8개의 공연을 선택해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                preference = complete_onboarding(user)

            return Response({
                'success': True,
                'has_onboarded': True,
                'signal_count': preference.signal_count,
                'message': '온보딩이 완료되었습니다!'
            })

        except Exception as e:
            return Response(
                {'error': f'온보딩 완료 실패: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
