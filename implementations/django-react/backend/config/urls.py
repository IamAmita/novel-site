from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import (
    CsrfView,
    LoginView,
    LogoutView,
    MeView,
    PenNameViewSet,
    RegisterView,
)
from worlds.views import WorldViewSet

router = DefaultRouter()
router.register("pennames", PenNameViewSet, basename="penname")
router.register("worlds", WorldViewSet, basename="world")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/csrf/", CsrfView.as_view()),
    path("api/auth/register/", RegisterView.as_view()),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    path("api/auth/me/", MeView.as_view()),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
