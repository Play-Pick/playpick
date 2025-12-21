from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'followers_count', 'followings_count']


class UserDetailSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nickname', 'date_joined',
            'is_staff', 'is_superuser',
            'followers', 'followings',
            'followers_count', 'followings_count'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입용 Serializer"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'nickname', 'birth_date', 'region',
            'preference_tags', 'favorite_actors'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'nickname': {'required': False},
            'birth_date': {'required': False},
            'region': {'required': False},
            'preference_tags': {'required': False},
            'favorite_actors': {'required': False},
        }

    def validate(self, attrs):
        """비밀번호 확인"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "비밀번호가 일치하지 않습니다."
            })
        return attrs

    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.get('email', ''),
            password=password,
            **validated_data
        )
        return user
