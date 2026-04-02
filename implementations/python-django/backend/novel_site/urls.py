from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.masters.urls')),
    path('api/v1/', include('apps.common.urls')),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.novels.urls')),
    path('api/v1/', include('apps.worlds.urls')),
    path('api/v1/', include('apps.communications.urls')),
    path('api/v1/', include('apps.administration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
