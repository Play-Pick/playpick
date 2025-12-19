from django.db import models
from django.conf import settings
from performances.models import Performance


class UserLog(models.Model):
    """
    사용자 행동 로그 (User Behavior Log)
    추천 알고리즘의 f1 (클릭/관심 기반 점수) 계산을 위한 로그 데이터
    """
    ACTION_CHOICES = (
        ('view', '조회'),
        ('like', '찜하기'),
        ('search', '검색'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_logs',
        verbose_name="사용자"
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='user_logs',
        verbose_name="공연"
    )
    action_type = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        verbose_name="행동 유형"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="발생 시각"
    )

    class Meta:
        verbose_name = "사용자 행동 로그"
        verbose_name_plural = "사용자 행동 로그 목록"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['performance', '-timestamp']),
            models.Index(fields=['action_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_action_type_display()} - {self.performance.prfnm}"


class RecommendationCache(models.Model):
    """
    추천 결과 캐시 (Recommendation Result Cache)
    실시간 연산 부하를 줄이기 위해 유저별 추천 결과를 저장
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendation_cache',
        primary_key=True,
        verbose_name="사용자"
    )

    # 추천 결과: [{"mt20id": "PF123", "score": 0.85, "reason": "location"}, ...]
    top_n_list = models.JSONField(
        default=list,
        blank=True,
        verbose_name="추천 목록"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="갱신 일시"
    )

    class Meta:
        verbose_name = "추천 결과 캐시"
        verbose_name_plural = "추천 결과 캐시 목록"

    def __str__(self):
        return f"{self.user.username}의 추천 캐시"

    def is_fresh(self, max_age_hours=1):
        """
        캐시가 유효한지 확인 (기본: 1시간)
        """
        from django.utils import timezone
        from datetime import timedelta

        if not self.top_n_list:
            return False

        age = timezone.now() - self.updated_at
        return age < timedelta(hours=max_age_hours)
