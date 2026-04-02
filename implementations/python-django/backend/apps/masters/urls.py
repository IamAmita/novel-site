from rest_framework.routers import DefaultRouter
from .views import (
    MasterClassViewSet, MasterStatusViewSet, MasterActionViewSet,
    MasterOperationViewSet, MasterPermissionViewSet, MasterReasonViewSet,
    MasterTableViewSet, MasterTwoFactorMethodViewSet
)

router = DefaultRouter()
router.register(r'classes', MasterClassViewSet)
router.register(r'statuses', MasterStatusViewSet)
router.register(r'actions', MasterActionViewSet)
router.register(r'operations', MasterOperationViewSet)
router.register(r'permissions', MasterPermissionViewSet)
router.register(r'reasons', MasterReasonViewSet)
router.register(r'tables', MasterTableViewSet)
router.register(r'two-factor-methods', MasterTwoFactorMethodViewSet)

urlpatterns = router.urls
