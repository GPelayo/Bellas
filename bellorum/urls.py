from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from bellorum import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('gallery.urls'))
    # TODO Create default page
    #url(r'^$', gallery_urls.views.gallery_index_redirect),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
