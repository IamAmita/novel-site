from rest_framework import viewsets, permissions
from .models import (
    MasterClass, MasterStatus, MasterAction, MasterOperation,
    MasterPermission, MasterReason, MasterTable, MasterTwoFactorMethod
)
from .serializers import (
    MasterClassSerializer, MasterStatusSerializer, MasterActionSerializer,
    MasterOperationSerializer, MasterPermissionSerializer, MasterReasonSerializer,
    MasterTableSerializer, MasterTwoFactorMethodSerializer
)


class MasterClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassSerializer
    permission_classes = [permissions.AllowAny]


class MasterStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterStatus.objects.all()
    serializer_class = MasterStatusSerializer
    permission_classes = [permissions.AllowAny]


class MasterActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterAction.objects.all()
    serializer_class = MasterActionSerializer
    permission_classes = [permissions.AllowAny]


class MasterOperationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterOperation.objects.all()
    serializer_class = MasterOperationSerializer
    permission_classes = [permissions.IsAdminUser]


class MasterPermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterPermission.objects.all()
    serializer_class = MasterPermissionSerializer
    permission_classes = [permissions.AllowAny]


class MasterReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterReason.objects.all()
    serializer_class = MasterReasonSerializer
    permission_classes = [permissions.AllowAny]


class MasterTableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterTable.objects.all()
    serializer_class = MasterTableSerializer
    permission_classes = [permissions.IsAdminUser]


class MasterTwoFactorMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterTwoFactorMethod.objects.all()
    serializer_class = MasterTwoFactorMethodSerializer
    permission_classes = [permissions.AllowAny]
