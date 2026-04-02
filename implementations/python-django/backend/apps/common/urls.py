from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, TemplateViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'templates', TemplateViewSet)

urlpatterns = router.urls
