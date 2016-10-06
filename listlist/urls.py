"""listlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.conf import settings

#import my app views
from products import urls as products_urls
from category import urls as urls_categories
# from tags import urls as tags_urls
from dashboard.views import DashboardView, LegalView
from sellers import urls as sellers_urls
from contact.views import ContactCreateView

from posts import urls as post_urls


urlpatterns = [
    #handle dashboard views
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    #handle django registration redux
    url(r'^accounts/', include('registration.backends.default.urls')),
    #handle admin sites
    url(r'^admin/', include(admin.site.urls)),
    #handle products app
    url(r'^classifieds/', include(products_urls, namespace='products')),
    #handle sellers app
    url(r'^seller/', include(sellers_urls, namespace='sellers')),
    #handle categories
    url(r'^categories/', include(urls_categories, namespace='categories')),
    #blog app
    url(r'^posts/', include(post_urls, namespace="posts")),
    #contact app
    url(r'^contact/$', ContactCreateView.as_view(), name="contact"),
    #dashboard legal view
    url(r'^legal/$', LegalView.as_view(), name='legal'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
