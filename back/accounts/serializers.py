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
            'followers_count', 'followings_count',
            'has_onboarded', 'onboarded_at',
            'profile_image', 'region', 'birth_date',
            'preference_tags', 'favorite_actors'
        ]
        read_only_fields = ['id', 'date_joined', 'has_onboarded', 'onboarded_at']


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
            'preference_tags'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'nickname': {'required': False},
            'birth_date': {'required': False},
            'region': {'required': False},
            'preference_tags': {'required': False},
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


class PasswordVerifySerializer(serializers.Serializer):
    """비밀번호 확인용 Serializer"""
    password = serializers.CharField(write_only=True, required=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    """회원정보 수정용 Serializer"""
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'email', 'birth_date', 'region',
            'preference_tags', 'profile_image',
            'password', 'password2'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'birth_date': {'required': False},
            'region': {'required': False},
            'preference_tags': {'required': False},
            'profile_image': {'required': False},
        }

    def validate(self, attrs):
        """비밀번호 확인 (비밀번호 변경 시에만)"""
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password or password2:
            if password != password2:
                raise serializers.ValidationError({
                    "password2": "비밀번호가 일치하지 않습니다."
                })

        return attrs

    def update(self, instance, validated_data):
        """사용자 정보 업데이트"""
        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        # 일반 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 비밀번호 변경이 있을 경우
        if password:
            instance.set_password(password)

        instance.save()
        return instance
