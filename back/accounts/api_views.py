from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserDetailSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """사용자 ViewSet"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'me':
            return UserDetailSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve' or self.action == 'me':
            queryset = queryset.prefetch_related('followers', 'followings')

        return queryset

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """현재 로그인한 사용자 정보"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        """팔로우/언팔로우 토글"""
        target_user = self.get_object()
        current_user = request.user

        # 자기 자신을 팔로우할 수 없음
        if target_user == current_user:
            return Response(
                {'error': '자기 자신을 팔로우할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if current_user.followings.filter(pk=target_user.pk).exists():
            current_user.followings.remove(target_user)
            is_following = False
        else:
            current_user.followings.add(target_user)
            is_following = True

        return Response({
            'is_following': is_following,
            'followers_count': target_user.followers.count(),
            'followings_count': target_user.followings.count()
        })


class RegisterView(generics.CreateAPIView):
    """회원가입 View"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
