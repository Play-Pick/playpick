from rest_framework import serializers
from .models import UserLog, RecommendationCache
from performances.models import Performance


class UserLogSerializer(serializers.ModelSerializer):
    """
    사용자 행동 로그 Serializer
    POST /api/recommendations/log/ 요청에 사용
    """
    performance_id = serializers.CharField(write_only=True, help_text="공연 ID (mt20id)")

    class Meta:
        model = UserLog
        fields = ['id', 'performance_id', 'action_type', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def validate_performance_id(self, value):
        """공연 ID 유효성 검사"""
        try:
            Performance.objects.get(mt20id=value)
        except Performance.DoesNotExist:
            raise serializers.ValidationError(f"공연 ID '{value}'를 찾을 수 없습니다.")
        return value

    def validate_action_type(self, value):
        """행동 유형 유효성 검사"""
        allowed_types = ['view', 'like', 'search']
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"행동 유형은 {allowed_types} 중 하나여야 합니다."
            )
        return value

    def create(self, validated_data):
        """로그 생성 (user는 request.user로 자동 설정)"""
        performance_id = validated_data.pop('performance_id')
        performance = Performance.objects.get(mt20id=performance_id)

        return UserLog.objects.create(
            performance=performance,
            **validated_data
        )


class RecommendationItemSerializer(serializers.Serializer):
    """
    개별 추천 항목 Serializer
    추천 엔진에서 반환한 데이터를 공연 정보와 결합
    """
    # 추천 메타 정보
    mt20id = serializers.CharField()
    score = serializers.FloatField()
    reason = serializers.CharField()
    reason_text = serializers.CharField()

    # 공연 기본 정보 (Performance 모델에서 조회)
    prfnm = serializers.CharField(read_only=True)
    poster = serializers.URLField(read_only=True)
    prfpdfrom = serializers.DateField(read_only=True)
    prfpdto = serializers.DateField(read_only=True)
    fcltynm = serializers.CharField(read_only=True)
    genrenm = serializers.CharField(read_only=True)
    area = serializers.CharField(read_only=True)


class RecommendationListSerializer(serializers.Serializer):
    """
    추천 목록 전체 응답 Serializer
    GET /api/recommendations/list/ 응답에 사용
    """
    recommendations = RecommendationItemSerializer(many=True)
    cached = serializers.BooleanField(help_text="캐시에서 가져왔는지 여부")
    updated_at = serializers.DateTimeField(help_text="마지막 갱신 시각")


class RecommendationCacheSerializer(serializers.ModelSerializer):
    """
    추천 캐시 Serializer (Admin 또는 내부 사용)
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = RecommendationCache
        fields = ['user', 'username', 'top_n_list', 'updated_at']
        read_only_fields = ['updated_at']
