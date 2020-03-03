from django.shortcuts import render
from .documents import HomesForSaleDocument, HomesForRentDocument
# Create your views here.

def onsale_search(request):
	q = request.GET.get('q')
	# price = request.GET.get("price-input")
	# type = request.GET.get("type-input")
	# beds = request.GET.get("beds-input")
	# baths = request.GET.get("baths-input")
	if q:
		homes_for_sale = HomesForSaleDocument.search().query("match", location_name=q)
	else:
		homes_for_sale = ''
	# if price !="" and price is not None:
	# 	homes_for_sale = homes_for_sale.filter(price__icontains=price)
	return render(request, 'search/for_sale_results.html', {'homes_for_sale':homes_for_sale})

def rentals_search(request):
	q = request.GET.get('q')
	if q:
		homes_for_rent = HomesForRentDocument.search().query("match", location_name=q)
	else:
		homes_for_rent = ''
	return render(request, 'search/for_rent_results.html', {'homes_for_rent':homes_for_rent})
