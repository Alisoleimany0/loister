"""
URL configuration for loister project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from shop.sitemaps import ProductsSitemap, ShopSitemap
from site_configs.sitemaps import SiteSitemap
from . import settings

import re
from urllib.parse import urlsplit
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve

# def static(prefix, view=serve, **kwargs):
#     if not prefix:
#         raise ImproperlyConfigured("Empty static prefix not permitted")
#     # elif not settings.DEBUG or urlsplit(prefix).netloc:
#     elif urlsplit(prefix).netloc:
#         # No-op if not in debug mode or a non-local prefix.
#         return []
#     return [
#         re_path(
#             r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")), view, kwargs=kwargs
#         ),
#     ]

sitemaps = {
    'shop': ShopSitemap,
    'site': SiteSitemap,
    'products': ProductsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('customer', include('customer.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('info/', include('site_configs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
handler404 = 'loister.views.http404'

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
