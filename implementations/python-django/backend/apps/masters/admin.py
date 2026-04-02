from django.contrib import admin
from .models import (
    MasterClass, MasterStatus, MasterAction, MasterOperation,
    MasterPermission, MasterReason, MasterTable, MasterTwoFactorMethod
)


@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterStatus)
class MasterStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterAction)
class MasterActionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterOperation)
class MasterOperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterPermission)
class MasterPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterReason)
class MasterReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterTable)
class MasterTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(MasterTwoFactorMethod)
class MasterTwoFactorMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
