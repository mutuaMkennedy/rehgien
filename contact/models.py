from django.db import models
from django.conf import settings
# Create your models here.

class PageReport(models.Model):
    problem_choices = (
    ('1', 'Offensive Content'),
    ('2', 'Irrelevant Content'),
    ('3', 'Spam'),
    ('4', 'False content'),
    ('5', 'Other')
    )

    problem = models.CharField(choices = problem_choices, max_length = 1, blank = False, null = True)
    email = models.EmailField(blank = False)
    details = models.TextField()
    subject_user_id = models.PositiveIntegerField(blank=False, null = True)
    resolved = models.BooleanField(default = False)

    def __str__(self):
        return self.get_problem_display() + " - " + str(self.subject_user_id) + " resolved: " + str(self.resolved)

    class Meta:
        verbose_name_plural = "PageReports"

class ProjectsPortfolioReport(models.Model):
    problem_choices = (
    ('1', 'Offensive Content'),
    ('2', 'Irrelevant Content'),
    ('3', 'Inaccurate information'),
    ('4', 'Other')
    )

    problem = models.CharField(choices = problem_choices, max_length = 1, blank = False, null = True)
    email = models.EmailField(blank = False)
    details = models.TextField()
    subject_user_id = models.PositiveIntegerField(blank=False, null = True)
    subject_item_id = models.PositiveIntegerField(blank=False, null = True)
    resolved = models.BooleanField(default = False)

    def __str__(self):
        return self.get_problem_display() + " - " + str(self.subject_user_id) + " resolved: " + str(self.resolved)

    class Meta:
        verbose_name_plural = "ProjectsPortfolioReports"

class ReviewReport(models.Model):
    problem_choices = (
    ('1', 'Offensive Language'),
    ('2', 'Appears Fake'),
    ('3', 'Inaccurate review'),
    ('4', 'Other')
    )

    problem = models.CharField(choices = problem_choices, max_length = 1, blank = False, null = True)
    email = models.EmailField(blank = False)
    details = models.TextField()
    subject_user_id = models.PositiveIntegerField(blank=False, null = True)
    subject_item_id = models.PositiveIntegerField(blank=False, null = True)
    resolved = models.BooleanField(default = False)

    def __str__(self):
        return self.get_problem_display() + " - " + str(self.subject_user_id) + " resolved: " + str(self.resolved)

    class Meta:
        verbose_name_plural = "ReviewReports"
