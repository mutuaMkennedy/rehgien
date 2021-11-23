from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models


class RehgienProStaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['rehgien_pro:pro_join_landing']

    def location(self, item):
        return reverse(item)
