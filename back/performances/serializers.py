from rest_framework import serializers
from .models import Performance, BoxOfficeRanking, PerformanceDetail, PerformanceImage


class PerformanceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceImage
        fields = ['id', 'image_url', 'order']


class PerformanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceDetail
        fields = [
            'prfcast', 'prfcrew', 'prfruntime', 'prfage',
            'entrpsnm', 'pcseguidance', 'sty', 'dtguidance',
            'relates', 'collected_at', 'updated_at'
        ]


class PerformanceListSerializer(serializers.ModelSerializer):
    """공연 목록용 Serializer (기본 정보만)"""
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Performance
        fields = [
            'mt20id', 'prfnm', 'prfpdfrom', 'prfpdto',
            'fcltynm', 'poster', 'area', 'genrenm',
            'prfstate', 'openrun', 'is_liked', 'like_count'
        ]

    def get_is_liked(self, obj):
        """현재 사용자가 찜했는지 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False


class PerformanceDetailViewSerializer(serializers.ModelSerializer):
    """공연 상세 조회용 Serializer (모든 정보 포함)"""
    detail = PerformanceDetailSerializer(read_only=True)
    intro_images = PerformanceImageSerializer(many=True, read_only=True)
    has_detail = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = [
            'mt20id', 'prfnm', 'prfpdfrom', 'prfpdto',
            'fcltynm', 'poster', 'area', 'genrenm',
            'prfstate', 'openrun', 'rnum',
            'has_detail', 'detail', 'intro_images',
            'is_liked', 'like_count', 'is_watched'
        ]

    def get_is_liked(self, obj):
        """현재 사용자가 찜했는지 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

    def get_is_watched(self, obj):
        """현재 사용자가 관람했는지 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from accounts.models import WatchedPerformance
            return WatchedPerformance.objects.filter(
                user=request.user,
                performance=obj
            ).exists()
        return False


class BoxOfficeRankingSerializer(serializers.ModelSerializer):
    performance = PerformanceListSerializer(read_only=True)

    class Meta:
        model = BoxOfficeRanking
        fields = [
            'id', 'performance', 'rank', 'genre_code',
            'ranking_date', 'period_type', 'area',
            'seat_count', 'performance_count', 'collected_at'
        ]
