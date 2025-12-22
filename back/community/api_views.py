from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
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

        queryset = queryset.select_related('user', 'performance')

        # 필터링 (list action일 때만)
        if self.action == 'list':
            # board_type 필터
            board_type = self.request.query_params.get('board_type', None)
            if board_type:
                queryset = queryset.filter(board_type=board_type)

            # category 필터
            category = self.request.query_params.get('category', None)
            if category:
                queryset = queryset.filter(category=category)

            # performance_mt20id 필터 (mt20id 기반)
            performance_mt20id = self.request.query_params.get('performance_mt20id', None)
            if performance_mt20id:
                queryset = queryset.filter(performance__mt20id=performance_mt20id)

            # 검색 (제목 + 내용)
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(content__icontains=search)
                )

            # 정렬
            ordering = self.request.query_params.get('ordering', '-created_at')
            if ordering in ['-created_at', 'created_at', '-like_count', 'like_count']:
                if 'like_count' in ordering:
                    # 좋아요 수로 정렬 시 annotate 필요
                    from django.db.models import Count
                    queryset = queryset.annotate(like_count_num=Count('like_users'))
                    queryset = queryset.order_by(
                        '-like_count_num' if ordering == '-like_count' else 'like_count_num'
                    )
                else:
                    queryset = queryset.order_by(ordering)
            else:
                queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

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

    @action(detail=False, methods=['get'], url_path='best-reviews')
    def best_reviews(self, request):
        """
        베스트 관람후기 조회
        GET /api/community/posts/best-reviews/?limit=4
        - 최근 14일의 "후기" 글 중 좋아요 수 내림차순, 동점이면 최신순
        """
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count

        limit = int(request.query_params.get('limit', 4))
        two_weeks_ago = timezone.now() - timedelta(days=14)

        # 최근 14일의 REVIEW 카테고리 글 중 좋아요 수 기준 정렬
        queryset = Article.objects.filter(
            board_type='PERFORMANCE',
            category='REVIEW',
            created_at__gte=two_weeks_ago
        ).annotate(
            like_count_num=Count('like_users')
        ).filter(
            like_count_num__gt=0  # 좋아요가 1개 이상인 글만
        ).select_related('user', 'performance').prefetch_related(
            'like_users'
        ).order_by('-like_count_num', '-created_at')[:limit]

        serializer = ArticleListSerializer(queryset, many=True, context={'request': request})
        return Response({
            'success': True,
            'results': serializer.data,
            'count': len(serializer.data)
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
