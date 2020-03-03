from django.shortcuts import render
from .models import MortgageRates
from . import forms
# Create your views here.


def mortgagehomepage(request):
	return render(request, 'mortgage/mortgage.html')

def mortgage_calculator(request):
	# calculating required monthly payment : P = L[C(1+c)^n] / [(1+c)^n-1)] where: L=amount, n= months, c= interest rate
	loanrate = MortgageRates.objects.all()
	if request.method == 'POST':
		form = forms.mortgageform(request.POST, request.FILES)
		if form.is_valid():
			loan = form.cleaned_data['loan']
			term = form.cleaned_data['term']
			rate = 12
			calc = loan * rate * (1 + rate)**term / (1+rate)**term - 1
			payment = calc
			return render(request, 'mortgage/mortgage.html', {'payment': payment})
	else:
		form = forms.mortgageform()
	return render(request, 'mortgage/mortgage.html', {'form': form})








	

