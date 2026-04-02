from django.contrib import admin
from .models import Novel, NovelInfo, NovelStatus, NovelTag, Section, SectionStatus, Episode, EpisodeStatus


class NovelInfoInline(admin.StackedInline):
    model = NovelInfo
    extra = 1


class NovelStatusInline(admin.TabularInline):
    model = NovelStatus
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'created_at', 'deleted_at']
    list_filter = ['category', 'deleted_at']
    search_fields = ['info__title', 'user__email']
    inlines = [NovelInfoInline, NovelStatusInline]


@admin.register(NovelInfo)
class NovelInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'novel', 'title', 'is_r18', 'created_at']
    list_filter = ['is_r18']
    search_fields = ['title']


@admin.register(NovelStatus)
class NovelStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'novel', 'status', 'created_at']
    list_filter = ['status']


class EpisodeStatusInline(admin.TabularInline):
    model = EpisodeStatus
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'novel', 'title', 'sort_order', 'created_at']
    search_fields = ['title']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'novel', 'episode_number', 'title', 'sort_order', 'created_at', 'deleted_at']
    list_filter = ['deleted_at']
    search_fields = ['title', 'novel__info__title']
    inlines = [EpisodeStatusInline]
