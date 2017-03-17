from django.conf.urls import url
from gallery import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^grid/([A-Za-z0-9]+)/$', views.grid, name='grid'),
    url(r'^$', views.gallery_index_redirect)
]
