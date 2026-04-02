from django.contrib import admin
from .models import Category, Tag, Template


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'parent', 'sort_order', 'is_official']
    list_filter = ['is_official']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_official', 'use_count']
    list_filter = ['is_official']
    search_fields = ['name']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'created_at']
    search_fields = ['name', 'subject']
