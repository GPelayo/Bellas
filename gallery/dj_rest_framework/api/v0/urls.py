from django.conf.urls import url

from gallery.dj_rest_framework import views

urlpatterns = [
    url(r'gallery/index$', views.IndexView.as_view()),
    url(r'gallery/id/([0-9]+)', views.PageView.as_view())
]