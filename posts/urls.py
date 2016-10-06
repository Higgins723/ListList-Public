from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^create/$', views.post_create, name="create"),
    #Regex Expression for generated URL's based on ID
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name="detail"),
    url(r'^$', views.post_list, name="list"),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name="delete_post"),
]
