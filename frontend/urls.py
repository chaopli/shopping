from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^page=(?P<page>\d*)(?:&*price=(?P<price>(.*)))(?:&search=(?P<search>(.*)))', views.get_objects),
    url(r'^search=(?P<search>(.*))', views.get_objects)
]
