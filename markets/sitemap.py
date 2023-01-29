from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models

class JobPostSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['markets:job_post_home']

    def location(self, item):
        return reverse(item)
