from django.contrib.sitemaps import Sitemap
from . import models

class BusinessProfileSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.BusinessProfile.objects.filter(verified=True)
    #
    # def lastmod(self, obj):
    #     return obj.member_since
