from django.db import models

# 장르 코드 매핑
GENRE_CODE_MAPPING = {
    'AAAA': '연극',
    'BBBC': '뮤지컬',
    'CCCA': '클래식',
    'CCCC': '오페라',
    'CCCD': '무용',
    'EEEA': '복합',
    'EEEB': '서커스/마술',
    'GGGA': '대중음악',
    'KID': '아동',
}

# 랜딩 페이지에 표시할 장르 순서
GENRE_DISPLAY_ORDER = ['BBBC', 'AAAA', 'CCCA', 'GGGA', 'CCCD']


class Performance(models.Model):
    # (필수) 공연 ID (PK) - "PF279020"
    mt20id = models.CharField(max_length=20, primary_key=True, verbose_name="공연 ID")
    
    # (필수) 공연명
    prfnm = models.CharField(max_length=255, verbose_name="공연명")
    
    # --- 기본 필드 ---
    prfpdfrom = models.DateField(verbose_name="공연시작일", null=True, blank=True)
    prfpdto = models.DateField(verbose_name="공연종료일", null=True, blank=True)
    fcltynm = models.CharField(max_length=100, verbose_name="공연시설명", null=True, blank=True)
    poster = models.URLField(max_length=2048, verbose_name="포스터URL", null=True, blank=True)
    area = models.CharField(max_length=50, verbose_name="지역", null=True, blank=True)
    genrenm = models.CharField(max_length=50, verbose_name="장르", null=True, blank=True)
    prfstate = models.CharField(max_length=50, verbose_name="공연상태", null=True, blank=True)
    openrun = models.CharField(max_length=5, null=True, blank=True)
    rnum = models.CharField(blank=True, null=True)

    # [Algorithm Optimization] 
    # 매번 Detail 테이블을 Join하지 않고 검색하기 위해 배우 목록 텍스트를 이곳에도 저장 (반정규화)
    # 예: "조승우 옥주현" -> LIKE 검색용
    cast_search_text = models.TextField(verbose_name="검색용 출연진 텍스트", blank=True, null=True)

    def __str__(self):
        return self.prfnm

    @property
    def has_detail(self):
        return hasattr(self, 'detail')

    def get_detail(self):
        try:
            return self.detail
        except PerformanceDetail.DoesNotExist:
            return None

    class Meta:
        indexes = [
            models.Index(fields=['prfstate']),
            models.Index(fields=['genrenm']),
            models.Index(fields=['prfpdfrom', 'prfpdto']),
            models.Index(fields=['area']),
            # 검색 최적화 인덱스 추가 (선택사항)
            # models.Index(fields=['cast_search_text']), 
        ]


class BoxOfficeRanking(models.Model):
    """KOPIS 예매상황판 랭킹 데이터 (Raw Data)"""
    # ... 기존 코드 유지 (변경 없음) ...
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='box_office_rankings',
        verbose_name="공연"
    )
    rank = models.IntegerField(verbose_name="순위")
    genre_code = models.CharField(max_length=10, verbose_name="장르코드")
    ranking_date = models.DateField(verbose_name="랭킹 기준일")
    period_type = models.CharField(
        max_length=10,
        choices=[('day', '일간'), ('week', '주간'), ('month', '월간')],
        default='week',
        verbose_name="기간유형"
    )
    area = models.CharField(max_length=50, verbose_name="지역", null=True, blank=True)
    seat_count = models.IntegerField(verbose_name="좌석수", default=0)
    performance_count = models.IntegerField(verbose_name="공연횟수", default=0)
    collected_at = models.DateTimeField(auto_now_add=True, verbose_name="수집일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "박스오피스 랭킹"
        verbose_name_plural = "박스오피스 랭킹 목록"
        ordering = ['ranking_date', 'genre_code', 'rank']
        indexes = [
            models.Index(fields=['genre_code', 'ranking_date', 'rank']),
            models.Index(fields=['ranking_date', '-collected_at']),
            models.Index(fields=['performance', 'ranking_date']),
        ]
        unique_together = [['ranking_date', 'genre_code', 'rank', 'period_type']]

    def __str__(self):
        genre_name = GENRE_CODE_MAPPING.get(self.genre_code, self.genre_code)
        return f"{self.ranking_date} {genre_name} {self.rank}위 - {self.performance.prfnm}"


class PerformanceDetail(models.Model):
    """공연 상세 정보 (KOPIS 공연상세 API)"""
    # ... 기존 코드 유지 (변경 없음) ...
    performance = models.OneToOneField(
        Performance,
        on_delete=models.CASCADE,
        related_name='detail',
        primary_key=True,
        verbose_name="공연"
    )
    prfcast = models.TextField(verbose_name="출연진", blank=True)
    prfcrew = models.TextField(verbose_name="제작진", blank=True)
    prfruntime = models.CharField(max_length=50, verbose_name="공연시간", blank=True)
    prfage = models.CharField(max_length=50, verbose_name="관람연령", blank=True)
    entrpsnm = models.CharField(max_length=200, verbose_name="제작사", blank=True)
    pcseguidance = models.TextField(verbose_name="티켓가격", blank=True)
    sty = models.TextField(verbose_name="줄거리", blank=True)
    dtguidance = models.TextField(verbose_name="공연시간안내", blank=True)
    relates = models.JSONField(verbose_name="예매처", default=list, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True, verbose_name="수집일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "공연 상세 정보"
        verbose_name_plural = "공연 상세 정보 목록"

    def __str__(self):
        return f"{self.performance.prfnm} - 상세정보"


class PerformanceImage(models.Model):
    """공연 소개 이미지 (styurls)"""
    # ... 기존 코드 유지 (변경 없음) ...
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='intro_images',
        verbose_name="공연"
    )
    image_url = models.URLField(verbose_name="이미지 URL")
    order = models.IntegerField(default=0, verbose_name="순서")
    collected_at = models.DateTimeField(auto_now_add=True, verbose_name="수집일시")

    class Meta:
        verbose_name = "공연 소개 이미지"
        verbose_name_plural = "공연 소개 이미지 목록"
        ordering = ['performance', 'order']
        indexes = [
            models.Index(fields=['performance', 'order']),
        ]

    def __str__(self):
        return f"{self.performance.prfnm} - 이미지 {self.order + 1}"


# ==========================================
# [New] 추천 알고리즘 전용 Metric 테이블
# ==========================================

class PerformanceMetric(models.Model):
    """
    추천 알고리즘(f4, f5, f6)을 위해 미리 계산된 점수와 데이터를 저장하는 캐시 테이블
    Batch Job을 통해 주기적으로 업데이트됨.
    """
    performance = models.OneToOneField(
        Performance,
        on_delete=models.CASCADE,
        related_name='metric',
        primary_key=True,
        verbose_name="공연"
    )

    # f4: 대중성 점수 (BoxOfficeRanking과 예매율 등을 종합하여 0~1 사이로 정규화한 값)
    score_popularity = models.FloatField(default=0.0, verbose_name="대중성 점수")

    # f5: 최신성 점수 (공연 시작일/종료일 기준으로 Time Decay 적용된 값)
    score_recency = models.FloatField(default=0.0, verbose_name="최신성 점수")

    # f6: 아이템 기반 협업 필터링 결과 (JSON)
    # 매번 유사도를 계산하지 않고, 미리 계산된 '유사 공연 ID 리스트'를 저장
    # 예: ["PF111", "PF222", "PF333"]
    similar_performances = models.JSONField(
        default=list, 
        blank=True, 
        verbose_name="유사 공연 ID 목록"
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="통계 갱신일시")

    class Meta:
        verbose_name = "공연 추천 지표"
        verbose_name_plural = "공연 추천 지표 목록"
        indexes = [
            # 정렬 기준이 되는 점수들에 인덱스 추가
            models.Index(fields=['-score_popularity']),
            models.Index(fields=['-score_recency']),
        ]

    def __str__(self):
        return f"{self.performance.prfnm} - 지표"