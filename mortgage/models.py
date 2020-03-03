from django.db import models

# Create your models here.

class MortgageRates(models.Model):
	Equity_Bank = models.DecimalField(decimal_places=2, max_digits=2)
	Cooperative_Bank = models.DecimalField(decimal_places=2, max_digits=2)
	Kcb_Bank = models.DecimalField(decimal_places=2, max_digits=2)

	class Meta:
		verbose_name_plural = 'MortgageRates'



