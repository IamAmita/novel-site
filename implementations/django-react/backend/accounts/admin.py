from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import PenName, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("user_id", "email", "username", "is_active", "deleted_at")
    search_fields = ("user_id", "email", "username")
    ordering = ("user_id",)
    fieldsets = (
        (None, {"fields": ("user_id", "email", "username", "password")}),
        ("プロフィール", {"fields": ("icon", "bio")}),
        ("権限", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("状態", {"fields": ("deleted_at", "last_login")}),
    )
    add_fieldsets = (
        (None, {"fields": ("user_id", "email", "username", "password1", "password2")}),
    )


@admin.register(PenName)
class PenNameAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "deleted_at")
    search_fields = ("display_name", "user__user_id")
