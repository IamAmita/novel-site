from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Report, OperationHistory, WorkStat
from .serializers import ReportSerializer, ReportReviewSerializer, OperationHistorySerializer, WorkStatSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'class_id', 'reporter']
    ordering_fields = ['created_at', 'status']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def review(self, request, pk=None):
        report = self.get_object()
        report_status = request.data.get('status')
        if report_status not in [Report.STATUS_RESOLVED, Report.STATUS_DISMISSED]:
            return Response({'status': '有効なステータスを指定してください。'}, status=status.HTTP_400_BAD_REQUEST)
        report.status = report_status
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.save()
        return Response(ReportSerializer(report).data)


class OperationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationHistory.objects.all()
    serializer_class = OperationHistorySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'table', 'operation']
    ordering_fields = ['created_at']


class WorkStatViewSet(viewsets.ModelViewSet):
    queryset = WorkStat.objects.all()
    serializer_class = WorkStatSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['novel']
    ordering_fields = ['view_count', 'good_count', 'rating_count', 'updated_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def increment_view(self, request, pk=None):
        stat = self.get_object()
        stat.view_count += 1
        stat.save(update_fields=['view_count', 'updated_at'])
        return Response({'view_count': stat.view_count})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def recalculate(self, request, pk=None):
        stat = self.get_object()
        from apps.novels.models import Episode
        from apps.communications.models import Comment, Review, Evaluation
        novel = stat.novel
        stat.episode_count = Episode.objects.filter(novel=novel, deleted_at__isnull=True).count()
        # class_id for novels would be defined in masters data; using novel.id as placeholder
        stat.comment_count = Comment.objects.filter(
            class_id=10, target_id=novel.id, is_deleted=False
        ).count()
        stat.good_count = Evaluation.objects.filter(
            class_id=10, target_id=novel.id, eval_type='good'
        ).count()
        reviews = Review.objects.filter(class_id=10, target_id=novel.id)
        stat.rating_count = reviews.count()
        from django.db.models import Sum
        rating_sum = reviews.aggregate(total=Sum('rating'))['total'] or 0
        stat.rating_sum = rating_sum
        stat.save()
        return Response(WorkStatSerializer(stat).data)
