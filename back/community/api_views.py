from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CommentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """게시글 ViewSet"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # list와 retrieve 모두 comments와 like_users를 prefetch
        queryset = queryset.prefetch_related(
            'comments',
            'comments__user',  # 댓글 작성자 정보도 함께 가져오기
            'like_users'
        )

        return queryset.select_related('user', 'performance').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # 작성자만 수정 가능
        if serializer.instance.user != self.request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        # 작성자만 삭제 가능
        if instance.user != self.request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """게시글 좋아요/취소 토글"""
        article = self.get_object()
        user = request.user

        if user in article.like_users.all():
            article.like_users.remove(user)
            is_liked = False
        else:
            article.like_users.add(user)
            is_liked = True

        return Response({
            'is_liked': is_liked,
            'like_count': article.like_users.count()
        })


class CommentViewSet(viewsets.ModelViewSet):
    """댓글 ViewSet"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        article_id = self.request.query_params.get('article', None)

        if article_id:
            queryset = queryset.filter(article_id=article_id)

        return queryset.select_related('user', 'article')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {'error': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
