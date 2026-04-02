from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, CommentViewSet, ReviewViewSet, EvaluationViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='boards')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'evaluations', EvaluationViewSet, basename='evaluations')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = router.urls
