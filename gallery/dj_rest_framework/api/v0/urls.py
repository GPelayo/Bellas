from django.conf.urls import url

from gallery.dj_rest_framework import views

urlpatterns = [
    url(r'index$', views.IndexView.as_view(), name='index'),
    url(r'galleries/([0-9]+)', views.PageView.as_view(), name='galleries')
]