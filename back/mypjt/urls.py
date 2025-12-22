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
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from community.api_views import ArticleViewSet, CommentViewSet
# from accounts.views.api_views import UserViewSet, RegisterView
from recommendations.api_views import UserLogViewSet, RecommendationViewSet

# DRF Router 설정
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
# router.register(r'users', UserViewSet, basename='user')
router.register(r'recommendations/log', UserLogViewSet, basename='userlog')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 엔드포인트 (Vue 프론트엔드용)
    path('api/performances/', include('performances.urls')),
    path('api/accounts/', include('accounts.urls')),

    path('api/', include(router.urls)),
    # JWT 인증
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 회원가입
    # path('api/register/', RegisterView.as_view(), name='register'),
    # DRF 인증 (개발용)
    path('api/auth/', include('rest_framework.urls')),
]
