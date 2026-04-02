from rest_framework.routers import DefaultRouter
from .views import (
    WorldViewSet, SettingViewSet, SettingFieldViewSet,
    SettingRelationViewSet, WorldStatusViewSet
)

router = DefaultRouter()
router.register(r'worlds', WorldViewSet, basename='worlds')
router.register(r'settings', SettingViewSet, basename='settings')
router.register(r'setting-fields', SettingFieldViewSet, basename='setting-fields')
router.register(r'setting-relations', SettingRelationViewSet, basename='setting-relations')
router.register(r'world-statuses', WorldStatusViewSet, basename='world-statuses')

urlpatterns = router.urls
