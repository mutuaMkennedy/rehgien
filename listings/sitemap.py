from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models

class PropertyListingsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.Home.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.publishdate

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['homepage']

    def location(self, item):
        return reverse(item)
