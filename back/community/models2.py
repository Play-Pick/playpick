from django.db import models
from django.conf import settings
from performances.models import Performance  # 공연 모델 import

class Article(models.Model):
    """
    기존 Review 모델을 확장하여 리뷰, 질문, 잡담 등을 모두 포함하는 게시글(Article) 모델
    """
    
    # [3. 게시글 타입 정의]
    CATEGORY_CHOICES = (
        ('REVIEW', '후기'),      # 별점 필수
        ('QNA', '질문'),         # 별점 불필요
        ('FREE', '자유게시판'),   # 별점 불필요
        ('INFO', '정보공유'),
        ('EXPECT', '기대평'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='articles'
    )

    # [1. Performance 연결]
    # 공연에 달린 글이므로 ForeignKey 연결
    # related_name='articles'로 설정하여, Performance 쪽에서 performance.articles.all()로 역참조 가능
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE, # 공연 삭제되면 리뷰도 삭제 (정책에 따라 SET_NULL 가능)
        related_name='articles',
        verbose_name="관련 공연"
    )

    # [3. 글 타입 필드]
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES, 
        default='REVIEW',
        verbose_name="카테고리"
    )

    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    
    # [Refactor] 별점 (rank)
    # 질문이나 자유글에는 별점이 없으므로 null=True 허용
    rank = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="평점(1~5)"
    )

    # 좋아요 기능
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='like_articles',
        blank=True # 좋아요 없는 상태 허용
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ['-created_at'] # 최신글 우선

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} - {self.user.username}"


class Comment(models.Model):
    # Review -> Article로 변경됨에 따라 변수명 수정
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="게시글"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    content = models.TextField(verbose_name="댓글 내용")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ['created_at'] # 댓글은 작성순

    def __str__(self):
        return f"{self.content[:20]}.. - {self.user.username}"