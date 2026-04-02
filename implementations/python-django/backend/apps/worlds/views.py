from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    World, WorldInfo, WorldStatus, WorldCategory, WorldTag,
    Setting, SettingField, SettingRelation
)
from .serializers import (
    WorldSerializer, WorldCreateSerializer, WorldStatusSerializer,
    WorldCategorySerializer, WorldTagSerializer,
    SettingSerializer, SettingListSerializer, SettingFieldSerializer,
    SettingRelationSerializer
)


class WorldViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'novel']
    search_fields = ['info__title', 'info__description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return World.objects.select_related('user', 'user__profile', 'novel', 'info').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WorldCreateSerializer
        return WorldSerializer

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
    def settings(self, request, pk=None):
        world = self.get_object()
        settings_qs = Setting.objects.filter(world=world, deleted_at__isnull=True)
        serializer = SettingListSerializer(settings_qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        world = self.get_object()
        statuses = WorldStatus.objects.filter(world=world).order_by('-created_at')
        serializer = WorldStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_status(self, request, pk=None):
        world = self.get_object()
        if world.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        serializer = WorldStatusSerializer(data={'world': world.id, **request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def categories(self, request, pk=None):
        world = self.get_object()
        if world.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST':
            serializer = WorldCategorySerializer(data={'world': world.id, **request.data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # DELETE
        category_id = request.data.get('category')
        WorldCategory.objects.filter(world=world, category_id=category_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def tags(self, request, pk=None):
        world = self.get_object()
        if world.user != request.user and not request.user.is_staff:
            return Response({'detail': '権限がありません。'}, status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST':
            serializer = WorldTagSerializer(data={'world': world.id, **request.data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # DELETE
        tag_id = request.data.get('tag')
        WorldTag.objects.filter(world=world, tag_id=tag_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SettingViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['world', 'parent', 'class_id', 'is_public']
    search_fields = ['name']
    ordering_fields = ['sort_order', 'id']

    def get_queryset(self):
        return Setting.objects.filter(deleted_at__isnull=True).select_related('world', 'class_id')

    def get_serializer_class(self):
        if self.action == 'list':
            return SettingListSerializer
        return SettingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        world = serializer.validated_data.get('world')
        if world.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.world.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['get'])
    def fields(self, request, pk=None):
        setting = self.get_object()
        fields_qs = SettingField.objects.filter(setting=setting)
        serializer = SettingFieldSerializer(fields_qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def relations(self, request, pk=None):
        setting = self.get_object()
        relations = SettingRelation.objects.filter(from_setting=setting)
        serializer = SettingRelationSerializer(relations, many=True)
        return Response(serializer.data)


class SettingFieldViewSet(viewsets.ModelViewSet):
    queryset = SettingField.objects.all()
    serializer_class = SettingFieldSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['setting']
    ordering_fields = ['sort_order', 'id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        setting = serializer.validated_data.get('setting')
        if setting.world.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()


class SettingRelationViewSet(viewsets.ModelViewSet):
    queryset = SettingRelation.objects.all()
    serializer_class = SettingRelationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['from_setting', 'to_setting']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        from_setting = serializer.validated_data.get('from_setting')
        if from_setting.world.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()


class WorldStatusViewSet(viewsets.ModelViewSet):
    queryset = WorldStatus.objects.all()
    serializer_class = WorldStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['world', 'status']
