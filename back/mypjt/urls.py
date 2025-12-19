"""
URL configuration for mypjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from performances import views as performance_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from performances.api_views import PerformanceViewSet, BoxOfficeRankingViewSet
from community.api_views import ArticleViewSet, CommentViewSet
from accounts.api_views import UserViewSet, RegisterView
from recommendations.api_views import UserLogViewSet, RecommendationViewSet
from performances.management_api_views import (
    CollectBoxOfficeAPIView,
    CollectPerformancesAPIView,
    CollectPerformanceDetailAPIView,
    CreateTestBoxOfficeAPIView,
    DataStatsAPIView
)

# DRF Router 설정
router = DefaultRouter()
router.register(r'performances', PerformanceViewSet, basename='performance')
router.register(r'boxoffice', BoxOfficeRankingViewSet, basename='boxoffice')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserViewSet, basename='user')
router.register(r'recommendations/log', UserLogViewSet, basename='userlog')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', performance_views.landing, name='landing'),
    # API 엔드포인트 (Vue 프론트엔드용)
    path('api/', include(router.urls)),
    # JWT 인증
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 회원가입
    path('api/register/', RegisterView.as_view(), name='register'),
    # 관리자 전용 - 데이터 수집 API
    path('api/management/collect-boxoffice/', CollectBoxOfficeAPIView.as_view(), name='collect-boxoffice'),
    path('api/management/collect-performances/', CollectPerformancesAPIView.as_view(), name='collect-performances'),
    path('api/management/collect-details/', CollectPerformanceDetailAPIView.as_view(), name='collect-details'),
    path('api/management/create-test-boxoffice/', CreateTestBoxOfficeAPIView.as_view(), name='create-test-boxoffice'),
    path('api/management/stats/', DataStatsAPIView.as_view(), name='data-stats'),
    # DRF 인증 (개발용)
    path('api/auth/', include('rest_framework.urls')),
    # 기존 템플릿 기반 뷰
    path('community/', include('community.urls')),
    path('accounts/', include('accounts.urls')),
    path('performances/', include('performances.urls')),
]
