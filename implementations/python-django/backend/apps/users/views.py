from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    User, UserProfile, UserStatus, UserAction, UserPermission,
    Follow, Block, DirectMessage, LoginHistory, TwoFactorAuth,
    AuthorPermissionRequest
)
from .serializers import (
    UserSerializer, UserPublicSerializer, RegisterSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    UserProfileSerializer, UserStatusSerializer, UserActionSerializer,
    UserPermissionSerializer, FollowSerializer, BlockSerializer,
    DirectMessageSerializer, LoginHistorySerializer, TwoFactorAuthSerializer,
    AuthorPermissionRequestSerializer, AuthorPermissionRequestReviewSerializer
)


class RegisterView(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # ログイン履歴を記録
            user_data = response.data.get('user')
            if user_data:
                try:
                    user = User.objects.get(id=user_data['id'])
                    ip_address = request.META.get('REMOTE_ADDR')
                    user_agent = request.META.get('HTTP_USER_AGENT', '')
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=ip_address,
                        user_agent=user_agent,
                    )
                except User.DoesNotExist:
                    pass
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted_at__isnull=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['created_at', 'username']

    def get_serializer_class(self):
        if self.request.user.is_authenticated and (
            self.request.user.is_staff or
            (self.kwargs.get('pk') and str(self.kwargs['pk']) == str(self.request.user.id))
        ):
            return UserSerializer
        return UserPublicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            if not self.request.user.is_authenticated:
                self.permission_denied(self.request)
            return self.request.user
        return super().get_object()

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': '現在のパスワードが正しくありません。'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'パスワードを変更しました。'})

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'detail': 'ログアウトしました。'})


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        profile = self.get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['follower', 'followee']

    def get_queryset(self):
        return Follow.objects.filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        follow = self.get_object()
        if follow.follower != request.user:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        follow.deleted_at = timezone.now()
        follow.save()
        return Response({'detail': 'フォローを解除しました。'})


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Block.objects.filter(blocker=self.request.user)

    def perform_create(self, serializer):
        serializer.save(blocker=self.request.user)


class DirectMessageViewSet(viewsets.ModelViewSet):
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            receiver=user
        ).select_related('sender', 'sender__profile')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        if message.receiver != request.user:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        message.is_read = True
        message.save()
        return Response({'detail': '既読にしました。'})


class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return LoginHistory.objects.all()
        return LoginHistory.objects.filter(user=self.request.user)


class UserStatusViewSet(viewsets.ModelViewSet):
    queryset = UserStatus.objects.all()
    serializer_class = UserStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'status']


class UserActionViewSet(viewsets.ModelViewSet):
    serializer_class = UserActionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action', 'class_id']

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserAction.objects.all()
        return UserAction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'permission']

    def perform_create(self, serializer):
        serializer.save(granted_by=self.request.user)


class AuthorPermissionRequestViewSet(viewsets.ModelViewSet):
    queryset = AuthorPermissionRequest.objects.all()
    serializer_class = AuthorPermissionRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def review(self, request, pk=None):
        instance = self.get_object()
        review_status = request.data.get('status')
        if review_status not in [
            AuthorPermissionRequest.STATUS_APPROVED,
            AuthorPermissionRequest.STATUS_REJECTED
        ]:
            return Response({'status': '有効なステータスを指定してください。'}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = review_status
        instance.reviewed_by = request.user
        instance.reviewed_at = timezone.now()
        instance.save()
        return Response(AuthorPermissionRequestSerializer(instance).data)
