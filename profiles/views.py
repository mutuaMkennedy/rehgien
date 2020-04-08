from django.shortcuts import render, get_object_or_404
from listings.models import PropertyForSale
from listings.models import RentalProperty
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile
from . import forms

# Create your views here.

def profile(request):
	user = request.user
	profile_list = UserProfile.objects.all().filter(user=request.user)
	for_sale_user_posts = PropertyForSale.objects.all().filter(owner=request.user)
	rental_user_posts = RentalProperty.objects.all().filter(owner=request.user)
	#SALES PAGINATION
	paginator_sales = Paginator(for_sale_user_posts, 6) #show the first 3
	listing_page = request.GET.get('page')
	user_sale_posts = paginator_sales.get_page(listing_page)
	#RENTALS PAGINATION
	paginator_rentals = Paginator(rental_user_posts, 6) #show the first 3
	_listing_page = request.GET.get('page')
	user_rental_posts = paginator_rentals.get_page(_listing_page)
	return render(request, 'profiles/user_profile.html', {'user': user, 'user_sale_posts':user_sale_posts, 'user_rental_posts':user_rental_posts, 'profile_list':profile_list})

def edit_profile(request, pk):
	profile = get_object_or_404(UserProfile, pk=pk)
	if request.method == 'POST':
			p_edit_form = forms.ProfileEditForm(request.POST, request.FILES, instance=profile)
			if p_edit_form.is_valid():
				instance = p_edit_form.save(commit=False)
				instance.user = request.user
				instance.save()

				messages.success(request, 'Profile Updated Successfully!')
				return redirect('profiles:account')
			else:
				messages.error(request,'Could not complete request!')
	else:
		p_edit_form = forms.ProfileEditForm(instance=profile)
	return render(request, 'profiles/edit_profile.html', {'p_edit_form':p_edit_form})
