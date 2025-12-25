from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    [추천 알고리즘 지원을 위한 확장 User 모델]
    - f2 (취향 매칭): preference_tags, favorite_actors
    - f3 (위치 근접성): region_gu, region_dong
    """

    # 1. 기본 프로필
    nickname = models.CharField(max_length=20, blank=True, null=True, verbose_name="닉네임")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name="프로필 이미지")

    # 2. [f3] 위치 기반 추천을 위한 거주지 정보
    # KOPIS 데이터는 광역시/도 단위로 제공되므로 동일한 단위로 매칭
    # 예: '서울특별시', '경기도', '부산광역시' -> Performance.area와 매칭
    region = models.CharField(max_length=50, blank=True, null=True, verbose_name="거주 지역 (광역시/도)")

    # 3. [f2] 취향 매칭을 위한 선호 데이터 (JSON)
    # RDB(N:M) 대신 JSONField를 사용하여 조회 속도를 높이고 유연하게 저장

    # 예: ["뮤지컬", "로맨틱코미디", "화려한"] -> 태그 매칭 점수 계산
    preference_tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name="선호 장르/분위기 태그"
    )

    # 예: ["조승우", "옥주현"] -> 출연진 매칭 점수 계산
    favorite_actors = models.JSONField(
        default=list,
        blank=True,
        verbose_name="선호 배우 목록"
    )

    # 4. [f2-Add] 연령대 매칭을 위한 생년월일 (공연 관람연령 prfage 비교용)
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")

    # 5. 팔로잉 (기존 유지)
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        verbose_name="팔로잉"
    )

    # 6. 온보딩 추적
    has_onboarded = models.BooleanField(
        default=False,
        verbose_name="온보딩 완료 여부"
    )
    onboarded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="온보딩 완료 시각"
    )

    def __str__(self):
        return self.username

    # [Helper Method] 추천 시스템에서 나이 계산 시 사용
    @property
    def age(self):
        import datetime
        if self.birth_date:
            today = datetime.date.today()
            return today.year - self.birth_date.year
        return 0


class UserPreference(models.Model):
    """User preference vector derived from onboarding selections"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='preference',
        primary_key=True,
        verbose_name="사용자"
    )

    # 1536-dim vector (same as PerformanceEmbedding)
    preference_vector = models.JSONField(
        verbose_name="선호도 벡터",
        help_text="1536차원 사용자 선호 벡터 (normalized)"
    )

    # Metadata
    signal_count = models.IntegerField(
        default=0,
        verbose_name="시그널 개수",
        help_text="온보딩 시 선택한 공연 개수"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "사용자 선호도"
        verbose_name_plural = "사용자 선호도 목록"

    def __str__(self):
        return f"{self.user.username}의 선호도 벡터 ({self.signal_count}개 신호)"


class UserPerformanceSignal(models.Model):
    """Records user reactions to performances during onboarding"""

    SIGNAL_CHOICES = [
        (1.5, '보고싶어요'),
        (0.0, '모르겠어요'),
        (-1.0, '안보고싶어요'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='performance_signals',
        verbose_name="사용자"
    )

    performance = models.ForeignKey(
        'performances.Performance',
        on_delete=models.CASCADE,
        related_name='user_signals',
        verbose_name="공연"
    )

    signal = models.FloatField(
        choices=SIGNAL_CHOICES,
        verbose_name="반응"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "사용자 공연 시그널"
        verbose_name_plural = "사용자 공연 시그널 목록"
        unique_together = [['user', 'performance']]
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        signal_label = dict(self.SIGNAL_CHOICES).get(self.signal, '알 수 없음')
        return f"{self.user.username} → {self.performance.prfnm} ({signal_label})"


class WatchedPerformance(models.Model):
    """User watched performances tracking"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watched_performances',
        verbose_name="사용자"
    )

    performance = models.ForeignKey(
        'performances.Performance',
        on_delete=models.CASCADE,
        to_field='mt20id',
        related_name='watched_by_users',
        verbose_name="공연"
    )

    watched_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="관람 등록 시각"
    )

    # Optional: 향후 별점 기능 확장용
    rating = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="별점 (1-5)",
        help_text="1~5점 별점 (선택사항)"
    )

    class Meta:
        verbose_name = "관람한 공연"
        verbose_name_plural = "관람한 공연 목록"
        unique_together = [['user', 'performance']]
        indexes = [
            models.Index(fields=['user', 'watched_at']),
            models.Index(fields=['-watched_at']),
        ]
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user.username} → {self.performance.prfnm} (관람함)"
