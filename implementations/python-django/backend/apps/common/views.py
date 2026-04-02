from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Template
from .serializers import CategorySerializer, CategoryFlatSerializer, TagSerializer, TemplateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_official', 'parent']
    search_fields = ['name', 'slug']
    ordering_fields = ['sort_order', 'id', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryFlatSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Category.objects.all()
        if self.request.query_params.get('root_only'):
            queryset = queryset.filter(parent__isnull=True)
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_official']
    search_fields = ['name']
    ordering_fields = ['name', 'use_count', 'created_at']
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAdminUser]
