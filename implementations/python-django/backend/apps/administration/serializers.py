from rest_framework import serializers
from apps.users.serializers import UserPublicSerializer
from .models import Report, OperationHistory, WorkStat


class ReportSerializer(serializers.ModelSerializer):
    reporter_info = UserPublicSerializer(source='reporter', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_info', 'class_id', 'target_id',
            'reason', 'body', 'status', 'reviewed_by', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['reporter', 'status', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at']


class ReportReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['status', 'reviewed_by', 'reviewed_at']


class OperationHistorySerializer(serializers.ModelSerializer):
    user_info = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = OperationHistory
        fields = [
            'id', 'user', 'user_info', 'table', 'target_id', 'operation',
            'before_data', 'after_data', 'ip_address', 'created_at'
        ]
        read_only_fields = ['created_at']


class WorkStatSerializer(serializers.ModelSerializer):
    rating_avg = serializers.FloatField(read_only=True)

    class Meta:
        model = WorkStat
        fields = [
            'id', 'novel', 'view_count', 'episode_count', 'comment_count',
            'good_count', 'bookmark_count', 'rating_sum', 'rating_count',
            'rating_avg', 'updated_at'
        ]
        read_only_fields = ['updated_at']
