from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.api_views import PerformanceViewSet, BoxOfficeRankingViewSet
from .views.management_api_views import (
    CollectBoxOfficeAPIView,
    CollectPerformancesAPIView,
    CollectPerformanceDetailAPIView,
    CreateTestBoxOfficeAPIView,
    DataStatsAPIView
)

app_name = "performances"

# DRF Router
router = DefaultRouter()
# 주의: 더 구체적인 경로(boxoffice)를 먼저 등록해야 함
router.register(r'boxoffice', BoxOfficeRankingViewSet, basename='boxoffice')
router.register(r'', PerformanceViewSet, basename='performance')

urlpatterns = [
    # Router URLs (performances/, boxoffice/)
    path('', include(router.urls)),

    # Management APIs (관리자 전용)
    path('management/collect-boxoffice/', CollectBoxOfficeAPIView.as_view(), name='collect-boxoffice'),
    path('management/collect-performances/', CollectPerformancesAPIView.as_view(), name='collect-performances'),
    path('management/collect-details/', CollectPerformanceDetailAPIView.as_view(), name='collect-details'),
    path('management/create-test-boxoffice/', CreateTestBoxOfficeAPIView.as_view(), name='create-test-boxoffice'),
    path('management/stats/', DataStatsAPIView.as_view(), name='data-stats'),
]
