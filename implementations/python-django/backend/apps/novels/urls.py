from rest_framework.routers import DefaultRouter
from .views import NovelViewSet, SectionViewSet, EpisodeViewSet, NovelStatusViewSet, NovelTagViewSet

router = DefaultRouter()
router.register(r'novels', NovelViewSet, basename='novels')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'episodes', EpisodeViewSet, basename='episodes')
router.register(r'novel-statuses', NovelStatusViewSet, basename='novel-statuses')
router.register(r'novel-tags', NovelTagViewSet, basename='novel-tags')

urlpatterns = router.urls
