from django.db import models
from django.conf import settings


class PartnerProgram(models.Model):
    title = models.CharField(max_length=100)
    short_descritpion = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ImageField(upload_to = 'partner_program_photos', blank = True)

    def __str__(self):
        return self.title

class RehgienPartner(models.Model):
    APPROVAL_CHOICES = (
        ('APPROVED','approved'),
        ('PENDING','pending'),
        ('REJECTED','rejected'),
    )
    partner_program = models.ForeignKey(PartnerProgram, on_delete=models.SET_NULL,\
                            default = None, related_name='partner_program', blank=False, null=True)
    first_name = models.CharField(max_length = 100, blank=False)
    last_name = models.CharField(max_length = 100, blank=False)
    email = models.EmailField(blank=False)
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(max_length=200, blank=True)
    phone_number = models.CharField( max_length=13, blank=False)
    message = models.TextField(null=True)
    approval_status = models.CharField(max_length=15, choices=APPROVAL_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'RehgienPartner'

    def __str__(self):
        return self.partner_program.title + ' ' + self.first_name + ' ' + self.last_name  + ' ' + self.email  + ' ' + self.company_name
