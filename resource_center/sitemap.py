from django.contrib.sitemaps import Sitemap
from . import models

class BlogPostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return models.BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.publishdate
