from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models as profiles_models
from listings import models as listings_models
from listings.apis import serializers as listings_serializers
from location.api import serializers as location_serializers
from django.db.models import Avg
from rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from django.db import IntegrityError
from . import views
# referencing the custom user model
User = get_user_model()

#serializing usermodel + their Listings

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(min_length=None,allow_blank=True, required=False)
    phone = serializers.CharField(max_length=30,allow_blank=True,required=False)
    first_name = serializers.CharField(max_length=65,allow_blank=True,required=False)
    last_name = serializers.CharField(max_length=65,allow_blank=True,required=False)

    def validate_phone(self,phone):
        usr = User.objects.filter(phone=phone)
        if usr.exists():
            raise serializers.ValidationError(
                    ("A user is already registered with this phone number."))
        else:
            return phone

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        """
            Checking if there is data in the fields before trying to save to avoid Integrity errors
            caused by empty fields
        """
        if self.data.get('email'):
            user.email = self.data.get('email')
        if self.data.get('phone'):
            user.phone = self.data.get('phone')
        if self.data.get('first_name'):
            user.first_name = self.data.get('first_name')
        if self.data.get('last_name'):
            user.last_name = self.data.get('last_name')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','user_type',
        'profile_image'
        ]

class ProfessionalGroupSerializer(serializers.ModelSerializer):
    total_services = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.ProfessionalGroup
        fields = ['pk',"group_image","slug","interests","total_services"]

    def get_total_services(self,obj):
        categories = profiles_models.ProfessionalCategory.objects.filter(professional_group = obj.pk)
        return categories.count()

class ProfessionalCategorySerializer(serializers.ModelSerializer):
    professional_group = ProfessionalGroupSerializer(many=False, read_only=True)
    professional_services = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.ProfessionalCategory
        fields = ['pk', "category_name","category_image","slug","professional_group",
                    "professional_services"]

    def get_professional_services(self,obj):
        services = []
        for svc in obj.pro_category.all():
            item = {
                "pk":svc.pk,
                "professional_category":svc.professional_category.pk,
                "service_name":svc.service_name,
                # "service_image",
                "slug":svc.slug,
            }

            services.append(item)
        return services

class ProfessionalServiceSerializer(serializers.ModelSerializer):
    professional_category = ProfessionalCategorySerializer()
    class Meta:
        model = profiles_models.ProfessionalService
        fields = ['pk',"professional_category","service_name","service_image","slug"]

class ServiceSearchHistorySerializer(serializers.ModelSerializer):
    professional_service = ProfessionalServiceSerializer()
    project_location = location_serializers.KenyaTownSerializer()
    class Meta:
        model = profiles_models.ServiceSearchHistory
        fields = [
        'pk','user', 'professional_service','project_location', 'search_count', 'search_date'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_user_object = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.Review
        fields = [
        'pk',"recommendation_rating_choices","responsive_rating_choices","knowledge_rating_choices","professionalism_rating_choices",
        "quality_rating_choices","profile","recommendation_rating","responsive_rating","knowledge_rating","professionalism_rating",
        "quality_of_service_rating","comment","likes","reviewer","review_date","reviewer_user_object"
        ]

    def get_reviewer_user_object(self,obj):
        user_object = {
            'id':obj.reviewer.pk,
            'username':obj.reviewer.username,
            'first_name':obj.reviewer.first_name,
            'last_name':obj.reviewer.last_name,
            'email':obj.reviewer.email,
            'user_type':obj.reviewer.user_type,
            'profile_image':obj.reviewer.profile_image.url if obj.reviewer.profile_image else '',
            }
        return user_object

class LikeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Review
        fields = ["likes"]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Client
        fields =[
        "pk", "business_profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.BusinessHours
        fields =[
        "WEEKDAYS","pk","business_profile","weekday","from_hour","to_hour",
        ]

class QuestionOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.QuestionOptions
        fields = [
            "pk","question","name",
        ]

class QuestionSerializer(serializers.ModelSerializer):
    question_option = QuestionOptionsSerializer(many=True)
    class Meta:
        model = profiles_models.Question
        fields = [
            "pk","matchMaker","step","title","slug","client_question","pro_question","question_type","question_option"
        ]

class MatchMakerSerializer(serializers.ModelSerializer):
    professional_service = ProfessionalServiceSerializer()
    matchmaker_question = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.MatchMaker
        fields = [
            "pk","professional_service","description","matchmaker_question"
        ]

    def get_matchmaker_question(self, object):
        questions = object.matchmaker_question.order_by('step')
        return QuestionSerializer(questions,many=True).data

class ProAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    answer = QuestionOptionsSerializer(many=True)
    service_delivery_areas = location_serializers.KenyaTownSerializer(many=True)
    professional_service = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.ProAnswer
        fields = [
            "pk","business_profile","professional_service", "question","service_delivery_areas", 
            "answer", "timestamp"
        ]

    def get_professional_service(self,obj):
        return obj.question.matchMaker.professional_service.pk

class BusinessProfileSerializer(WritableNestedModelSerializer):
    professional_category = ProfessionalCategorySerializer(many=False)
    professional_services = ProfessionalServiceSerializer(many=True)
    pro_business_client = ClientSerializer(many=True)
    pro_business_hours = BusinessHoursSerializer(many=True)
    pro_business_review = ReviewSerializer(many=True)
    match_answer = ProAnswerSerializer(many=True)
    service_areas = location_serializers.KenyaTownSerializer(many=True)
    pro_portfolio_items = serializers.SerializerMethodField()
    pro_followers = serializers.SerializerMethodField()
    pro_saves = serializers.SerializerMethodField()
    rating_stats = serializers.SerializerMethodField()
    _business_profile_percentage_complete_ = serializers.SerializerMethodField()
    business_account_setup_milestones = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.BusinessProfile
        fields = [
        "pk","user","professional_category","professional_services","match_answer","business_profile_image",
        "business_name","phone","business_email","address","location","website_link",
        "facebook_page_link","twitter_page_link","linkedin_page_link","instagram_page_link",
        "about_video","about","service_areas","saves","followers","member_since",
        "featured","verified","pro_business_client","pro_business_hours","pro_business_review",
        "pro_portfolio_items","pro_followers","pro_saves",
        "rating_stats","_business_profile_percentage_complete_","business_account_setup_milestones"
        ]

    def get_business_account_setup_milestones(self,obj):
        percent_complete = {
        "setup_business_account": 10,
        "add_services_you_offer": 20,
        "upload_work_projects": 20,
        "upload_profile_photo": 20,
        "add_business_description": 10,
        "get_external_reviews": 20,
        }
        total = 0
        milestones = [
            {
                "status":False,
                "name":"Setup your business account",
                "order":0,
                "slug":"setup-business-account",
                "details":"As a service provider, your business page is what helps us connect you with the right customers for your business."
            },
            {
                "name":"Add services you offer",
                "order":1,
                "status":False,
                "slug":"add-services-you-offer",
                "details":"It is critical to include the services you provide in order for customers to find you. You should also establish targeting preferences for each service you provide. These preferences are what we use to match you with customers who are a good fit."        
            },
            {
                "name":"Upload 3 work projects",
                "order":2,
                "status":False,
                "slug":"upload-work-projects",
                "details":"Showcase your previous work to boost the credibility of your profile. Adding projects allows you to demonstrate to potential clients what it's like to work with you."
            },
            {
                "name":"Upload your profile photo",
                "order":3,
                "status":False,
                "slug":"upload-profile-photo",
                "details":"Adding a profile picture to your company's website helps to personalize it. Profile photos can be anything you want: mugshots, logos, etc., but they must accurately represent your company and brand. Uploading blurry photos is not recommended."
            },
            {
                "name":"Add your business description",
                "order":4,
                "status":False,
                "slug":"add-business-description",
                "details":"Reviews are key to getting you hired. Getting reviews from past clients helps future clients decide whether to hire you. You can ask for reviews via email or share a link to customers outside of Rehgien."
            },
            {
                "name":"Get 3 external reviews",
                "order":5,
                "status":False,
                "slug":"get-external-reviews",
                "details":"Reviews are key to getting you hired. Getting reviews from past clients helps future clients decide whether to hire you. You can ask for reviews via email or share a link to customers outside of Rehgien."
            },
        ]

        if obj:
            milestones[0]["status"] = True
            total += percent_complete.get("setup_business_account", 0)
        if obj.professional_services:
            milestones[1]["status"] = True
            total += percent_complete.get("add_services_you_offer", 0)
        if obj.user.profiles_portfolioitem_createdby_related.all().count() >= 3:
            milestones[2]["status"] = True
            total += percent_complete.get("upload_work_projects", 0)
        if obj.business_profile_image:
            milestones[3]["status"] = True
            total += percent_complete.get("upload_profile_photo", 0)
        if obj.about:
            milestones[4]["status"] = True
            total += percent_complete.get("add_business_description", 0)
        if obj.pro_business_review.all().count() >= 3:
            milestones[5]["status"] = True
            total += percent_complete.get("get_external_reviews", 0)

        context = {
            "percent_complete":total,
            "milestones":milestones
        }
        return context
 
    def get_pro_portfolio_items(self,obj):
        portfolio_object = profiles_models.PortfolioItem.objects.filter(created_by=obj.user.pk)
        portfolio_item_array = []
        if portfolio_object.exists():
            for ptf in portfolio_object:
                ptf_object_photos = []

                # looping over all the photos related to this portfolio object
                for pic in ptf.portfolio_item_photo.all():
                    photo_object = {
                        'pk':pic.pk,
                        'portfolio_item':pic.portfolio_item.pk,
                        'photo':pic.photo.url if pic.photo else '',
                    }
                    ptf_object_photos.append(photo_object)

                # creating the user object arrray
                user_object = {
                    'id':ptf.created_by.pk,
                    'username':ptf.created_by.username,
                    'first_name':ptf.created_by.first_name,
                    'last_name':ptf.created_by.last_name,
                    'email':ptf.created_by.email,
                    'user_type':ptf.created_by.user_type,
                    'profile_image':ptf.created_by.profile_image.url if ptf.created_by.profile_image else '',
                    }

                # and finally creating the portfolio object arrray
                portfolio_object = {
                    'pk':ptf.pk,
                    'name': ptf.name,
                    'description': ptf.description,
                    "project_job_type":ptf.project_job_type.service_name if ptf.project_job_type else "",
                    "project_job_type_object":{
                        "pk":ptf.project_job_type.pk if ptf.project_job_type else "",
                        "service_name":ptf.project_job_type.service_name if ptf.project_job_type else "",
                        "slug":ptf.project_job_type.slug if ptf.project_job_type else "",
                    },
                    "project_location":ptf.project_location.town_name if ptf.project_location else "",
                    "project_location_object":{
                        "id":ptf.project_location.pk if ptf.project_job_type else "",
                        "town_name":ptf.project_location.town_name if ptf.project_location else ""
                    },
                    "project_cost":ptf.project_cost,
                    "project_duration":ptf.project_duration,
                    "project_year":ptf.project_year,
                    'video': ptf.video,
                    'photos':ptf_object_photos,
                    'created_at': ptf.created_at,
                    'created_by': user_object,
                 }

                portfolio_item_array.append(portfolio_object)

        return portfolio_item_array

    def get_rating_stats(self,obj):
        pro_reviews = obj.pro_business_review.all()

        rvw_count = pro_reviews.count()
        if rvw_count == 0:
            rvw_count = 1

        recommendation_rating_avg = pro_reviews.aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
        responsive_rating_avg = pro_reviews.aggregate(Avg('responsive_rating')).get('responsive_rating__avg', 0.00)
        knowledge_rating_avg = pro_reviews.aggregate(Avg('knowledge_rating')).get('knowledge_rating__avg', 0.00)
        professionalism_rating_avg = pro_reviews.aggregate(Avg('professionalism_rating')).get('professionalism_rating__avg', 0.00)
        quality_of_service_rating_avg = pro_reviews.aggregate(Avg('quality_of_service_rating')).get('quality_of_service_rating__avg', 0.00)

        five_star_ratings = pro_reviews.filter(recommendation_rating=5).count()
        four_star_ratings = pro_reviews.filter(recommendation_rating=4).count()
        three_star_ratings = pro_reviews.filter(recommendation_rating=3).count()
        two_star_ratings = pro_reviews.filter(recommendation_rating=2).count()
        one_star_ratings = pro_reviews.filter(recommendation_rating=1).count()

        array = {
            "five_stars": five_star_ratings/ rvw_count * 100,
            "four_stars": four_star_ratings / rvw_count * 100,
            "three_stars": three_star_ratings / rvw_count * 100,
            "two_stars": two_star_ratings / rvw_count * 100,
            "one_stars": one_star_ratings / rvw_count * 100,
            }

        highly_rated_traits = []
        if responsive_rating_avg and responsive_rating_avg >= 4.5:
            highly_rated_traits.append('Responsiveness')
        if knowledge_rating_avg and knowledge_rating_avg >= 4.5:
            highly_rated_traits.append('Knowledge')
        if professionalism_rating_avg and professionalism_rating_avg >= 4.5:
            highly_rated_traits.append('Professionalism')
        if quality_of_service_rating_avg and quality_of_service_rating_avg >= 4.5:
            highly_rated_traits.append('Qaulity of service')

        comment = ''

        if recommendation_rating_avg:
            if recommendation_rating_avg >= 4.5:
                comment = 'Very Highly rated'
            elif recommendation_rating_avg >= 3.5 and recommendation_rating_avg < 4.5:
                comment = 'Highly rated'
            elif recommendation_rating_avg >= 2.5 and recommendation_rating_avg < 3.5:
                comment = 'Rated Average'
            elif recommendation_rating_avg > 0 and recommendation_rating_avg < 1.5:
                comment = 'Rated Low'
            else:
                comment = 'Not Rated'
        else:
            comment = 'Not Rated'

        array = {
            "overall_rating": recommendation_rating_avg if recommendation_rating_avg else 0,
            "recommendation_rating_avg":recommendation_rating_avg if recommendation_rating_avg else 0,
            "responsive_rating_avg":responsive_rating_avg if recommendation_rating_avg else 0,
            "knowledge_rating_avg":knowledge_rating_avg if recommendation_rating_avg else 0,
            "professionalism_rating_avg":professionalism_rating_avg if recommendation_rating_avg else 0,
            "quality_of_service_rating_avg":quality_of_service_rating_avg if recommendation_rating_avg else 0,
            "highly_rated_traits":highly_rated_traits,
            "comment": comment,
            "stars_percentage_avg": array
        }

        return array

    def get__business_profile_percentage_complete_(self,obj):
        percent = {
        'business_profile_image': 10, 'professional_category':10, 'phone':5, 'business_email':10,
        'address':10, 'website_link':5, 'facebook_page_link': 5,
        'twitter_page_link': 5, 'linkedin_page_link':5, 'instagram_page_link':5,
        'location':10, 'about':20
        }
        total = 0
        if obj.business_profile_image:
            total += percent.get('business_profile_image', 0)
        if obj.professional_category:
            total += percent.get('professional_category', 0)
        if obj.phone:
            total += percent.get('phone', 0)
        if obj.address:
            total += percent.get('address', 0)
        if obj.business_email:
            total += percent.get('business_email', 0)
        if obj.website_link:
            total += percent.get('website_link', 0)
        if obj.facebook_page_link:
            total += percent.get('facebook_page_link', 0)
        if obj.twitter_page_link:
            total += percent.get('twitter_page_link', 0)
        if obj.linkedin_page_link:
            total += percent.get('linkedin_page_link', 0)
        if obj.instagram_page_link:
            total += percent.get('instagram_page_link', 0)
        if obj.location:
            total += percent.get('location', 0)
        if obj.about:
            total += percent.get('about', 0)
        return "%s"%(total)

    def get_pro_saves(self,obj):
        saves_array = []
        for save in obj.saves.all():
            saves_object = {
                'id':save.pk,
                'username':save.username,
                'first_name':save.first_name,
                'last_name':save.last_name,
                'email':save.email,
                'user_type':save.user_type,
                'profile_image':save.profile_image.url if save.profile_image else '',
            }
            saves_array.append(saves_object)
        return saves_array

    def get_pro_followers(self,obj):
        followers_array = []
        for follower in obj.followers.all():
            business_page_array = []
            if follower.user_type == 'PRO':
                user_followers = []
                business_page = {
                    "pk":follower.pro_business_profile.pk,
                    "user":follower.pro_business_profile.user.username,
                    "professional_category":follower.pro_business_profile.professional_category.category_name,
                    "business_profile_image":follower.pro_business_profile.business_profile_image.url if follower.pro_business_profile.business_profile_image else '',
                    "business_name":follower.pro_business_profile.business_name,
                    "phone":follower.pro_business_profile.phone,
                    "business_email":follower.pro_business_profile.business_email,
                    'followers':user_followers
                }

                for f in follower.pro_business_profile.followers.all():
                    follower_user_obj = {
                    'id':f.pk,
                    'username':f.username,
                    'first_name':f.first_name,
                    'last_name':f.last_name,
                    'email':f.email,
                    'user_type':f.user_type,
                    'profile_image':f.profile_image.url if f.profile_image else '',
                    }

                    user_followers.append(follower_user_obj)

                business_page_array.append(business_page)

            follower_object = {
                'id':follower.pk,
                'username':follower.username,
                'first_name':follower.first_name,
                'last_name':follower.last_name,
                'email':follower.email,
                'user_type':follower.user_type,
                'profile_image':follower.profile_image.url if follower.profile_image else '',
                'business_page':business_page_array
            }
            followers_array.append(follower_object)
        return followers_array


class SocialBusinessProfileSerializer(WritableNestedModelSerializer):
    class Meta:
        model = profiles_models.BusinessProfile
        fields = ["saves","followers"]

class PortfolioItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PortfolioItemPhoto
        fields = ['pk','portfolio_item','photo']

class PortfolioItemSerializer(WritableNestedModelSerializer):
    portfolio_item_photo= PortfolioItemPhotoSerializer(many=True)
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "pk","name","description","project_job_type","project_location",
        "project_cost","project_duration","project_year","video",
        "portfolio_item_photo","created_at","created_by"
        ]

class PortfolioItemSerializer2(WritableNestedModelSerializer):
    # project_job_type = ProfessionalServiceSerializer()
    # project_location = location_serializers.KenyaTownSerializer()
    project_job_type_obj = serializers.SerializerMethodField()
    project_location_obj = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "pk","name","description","project_job_type","project_location",
        "project_job_type_obj","project_location_obj",
        "project_cost","project_duration","project_year","video",
        "created_at","created_by",
        ]
    
    def get_project_job_type_obj(self,obj):
        job_type = obj.project_job_type
        return ProfessionalServiceSerializer(job_type).data

    def get_project_location_obj(self,obj):
        service = obj.project_location
        return location_serializers.KenyaTownSerializer(service).data

class TeammateConnectionSerializer(serializers.ModelSerializer):
    requestor_user_object = serializers.SerializerMethodField()
    receiver_user_object = serializers.SerializerMethodField()
    requestor_business_profile = serializers.SerializerMethodField()
    receiver_business_profile = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.TeammateConnection
        fields = [
        'pk',"requestor", "receiver", "accepted_choices","receiver_accepted", "starred",
        "created_at", "requestor_user_object","receiver_user_object",
        "requestor_business_profile", "receiver_business_profile"
        ]

    def get_requestor_user_object(self,obj):
        user_object = {
            'id':obj.requestor.pk,
            'username':obj.requestor.username,
            'first_name':obj.requestor.first_name,
            'last_name':obj.requestor.last_name,
            'email':obj.requestor.email,
            'user_type':obj.requestor.user_type,
            'profile_image':obj.requestor.profile_image.url if obj.requestor.profile_image else '',
            }
        return user_object

    def get_receiver_user_object(self,obj):
        user_object = {
            'id':obj.receiver.pk,
            'username':obj.receiver.username,
            'first_name':obj.receiver.first_name,
            'last_name':obj.receiver.last_name,
            'email':obj.receiver.email,
            'user_type':obj.receiver.user_type,
            'profile_image':obj.receiver.profile_image.url if obj.receiver.profile_image else '',
            }
        return user_object

    def get_requestor_business_profile(self, obj):
        if obj.requestor.user_type == 'PRO':
            profile = {
            "pk": obj.requestor.pro_business_profile.pk,
            "user": obj.requestor.pro_business_profile.user.username,
            "professional_category": obj.requestor.pro_business_profile.professional_category.category_name,
            "business_name": obj.requestor.pro_business_profile.business_name,
            "business_profile_image": obj.requestor.pro_business_profile.business_profile_image.url if obj.requestor.pro_business_profile.business_profile_image else ''
            }
            return profile
        else:
            return ''

    def get_receiver_business_profile(self, obj):
        if obj.receiver.user_type == 'PRO':
            profile = {
            "pk": obj.receiver.pro_business_profile.pk,
            "user": obj.receiver.pro_business_profile.user.username,
            "professional_category": obj.receiver.pro_business_profile.professional_category.category_name,
            "business_name": obj.receiver.pro_business_profile.business_name,
            "business_profile_image": obj.receiver.pro_business_profile.business_profile_image.url if obj.receiver.pro_business_profile.business_profile_image else ''
            }
            return profile
        else:
            return ''

class UserAccountSerializer(WritableNestedModelSerializer):
    pro_business_profile = BusinessProfileSerializer(many=False)
    profiles_portfolioitem_createdby_related = PortfolioItemSerializer(many=True)
    connection_requestor = TeammateConnectionSerializer(many=True)
    connection_request_receiver = TeammateConnectionSerializer(many=True)
    user_service_search_history = serializers.SerializerMethodField()
    listings_home_owner_related = listings_serializers.HomeSerializer(many=True)
    _user_account_percentage_complete_ = serializers.SerializerMethodField()
    business_pages_following = serializers.SerializerMethodField()
    business_pages_saved = serializers.SerializerMethodField()
    has_interest_group = serializers.SerializerMethodField()
    groups_interested_in = serializers.SerializerMethodField()
    recommended_services = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.User
        fields = [
        'user_type_choices','account_type_choices','pk', 'username', 'first_name',
        'last_name', 'email', 'user_type','account_type', 'profile_image', 'business_pages_following', 'business_pages_saved',
        "pro_business_profile", "profiles_portfolioitem_createdby_related", "connection_requestor",
        "connection_request_receiver", "listings_home_owner_related",'_user_account_percentage_complete_', 'has_interest_group',
        "groups_interested_in", 'user_service_search_history','recommended_services'
        ]

    def get_has_interest_group(self, obj):
        groups = obj.group_interests.all()
        status = False
        if groups:
            status = True
        return status

    def get__user_account_percentage_complete_(self,obj):
        percent = { 'username': 10, 'first_name': 15, 'last_name': 15, 'email': 20,
        'profile_image': 30, 'user_type':5,'account_type':5}
        total = 0
        if obj.username:
            total += percent.get('username', 0)
        if obj.first_name:
            total += percent.get('first_name', 0)
        if obj.last_name:
            total += percent.get('last_name', 0)
        if obj.email:
            total += percent.get('email', 0)
        if obj.profile_image:
            total += percent.get('profile_image', 0)
        return "%s"%(total)

    def get_business_pages_following(self, object):
        business_pages_following = object.business_page_followers.all()
        return BusinessProfileSerializer(business_pages_following, many=True).data

    def get_business_pages_saved(self, object):
        business_pages_saved = object.business_page_saves.all()
        return BusinessProfileSerializer(business_pages_saved, many=True).data

    def get_user_service_search_history(self, object):
        searches = object.user_service_search_history.order_by('-search_date')
        return ServiceSearchHistorySerializer(searches,many=True).data

    def get_recommended_services(self,object):
        rec_services = []
        interest_group = object.group_interests.all()
        if interest_group:
            for grp in interest_group:
                searches = profiles_models.ServiceSearchHistory.objects.all()
                services = profiles_models.ProfessionalService.objects.filter(professional_category__professional_group__pk=grp.pk)
                popular_services = views.get_popular_searches(services,searches)

                pop_services_array = []
                for svc in popular_services:
                    arr = {
                        "pk":svc['professional_service']['pk'],
                        "service_name":svc['professional_service']['service_name'],
                        "service_image":svc['professional_service']['service_image'],
                        "slug":svc['professional_service']['slug'],
                    }
                    pop_services_array.append(arr)

                category_array = []
                for catg in grp.pro_category_group.all():
                    arr = {
                    "category_name":catg.category_name,
                    "category_image":catg.category_image.url if catg.category_image else '',
                    "slug":catg.slug,
                    }
                    category_array.append(arr)

                array = {
                "group_name":grp.group_name,
                "group_image":grp.group_image.url if grp.group_image else '',
                "slug":grp.slug,
                "professional_categories":category_array,
                "professional_services":pop_services_array
                }
                rec_services.append(array)

            return rec_services
        else:
            return rec_services

    def get_groups_interested_in(self, object):
        group_objects = object.group_interests.all()
        groups = []
        for grp in group_objects:
            array={
                "pk":grp.pk,
                "group_name":grp.group_name,
                "group_image":grp.group_image.url if grp.group_image.url else '',
                "slug":grp.slug,
            }
            groups.append(array)
        return groups
        # return ProfessionalGroupSerializer(group_objects, many=True).data

class PhoneOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PhoneOTP
        fields = '__all__'
