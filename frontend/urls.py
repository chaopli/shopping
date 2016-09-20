from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^page=(?P<page>\d*)&brand=(?P<brand>(.*))', views.get_objects),
]
