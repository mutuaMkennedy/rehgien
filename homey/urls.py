"""homey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from photologue.sitemaps import GallerySitemap, PhotoSitemap
from listings import views
from contact import views as contact_views
from django.views.generic import TemplateView
from allauth.account.views import confirm_email
from rest_auth.views import PasswordResetConfirmView
from django.contrib.sitemaps.views import sitemap
from listings.sitemap import  StaticViewSitemap, PropertyListingsSitemap
from markets.sitemap import JobPostSitemap
from profiles.sitemap import StaticBusinessHomepageSitemap, BusinessProfileSitemap
from resource_center.sitemap import BlogPostSitemap
from rehgien_pro.sitemap import RehgienProStaticViewSitemap
from contact.sitemap import ContactStaticViewSitemap
#from haystack.forms import FacetedSearchForm
#from haystack.views import FacetedSearchView

sitemaps = {
    'property_listings':PropertyListingsSitemap,
    'job_posts':JobPostSitemap,
    'static_business_homepage':StaticBusinessHomepageSitemap,
    'business_profiles':BusinessProfileSitemap,
    'blog_post':BlogPostSitemap,
    'static_content':StaticViewSitemap,
    "RehgienProStaticViewSitemap":RehgienProStaticViewSitemap,
    "ContactStaticViewSitemap":ContactStaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.homepage, name='homepage'),
    path('location/', include('location.urls')),
    path('listings/', include('listings.urls')),
    path('mortgage/', include('mortgage.urls')),
    path('contact/', include('contact.urls')),
    path('profile/', include('profiles.urls')),
    path('markets/', include('markets.urls')),
    path('pro/', include('rehgien_pro.urls')),
    path('resources/', include('resource_center.urls')),
    path('partnerships/', include('partnership.urls')),
    path('ac/', include('app_accounts.urls')),
    path('chat/', include('chat.urls')),
    path('apis/', include('chat.apis.urls')),
    path('apis/', include('listings.apis.urls')),
    path('apis/', include('location.api.urls')),
    path('apis/', include('profiles.apis.urls')),
    path('apis/', include('markets.apis.urls')),
    path('apis/', include('contact.apis.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path("select2/", include("django_select2.urls")),
    url(r'^apis/rest-auth/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email'),
    path('r/site/indexing/sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('terms_of_service/', TemplateView.as_view(template_name = 'terms_of_service.html'), name='terms_of_use'),
    path('privacy_policy/', TemplateView.as_view(template_name = 'privacy_policy.html'), name='privacy_policy'),
    path('contact_us/', contact_views.contact_us, name="contact_us"),
    path('about_us/', contact_views.about_us, name="about_us"),
    # path('msg/', TemplateView.as_view(template_name = 'index.html')),
    #url(r'^search/', include('haystack.urls')),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('apis/api-auth/', include('rest_framework.urls')),
    url(r'^apis/rest-auth/', include('rest_auth.urls')),
    url(r'^apis/rest-auth/', include('rest_auth.urls')),
    url(r'^apis/rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    # re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name = 'index.html')),
]

sitemaps = {
        'photologue_galleries': GallerySitemap,
        'photologue_photos': PhotoSitemap,
}
