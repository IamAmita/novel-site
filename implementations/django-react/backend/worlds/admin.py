from django.contrib import admin

from .models import World


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ("name", "owner_pen_name", "updated_at", "deleted_at")
    search_fields = ("name",)
