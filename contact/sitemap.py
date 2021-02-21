from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models


class ContactStaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['contact:about_us']

    def location(self, item):
        return reverse(item)
