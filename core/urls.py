from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('custom_login.urls', 'auth'), namespace='auth')),
    path('', include(('website.urls','website'),namespace='website')),
    path('event/', include(('mass.urls','mass'),namespace='mass')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)