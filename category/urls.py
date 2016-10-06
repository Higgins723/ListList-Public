from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name='category_home'),
    url(r'^(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
]