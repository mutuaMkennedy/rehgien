from django.contrib import admin
from .models import MortgageRates

# Register your models here.
class MortgageRatesAdmin(admin.ModelAdmin):
	display_list = ('Equity_Bank', 'Cooperative_Bank', 'Kcb_Bank')


admin.site.register(MortgageRates, MortgageRatesAdmin)



