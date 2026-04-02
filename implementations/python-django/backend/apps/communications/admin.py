from django.contrib import admin
from .models import Board, Comment, Review, Evaluation, Notification, NotificationStatus


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'class_id', 'target_id', 'is_closed', 'created_at']
    list_filter = ['is_closed']
    search_fields = ['title', 'user__email']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'class_id', 'target_id', 'parent', 'is_deleted', 'created_at']
    list_filter = ['is_deleted']
    search_fields = ['body', 'user__email']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'class_id', 'target_id', 'title', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['title', 'user__email']


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'class_id', 'target_id', 'eval_type', 'created_at']
    list_filter = ['eval_type']


class NotificationStatusInline(admin.StackedInline):
    model = NotificationStatus
    extra = 0


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'class_id', 'target_id', 'created_at']
    search_fields = ['message', 'user__email']
    inlines = [NotificationStatusInline]


@admin.register(NotificationStatus)
class NotificationStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'notification', 'is_read', 'read_at']
    list_filter = ['is_read']
