from django import forms



class mortgageform(forms.Form):
	Home_price = forms.FloatField(required=True)
	Down_payment = forms.FloatField(required=True)
	Loan_program = forms.IntegerField(required=True, label='Enter loan term in months')
	Interest_rate = forms.DecimalField(required=False, label='Rates provided by this bank', disabled=True)
