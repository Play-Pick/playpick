from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'username', 'nickname', 'created_at', 'updated_at']
        read_only_fields = ['user']


class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    performance_name = serializers.CharField(source='performance.prfnm', read_only=True)
    performance_poster = serializers.CharField(source='performance.poster', read_only=True)
    performance_area = serializers.CharField(source='performance.area', read_only=True)
    prfpdfrom = serializers.DateField(source='performance.prfpdfrom', read_only=True)
    prfpdto = serializers.DateField(source='performance.prfpdto', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'board_type', 'category', 'rank', 'performance', 'performance_name',
            'performance_poster', 'performance_area', 'prfpdfrom', 'prfpdto',
            'content', 'created_at', 'updated_at',
            'user', 'username', 'nickname', 'like_count', 'is_liked', 'like_users', 'comments'
        ]
        read_only_fields = ['user']

    def get_is_liked(self, obj):
        """현재 사용자가 좋아요했는지 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

    def validate(self, data):
        """
        board_type과 category, performance 간의 관계를 검증
        """
        board_type = data.get('board_type', 'PERFORMANCE')
        category = data.get('category')
        performance = data.get('performance')

        # PERFORMANCE 타입 검증
        if board_type == 'PERFORMANCE':
            # performance가 필수
            if not performance:
                raise serializers.ValidationError({
                    'performance': '공연글은 반드시 공연을 선택해야 합니다.'
                })
            # 허용된 카테고리만 사용 가능
            if category not in ['REVIEW', 'EXPECTATION', 'QNA']:
                raise serializers.ValidationError({
                    'category': '공연글은 후기, 기대평, 질문 카테고리만 사용할 수 있습니다.'
                })
            # REVIEW, EXPECTATION은 별점 필수
            if category in ['REVIEW', 'EXPECTATION'] and not data.get('rank'):
                raise serializers.ValidationError({
                    'rank': f'{category} 카테고리는 별점이 필수입니다.'
                })

        # GENERAL 타입 검증
        elif board_type == 'GENERAL':
            # performance가 null이어야 함
            if performance:
                raise serializers.ValidationError({
                    'performance': '일반글은 공연을 선택할 수 없습니다.'
                })
            # 허용된 카테고리만 사용 가능
            if category not in ['FREE', 'INFO']:
                raise serializers.ValidationError({
                    'category': '일반글은 자유게시판, 정보공유 카테고리만 사용할 수 있습니다.'
                })

        return data


class ArticleDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    performance_name = serializers.CharField(source='performance.prfnm', read_only=True)
    performance_poster = serializers.CharField(source='performance.poster', read_only=True)
    performance_area = serializers.CharField(source='performance.area', read_only=True)
    prfpdfrom = serializers.DateField(source='performance.prfpdfrom', read_only=True)
    prfpdto = serializers.DateField(source='performance.prfpdto', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'board_type', 'category', 'rank', 'performance', 'performance_name',
            'performance_poster', 'performance_area', 'prfpdfrom', 'prfpdto',
            'content', 'created_at', 'updated_at',
            'user', 'username', 'nickname', 'like_count', 'is_liked', 'like_users', 'comments'
        ]
        read_only_fields = ['user']

    def get_is_liked(self, obj):
        """현재 사용자가 좋아요했는지 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

    def validate(self, data):
        """
        board_type과 category, performance 간의 관계를 검증
        """
        board_type = data.get('board_type', self.instance.board_type if self.instance else 'PERFORMANCE')
        category = data.get('category', self.instance.category if self.instance else None)
        performance = data.get('performance', self.instance.performance if self.instance else None)

        # PERFORMANCE 타입 검증
        if board_type == 'PERFORMANCE':
            # performance가 필수
            if not performance:
                raise serializers.ValidationError({
                    'performance': '공연글은 반드시 공연을 선택해야 합니다.'
                })
            # 허용된 카테고리만 사용 가능
            if category not in ['REVIEW', 'EXPECTATION', 'QNA']:
                raise serializers.ValidationError({
                    'category': '공연글은 후기, 기대평, 질문 카테고리만 사용할 수 있습니다.'
                })
            # REVIEW, EXPECTATION은 별점 필수
            rank = data.get('rank', self.instance.rank if self.instance else None)
            if category in ['REVIEW', 'EXPECTATION'] and not rank:
                raise serializers.ValidationError({
                    'rank': f'{category} 카테고리는 별점이 필수입니다.'
                })

        # GENERAL 타입 검증
        elif board_type == 'GENERAL':
            # performance가 null이어야 함
            if performance:
                raise serializers.ValidationError({
                    'performance': '일반글은 공연을 선택할 수 없습니다.'
                })
            # 허용된 카테고리만 사용 가능
            if category not in ['FREE', 'INFO']:
                raise serializers.ValidationError({
                    'category': '일반글은 자유게시판, 정보공유 카테고리만 사용할 수 있습니다.'
                })

        return data
