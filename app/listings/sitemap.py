from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models

class PropertyListingsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return models.Home.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.publishdate

class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['homepage', 'listings:shop_category']

    def location(self, item):
        return reverse(item)
