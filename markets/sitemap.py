from django.contrib.sitemaps import Sitemap
from . import models

class JobPostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.JobPost.objects.all()

    def lastmod(self, obj):
        return obj.job_update_date
