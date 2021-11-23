from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models


class ContactStaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['contact:contact_us']

    def location(self, item):
        return reverse(item)

class AboutUsStaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['about_us']

    def location(self, item):
        return reverse(item)
