from django.db import models
from django.conf import settings
from performances.models import Performance  # 공연 모델 import

class Article(models.Model):
    """
    기존 Review 모델을 확장하여 리뷰, 질문, 잡담 등을 모두 포함하는 게시글(Article) 모델
    board_type으로 공연글/일반글 구분
    """

    # 게시판 타입
    BOARD_TYPE_CHOICES = (
        ('PERFORMANCE', '공연글'),
        ('GENERAL', '일반글'),
    )

    # 카테고리 (board_type에 따라 허용되는 값이 다름)
    CATEGORY_CHOICES = (
        ('REVIEW', '후기'),       # PERFORMANCE only, 별점 필수
        ('EXPECTATION', '기대평'), # PERFORMANCE only, 별점 필수
        ('QNA', '질문'),          # PERFORMANCE only
        ('FREE', '자유게시판'),    # GENERAL only
        ('INFO', '정보공유'),      # GENERAL only
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    # 게시판 타입 (PERFORMANCE or GENERAL)
    board_type = models.CharField(
        max_length=20,
        choices=BOARD_TYPE_CHOICES,
        default='PERFORMANCE',
        verbose_name="게시판 타입"
    )

    # [1. Performance 연결]
    # PERFORMANCE 타입일 경우 필수, GENERAL일 경우 null
    # related_name='articles'로 설정하여, Performance 쪽에서 performance.articles.all()로 역참조 가능
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,  # 공연 삭제되면 리뷰도 삭제 (정책에 따라 SET_NULL 가능)
        related_name='articles',
        verbose_name="관련 공연",
        null=True,  # GENERAL 타입에서는 null 허용
        blank=True
    )

    # 카테고리 (board_type에 따라 허용되는 값이 다름)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='REVIEW',
        verbose_name="카테고리"
    )

    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")

    # [Refactor] 별점 (rank)
    # 질문이나 자유글에는 별점이 없으므로 null=True 허용
    # 0.5 단위 별점을 지원하기 위해 FloatField 사용
    rank = models.FloatField(
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
        db_table = 'community_review'  # 기존 테이블명 유지
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
