from rest_framework import serializers
from .models import (
    MasterClass, MasterStatus, MasterAction, MasterOperation,
    MasterPermission, MasterReason, MasterTable, MasterTwoFactorMethod
)


class MasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClass
        fields = ['id', 'name', 'description']


class MasterStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterStatus
        fields = ['id', 'name', 'description']


class MasterActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterAction
        fields = ['id', 'name', 'description']


class MasterOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterOperation
        fields = ['id', 'name', 'description']


class MasterPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPermission
        fields = ['id', 'name', 'description']


class MasterReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterReason
        fields = ['id', 'name', 'description']


class MasterTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTable
        fields = ['id', 'name', 'description']


class MasterTwoFactorMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTwoFactorMethod
        fields = ['id', 'name', 'description']
