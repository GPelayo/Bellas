from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from bellorum import settings
from gallery.dj_rest_framework.api import v0

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v0/', include(v0.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
