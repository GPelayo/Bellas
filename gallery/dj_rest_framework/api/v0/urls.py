from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'gallery/index$', views.IndexView.as_view()),
    url(r'gallery/id/([0-9]+)', views.PageView.as_view())
]