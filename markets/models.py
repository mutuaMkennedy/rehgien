from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from django.utils.safestring import mark_safe

# Request are published as leads
class JobPost(models.Model):
    PROJECT_SIZE = (
        ('LARGE',mark_safe(
            u'<span>Large</span> <small>Mostly a longer term activity with a series of complex multiple requirements.' +
            '<br>Example: Designing and building a house. </small>'
            )
        ),
        ('MEDIUM',mark_safe(
            u'<span>Medium</span><small> A moderately complex activity with a well defined time frame.' +
            '<br>Example: Home value assessment. </small>'
            )
        ),
        ('SMALL',mark_safe(
            u'<span>Small</span> <small>A relatively quick activity with less complex steps which can ussually be done in a small time frame.' +
            '<br>Examples: Cleaning service, Moving service etc. </small>'
            )
        ),
    )
    PROJECT_DURATION_CHOICES = (
        ('1', mark_safe(u'<span>less than a week</span>')),
        ('2', mark_safe(u'<span>less than 1 month</span>')),
        ('3', mark_safe(u'<span>1 to 3 months</span>')),
        ('4', mark_safe(u'<span>3 to 6 months</span>')),
        ('5', mark_safe(u'<span>more than 6 months</span>')),
    )

    title = models.CharField(max_length = 100, blank=False )
    description = models.TextField(blank = False)
    project_size = models.CharField(max_length = 20, choices = PROJECT_SIZE , blank = False)
    project_duration =  models.CharField(max_length = 20, choices = PROJECT_DURATION_CHOICES , blank = False)
    skill_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)
    verified = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    location = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)
    job_viewers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='job_viewer', blank=True)
    job_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    job_update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    job_poster = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_poster', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'JobPosts'

    def get_absolute_url(self):
        return reverse( 'rehgien_pro:job_detail', kwargs={'pk':self.pk})

class JobPostProposal(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_post_proposal')
    message = models.TextField()
    proposal_sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_post_responder', on_delete=models.CASCADE, default=None, null=True)
    proposal_send_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'JobPostProposals'
