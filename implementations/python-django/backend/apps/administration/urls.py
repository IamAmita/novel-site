from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, OperationHistoryViewSet, WorkStatViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'operation-history', OperationHistoryViewSet, basename='operation-history')
router.register(r'work-stats', WorkStatViewSet, basename='work-stats')

urlpatterns = router.urls
