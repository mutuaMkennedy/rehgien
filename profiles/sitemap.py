from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models

class StaticBusinessHomepageSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['profiles:business_homepage']

    def location(self, item):
        return reverse(item)

class BusinessProfileSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return models.BusinessProfile.objects.all()
