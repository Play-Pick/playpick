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
    # 예: '강남구', '역삼동' -> 공연장 주소와 매칭하여 거리 점수 계산
    region_gu = models.CharField(max_length=50, blank=True, null=True, verbose_name="거주 구 (Gu)")
    region_dong = models.CharField(max_length=50, blank=True, null=True, verbose_name="거주 동 (Dong)")

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
