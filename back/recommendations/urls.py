from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.api_views import UserLogViewSet, RecommendationViewSet

app_name = 'recommendations'

# DRF Router
router = DefaultRouter()
router.register(r'log', UserLogViewSet, basename='userlog')
router.register(r'', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
