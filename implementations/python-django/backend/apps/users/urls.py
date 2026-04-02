from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView,
    UserViewSet, UserProfileViewSet, FollowViewSet, BlockViewSet,
    DirectMessageViewSet, LoginHistoryViewSet, UserStatusViewSet,
    UserActionViewSet, UserPermissionViewSet, AuthorPermissionRequestViewSet
)

router = DefaultRouter()
router.register(r'auth', RegisterView, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'follows', FollowViewSet, basename='follows')
router.register(r'blocks', BlockViewSet, basename='blocks')
router.register(r'messages', DirectMessageViewSet, basename='messages')
router.register(r'login-history', LoginHistoryViewSet, basename='login-history')
router.register(r'statuses', UserStatusViewSet, basename='user-statuses')
router.register(r'actions', UserActionViewSet, basename='user-actions')
router.register(r'permissions', UserPermissionViewSet, basename='user-permissions')
router.register(r'author-requests', AuthorPermissionRequestViewSet, basename='author-requests')

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
