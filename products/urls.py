from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import (
        ProductCreateView,
        ProductDetailView,
        ProductListView,
        ProductUpdateView,
        VendorListView,
    )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^vendor/$', RedirectView.as_view(pattern_name='products:list'), name='vendor_list'),
    url(r'^vendor/(?P<vendor_name>[\w.@+-]+)/$', VendorListView.as_view(), name='vendor_detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),
]