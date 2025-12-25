from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.api_views import ArticleViewSet, CommentViewSet

app_name = 'community'

# DRF Router
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
