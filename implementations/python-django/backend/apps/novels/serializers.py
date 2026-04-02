from rest_framework import serializers
from apps.common.serializers import TagSerializer, CategoryFlatSerializer
from apps.users.serializers import UserPublicSerializer
from .models import Novel, NovelInfo, NovelStatus, NovelTag, Section, SectionStatus, Episode, EpisodeStatus


class NovelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovelInfo
        fields = ['title', 'synopsis', 'cover_image_url', 'is_r18', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class NovelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovelStatus
        fields = ['id', 'novel', 'status', 'note', 'created_at']
        read_only_fields = ['created_at']


class NovelTagSerializer(serializers.ModelSerializer):
    tag_detail = TagSerializer(source='tag', read_only=True)

    class Meta:
        model = NovelTag
        fields = ['id', 'novel', 'tag', 'tag_detail', 'created_at']
        read_only_fields = ['created_at']


class SectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionStatus
        fields = ['id', 'section', 'status', 'created_at']
        read_only_fields = ['created_at']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'novel', 'title', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EpisodeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeStatus
        fields = ['id', 'episode', 'status', 'created_at']
        read_only_fields = ['created_at']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'id', 'novel', 'section', 'episode_number', 'title', 'body',
            'sort_order', 'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['deleted_at', 'created_at', 'updated_at']


class EpisodeListSerializer(serializers.ModelSerializer):
    """エピソード一覧用（本文なし）"""
    class Meta:
        model = Episode
        fields = [
            'id', 'novel', 'section', 'episode_number', 'title',
            'sort_order', 'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['deleted_at', 'created_at', 'updated_at']


class NovelSerializer(serializers.ModelSerializer):
    info = NovelInfoSerializer(read_only=True)
    author = UserPublicSerializer(source='user', read_only=True)
    category_detail = CategoryFlatSerializer(source='category', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    episode_count = serializers.SerializerMethodField()

    class Meta:
        model = Novel
        fields = [
            'id', 'user', 'author', 'category', 'category_detail', 'tags',
            'info', 'episode_count', 'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'deleted_at', 'created_at', 'updated_at']

    def get_episode_count(self, obj):
        return obj.episodes.filter(deleted_at__isnull=True).count()


class NovelCreateSerializer(serializers.ModelSerializer):
    info = NovelInfoSerializer()

    class Meta:
        model = Novel
        fields = ['id', 'category', 'info', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        info_data = validated_data.pop('info')
        novel = Novel.objects.create(**validated_data)
        NovelInfo.objects.create(novel=novel, **info_data)
        return novel

    def update(self, instance, validated_data):
        info_data = validated_data.pop('info', None)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        if info_data:
            NovelInfo.objects.update_or_create(novel=instance, defaults=info_data)
        return instance
