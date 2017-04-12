from django.conf.urls import url
from gallery import views

urlpatterns = [
    url(r'^gallery/$', views.gallery_data),
    url(r'^gallery/all$', views.gallery_list)
]