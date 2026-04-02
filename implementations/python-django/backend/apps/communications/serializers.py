from rest_framework import serializers
from apps.users.serializers import UserPublicSerializer
from .models import Board, Comment, Review, Evaluation, Notification, NotificationStatus


class BoardSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'author', 'title', 'class_id', 'target_id', 'is_closed', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'author', 'class_id', 'target_id', 'parent',
            'body', 'is_deleted', 'created_at', 'updated_at', 'replies'
        ]
        read_only_fields = ['user', 'is_deleted', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.filter(is_deleted=False).exists():
            return CommentSerializer(obj.replies.filter(is_deleted=False), many=True).data
        return []


class CommentListSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'author', 'class_id', 'target_id', 'parent',
            'body', 'is_deleted', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'is_deleted', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'author', 'class_id', 'target_id',
            'title', 'body', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('評価は1から5の間で指定してください。')
        return value


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'user', 'class_id', 'target_id', 'eval_type', 'created_at']
        read_only_fields = ['user', 'created_at']


class NotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationStatus
        fields = ['is_read', 'read_at', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    notification_status = NotificationStatusSerializer(source='status', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'class_id', 'target_id', 'message', 'created_at', 'notification_status']
        read_only_fields = ['user', 'created_at']
