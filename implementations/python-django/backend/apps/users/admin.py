from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, UserProfile, UserStatus, UserAction, UserPermission,
    Follow, Block, DirectMessage, LoginHistory, TwoFactorAuth,
    TwoFactorAuthCode, AuthorPermissionRequest
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'username', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['email', 'username']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('個人情報', {'fields': ('username', 'first_name', 'last_name')}),
        ('権限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要な日時', {'fields': ('last_login', 'email_verified_at', 'deleted_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'display_name']
    search_fields = ['display_name', 'user__email']


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    list_filter = ['status']


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'class_id', 'target_id', 'created_at']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'permission', 'granted_by', 'granted_at']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'followee', 'created_at']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'blocker', 'blocked', 'created_at']


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'is_read', 'created_at']
    list_filter = ['is_read']


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ip_address', 'created_at']


@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'method', 'is_enabled']


@admin.register(AuthorPermissionRequest)
class AuthorPermissionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'reviewed_by', 'created_at']
    list_filter = ['status']
