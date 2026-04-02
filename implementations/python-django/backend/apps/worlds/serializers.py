from rest_framework import serializers
from apps.users.serializers import UserPublicSerializer
from apps.common.serializers import CategoryFlatSerializer, TagSerializer
from .models import (
    World, WorldInfo, WorldStatus, WorldCategory, WorldTag,
    Setting, SettingField, SettingRelation
)


class WorldInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldInfo
        fields = ['title', 'description', 'cover_image_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class WorldStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldStatus
        fields = ['id', 'world', 'status', 'created_at']
        read_only_fields = ['created_at']


class WorldCategorySerializer(serializers.ModelSerializer):
    category_detail = CategoryFlatSerializer(source='category', read_only=True)

    class Meta:
        model = WorldCategory
        fields = ['id', 'world', 'category', 'category_detail', 'created_at']
        read_only_fields = ['created_at']


class WorldTagSerializer(serializers.ModelSerializer):
    tag_detail = TagSerializer(source='tag', read_only=True)

    class Meta:
        model = WorldTag
        fields = ['id', 'world', 'tag', 'tag_detail', 'created_at']
        read_only_fields = ['created_at']


class SettingFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingField
        fields = ['id', 'setting', 'label', 'value', 'data', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SettingRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingRelation
        fields = ['id', 'from_setting', 'to_setting', 'relation_label', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SettingSerializer(serializers.ModelSerializer):
    fields_data = SettingFieldSerializer(source='fields', many=True, read_only=True)
    relations_from = SettingRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Setting
        fields = [
            'id', 'world', 'parent', 'name', 'class_id', 'sort_order',
            'is_public', 'deleted_at', 'created_at', 'updated_at',
            'fields_data', 'relations_from'
        ]
        read_only_fields = ['deleted_at', 'created_at', 'updated_at']


class SettingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = [
            'id', 'world', 'parent', 'name', 'class_id', 'sort_order',
            'is_public', 'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['deleted_at', 'created_at', 'updated_at']


class WorldSerializer(serializers.ModelSerializer):
    info = WorldInfoSerializer(read_only=True)
    author = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = World
        fields = [
            'id', 'user', 'author', 'novel', 'info',
            'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'deleted_at', 'created_at', 'updated_at']


class WorldCreateSerializer(serializers.ModelSerializer):
    info = WorldInfoSerializer()

    class Meta:
        model = World
        fields = ['id', 'novel', 'info', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        info_data = validated_data.pop('info')
        world = World.objects.create(**validated_data)
        WorldInfo.objects.create(world=world, **info_data)
        return world

    def update(self, instance, validated_data):
        info_data = validated_data.pop('info', None)
        instance.novel = validated_data.get('novel', instance.novel)
        instance.save()
        if info_data:
            WorldInfo.objects.update_or_create(world=instance, defaults=info_data)
        return instance
