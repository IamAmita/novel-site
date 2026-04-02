from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Board, Comment, Review, Evaluation, Notification, NotificationStatus
from .serializers import (
    BoardSerializer, CommentSerializer, CommentListSerializer,
    ReviewSerializer, EvaluationSerializer,
    NotificationSerializer, NotificationStatusSerializer
)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['class_id', 'target_id', 'is_closed', 'user']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def close(self, request, pk=None):
        board = self.get_object()
        if board.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        board.is_closed = True
        board.save()
        return Response({'detail': 'ボードをクローズしました。'})


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['class_id', 'target_id', 'parent', 'user']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Comment.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def delete_comment(self, request, pk=None):
        comment = self.get_object()
        if comment.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        comment.is_deleted = True
        comment.body = '削除されたコメントです。'
        comment.save()
        return Response({'detail': 'コメントを削除しました。'})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['class_id', 'target_id', 'user']
    ordering_fields = ['rating', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.delete()


class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_id', 'target_id', 'eval_type']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Evaluation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.delete()


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['class_id']
    ordering_fields = ['created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all().select_related('status')
        return Notification.objects.filter(user=self.request.user).select_related('status')

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            self.permission_denied(self.request)
        notification = serializer.save(user=serializer.validated_data.get('user', self.request.user))
        NotificationStatus.objects.create(notification=notification)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if notification.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        notif_status, _ = NotificationStatus.objects.get_or_create(notification=notification)
        if not notif_status.is_read:
            notif_status.is_read = True
            notif_status.read_at = timezone.now()
            notif_status.save()
        return Response({'detail': '既読にしました。'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        notifications = Notification.objects.filter(user=request.user)
        NotificationStatus.objects.filter(
            notification__in=notifications, is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'detail': '全て既読にしました。'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = NotificationStatus.objects.filter(
            notification__user=request.user, is_read=False
        ).count()
        return Response({'count': count})
