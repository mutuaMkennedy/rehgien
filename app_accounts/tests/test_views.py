from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .. import views 
from profiles import models

# referencing the custom user model
User = get_user_model()

class UserLoginViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Run once to set up non-modified data for all class methods."""
        pass

    def setUp(self):
        """ Setup the any data we are going to need on every test we run """

        # Get a client for use in tests """
        self.client = Client()

        # Create two users
        client_user = User.objects.create_user(username='test_client', password='1X<ISRUkw+tuK', user_type="CLIENT")
        professional_user = User.objects.create_user(username='test_pro', password='2HJ1vRV0Z&3iD', user_type="PRO")

        client_user.save()
        professional_user.save()  

        # Create the required business profile for professional user to avoid any errors
        business_profile = models.BusinessProfile.objects.create(user=professional_user)

    def test_view_url_is_accessible(self):
        """ Test view url is accessible and returns a status code 200 """

        # Get the url
        url = reverse('app_accounts:user_login')

        # Issue a get request
        response = self.client.get(url)

        # Test reachability
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_resolves_correct_view(self):
        """ Test view url resolves to the correct view"""

        # Get the url
        url = reverse('app_accounts:user_login')
        
        # Check it resolves
        self.assertEqual(resolve(url).func, views.user_login)

    def test_view_uses_correct_template_for_users_not_logged_in(self):
        """ Test that users not logged in are shown the correct template """

        # Issue GET request
        response = self.client.get(reverse('app_accounts:user_login'))

        # Check correct template is used
        self.assertTemplateUsed(response, 'app_accounts/login.html')

    def test_client_user_redirect_if_logged_in(self):
        """ 
            Test that user of type client is redirected to correct url if they try
            to access this view while logged in
        """
       
        #  Login user
        login = self.client.login(username="test_client", password="1X<ISRUkw+tuK")
        
        #  Issue GET request
        response = self.client.get(reverse('app_accounts:user_login'))

        # Check our user gets redirected to the correct url
        self.assertRedirects(response, reverse('homepage'))

    def test_pro_user_redirect_if_logged_in(self):
        """ 
            Test that user of type professional is redirected to correct url if they try
            to access this view while logged in
        """

        #  Login user
        login = self.client.login(username="test_pro", password="2HJ1vRV0Z&3iD")

        #  Issue GET request
        response = self.client.get(reverse('app_accounts:user_login'))
        
        # Check our user gets redirected to the correct url
        self.assertRedirects(response, reverse('rehgien_pro:dashboard_home'))