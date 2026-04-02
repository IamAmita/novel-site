from django.contrib import admin
from .models import Report, OperationHistory, WorkStat


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'class_id', 'target_id', 'reason', 'status', 'reviewed_by', 'created_at']
    list_filter = ['status']
    search_fields = ['reporter__email', 'body']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reporter', 'reason', 'reviewed_by')


@admin.register(OperationHistory)
class OperationHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'table', 'target_id', 'operation', 'ip_address', 'created_at']
    list_filter = ['table', 'operation']
    search_fields = ['user__email', 'ip_address']
    readonly_fields = ['created_at']


@admin.register(WorkStat)
class WorkStatAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'novel', 'view_count', 'episode_count', 'comment_count',
        'good_count', 'bookmark_count', 'rating_count', 'updated_at'
    ]
    readonly_fields = ['updated_at']
    search_fields = ['novel__info__title']
