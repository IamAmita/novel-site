from django.contrib import admin
from .models import (
    World, WorldInfo, WorldStatus, WorldCategory, WorldTag,
    Setting, SettingField, SettingRelation
)


class WorldInfoInline(admin.StackedInline):
    model = WorldInfo
    extra = 1


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'novel', 'created_at', 'deleted_at']
    list_filter = ['deleted_at']
    search_fields = ['info__title', 'user__email']
    inlines = [WorldInfoInline]


@admin.register(WorldInfo)
class WorldInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'world', 'title', 'created_at']
    search_fields = ['title']


@admin.register(WorldStatus)
class WorldStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'world', 'status', 'created_at']


class SettingFieldInline(admin.TabularInline):
    model = SettingField
    extra = 0


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'world', 'name', 'class_id', 'is_public', 'sort_order']
    list_filter = ['is_public', 'class_id']
    search_fields = ['name']
    inlines = [SettingFieldInline]


@admin.register(SettingField)
class SettingFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'setting', 'label', 'sort_order']


@admin.register(SettingRelation)
class SettingRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_setting', 'to_setting', 'relation_label']
