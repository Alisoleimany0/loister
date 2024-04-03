from django.contrib import sitemaps
from django.urls import reverse

from shop.models import Product


class ProductsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Product.objects.all()


class ShopSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'browse']

    def location(self, item):
        return reverse(item)
