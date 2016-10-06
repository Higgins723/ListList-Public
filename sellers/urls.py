from django.conf.urls import include, url
from django.contrib import admin

from .views import (
        SellerDashboard,
        SellerProductDetailRedirectView,
        )

from products.views import (
    ProductCreateView,
    SellerProductListView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^products/add/$', ProductCreateView.as_view(), name='product_create'),
    url(r'^products/$', SellerProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='product_edit'),
    url(r'^products/(?P<slug>[-\w]+)/delete/$', ProductDeleteView.as_view(), name="product_delete"),
    url(r'^products/(?P<slug>[\w-]+)/$', SellerProductDetailRedirectView.as_view()),
]