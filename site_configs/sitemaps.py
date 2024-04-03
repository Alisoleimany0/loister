from django.contrib import sitemaps
from django.urls import reverse

from shop.models import Product


class SiteSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['about', 'contact']

    def location(self, item):
        return reverse(item)
