from rest_framework import serializers
from .models import Category, Tag, Template


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'parent', 'name', 'slug', 'sort_order', 'is_official', 'created_at', 'updated_at', 'children']
        read_only_fields = ['created_at', 'updated_at']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class CategoryFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'parent', 'name', 'slug', 'sort_order', 'is_official', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'is_official', 'use_count', 'created_at', 'updated_at']
        read_only_fields = ['use_count', 'created_at', 'updated_at']


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'subject', 'body', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
