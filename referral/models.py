from tabnanny import verbose
from django.db import models
from django.conf import settings

class ReferralSystem(models.Model):
    tier_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    reward_price = models.PositiveIntegerField(default=0)
    second_reward_price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tier_name + ' - ' + self.description

    class Meta:
        verbose_name_plural =  "Referral System"

class Recruiter(models.Model):
    referral_system = models.ForeignKey(ReferralSystem, related_name='recruiter_referral_system', on_delete=models.SET_NULL, default=None, null=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recruiter', on_delete=models.CASCADE, default=None, null=True)
    referral_code = models.CharField(max_length=250, default=None, null=True)
    referrals = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True,\
				related_name='recruiter_referral')

    def __str__(self):
        return self.recruiter.username + " - " + self.referral_code

    class Meta:
        verbose_name_plural = "Recruiters"

class ReferralPayouts(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='recruiter_payout', null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.recruiter.recruiter.username + " - " + self.recruiter.referral_code

    class Meta:
        verbose_name_plural = "Referral Payouts"