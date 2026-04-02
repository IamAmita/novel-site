from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Novel, NovelInfo, NovelStatus, NovelTag, Section, SectionStatus, Episode, EpisodeStatus
from .serializers import (
    NovelSerializer, NovelCreateSerializer, NovelStatusSerializer,
    NovelTagSerializer, SectionSerializer, SectionStatusSerializer,
    EpisodeSerializer, EpisodeListSerializer, EpisodeStatusSerializer
)


class NovelViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'category']
    search_fields = ['info__title', 'info__synopsis']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Novel.objects.select_related('user', 'user__profile', 'category', 'info').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NovelCreateSerializer
        return NovelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        novel = self.get_object()
        sections = Section.objects.filter(novel=novel).order_by('sort_order', 'id')
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def episodes(self, request, pk=None):
        novel = self.get_object()
        episodes = Episode.objects.filter(novel=novel).order_by('sort_order', 'episode_number')
        serializer = EpisodeListSerializer(episodes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        novel = self.get_object()
        statuses = NovelStatus.objects.filter(novel=novel).order_by('-created_at')
        serializer = NovelStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_status(self, request, pk=None):
        novel = self.get_object()
        if novel.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        serializer = NovelStatusSerializer(data={'novel': novel.id, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['novel']
    ordering_fields = ['sort_order', 'id']

    def get_queryset(self):
        return Section.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        novel = serializer.validated_data.get('novel')
        if novel.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

    @action(detail=True, methods=['get'])
    def episodes(self, request, pk=None):
        section = self.get_object()
        episodes = Episode.objects.filter(section=section).order_by('sort_order', 'episode_number')
        serializer = EpisodeListSerializer(episodes, many=True)
        return Response(serializer.data)


class EpisodeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['novel', 'section']
    search_fields = ['title']
    ordering_fields = ['sort_order', 'episode_number', 'created_at']

    def get_queryset(self):
        return Episode.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EpisodeListSerializer
        return EpisodeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        novel = serializer.validated_data.get('novel')
        if novel.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.novel.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        episode = self.get_object()
        statuses = EpisodeStatus.objects.filter(episode=episode).order_by('-created_at')
        serializer = EpisodeStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_status(self, request, pk=None):
        episode = self.get_object()
        if episode.novel.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        serializer = EpisodeStatusSerializer(data={'episode': episode.id, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NovelStatusViewSet(viewsets.ModelViewSet):
    queryset = NovelStatus.objects.all()
    serializer_class = NovelStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['novel', 'status']


class NovelTagViewSet(viewsets.ModelViewSet):
    queryset = NovelTag.objects.all()
    serializer_class = NovelTagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['novel', 'tag']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
