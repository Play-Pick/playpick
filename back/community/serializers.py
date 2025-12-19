from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'username', 'created_at', 'updated_at']
        read_only_fields = ['user']


class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    performance_name = serializers.CharField(source='performance.prfnm', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'category', 'rank', 'performance', 'performance_name',
            'content', 'created_at', 'updated_at',
            'user', 'username', 'like_count', 'like_users', 'comments'
        ]
        read_only_fields = ['user']


class ArticleDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    performance_name = serializers.CharField(source='performance.prfnm', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'category', 'rank', 'performance', 'performance_name',
            'content', 'created_at', 'updated_at',
            'user', 'username', 'like_count', 'like_users', 'comments'
        ]
        read_only_fields = ['user']
