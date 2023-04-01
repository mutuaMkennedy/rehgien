from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from unittest import mock
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
        client_user = User.objects.create_user(
            username='test_client', 
            password='1X<ISRUkw+tuK', 
            email="testclient@email.com",
            phone="+254123456789",
            user_type="CLIENT")
        professional_user = User.objects.create_user(
            username='test_pro', 
            password='2HJ1vRV0Z&3iD', 
            email="testpro@email.com",
            phone="+254123456788",
            user_type="PRO")

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

    def test_pro_user_can_log_in_via_email(self):
        """ 
            Test that user can log in using their email after submit of correct data
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"testpro@email.com","password":"2HJ1vRV0Z&3iD"})
        
        # Check our user gets redirected to the correct url meaning they have been authenticated
        self.assertRedirects(response, reverse('rehgien_pro:dashboard_home'))

    def test_pro_user_can_log_in_via_phone(self):
        """ 
            Test that user can log in using their phone number after submit of correct data
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"+254123456788","password":"2HJ1vRV0Z&3iD"})
        
        # Check our user gets redirected to the correct url meaning they have been authenticated
        self.assertRedirects(response, reverse('rehgien_pro:dashboard_home'))

    def test_client_user_cannot_login_using_email(self):
        """ 
            Test that client user cannot log in to protected view 
            using their email after even on submit of correct data,
            Only pro users should login from view
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"testclient@email.com","password":"1X<ISRUkw+tuK"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets a permission denied message
        self.assertIn("permission_denied", response.context)

    def test_client_user_cannot_login_using_phone(self):
        """ 
            Test that client user cannot log in to protected view 
            using their phone after even on submit of correct data,
            Only pro users should login from view
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"+254123456789","password":"1X<ISRUkw+tuK"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets a permission denied message
        self.assertIn("permission_denied", response.context)

    def test_user_is_shown_correct_template_when_they_enter_incorrect_login_data(self):
        """ 
            Test that client user cannot log if they enter wrong data and
            they are shown the correct template with message
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"wrong_identity","password":"1X<ISRUkw+tuK"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets a invalid identity message
        self.assertIn("invalid_identity", response.context)

    def test_user_is_shown_never_logged_in_if_email_provided_is_not_associated_with_a_user(self):
        """ 
            Test that client user cannot log if they enter email address
            that is not connected to any account
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"invalidemail@email.com","password":"1X<ISRUkw+tuK"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets an account not found message
        self.assertIn("account_not_found", response.context)

    def test_user_is_shown_never_logged_in_if_phone_provided_is_not_associated_with_a_user(self):
        """ 
            Test that client user cannot log if they enter a phone number
            that is not connected to any account
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"+254123455789","password":"1X<ISRUkw+tuK"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets an account not found message
        self.assertIn("account_not_found", response.context)

    def test_user_is_shown_correct_template_when_they_enter_correct_email_but_incorrect_password(self):
        """ 
            Test that client user cannot log if they enter a correct email address
            but provide wrong password
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"testclient@email.com","password":"wrong_password"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets incorrect password message
        self.assertIn("incorrect_password", response.context)

    def test_user_is_shown_correct_template_when_they_enter_correct_phone_but_incorrect_password(self):
        """ 
            Test that client user cannot log if they enter a correct email address
            but provide wrong password
        """
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:user_login'), {"identity":"+254123456789","password":"wrong_password"})
        
        # Check our user is shown correct template
        self.assertTemplateUsed(response, 'app_accounts/login.html')

        # Check our user gets a incorrect password message
        self.assertIn("incorrect_password", response.context)

class UserSignUpTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create two users
        client_user = User.objects.create_user(
            username='test_client', 
            password='1X<ISRUkw+tuK', 
            email="testclient@email.com",
            phone="+254123456789",
            user_type="CLIENT")
        professional_user = User.objects.create_user(
            username='test_pro', 
            password='2HJ1vRV0Z&3iD', 
            email="testpro@email.com",
            phone="+254123456788",
            user_type="PRO")

        client_user.save()
        professional_user.save()  

        # Create the required business profile for professional user to avoid any errors
        business_profile = models.BusinessProfile.objects.create(user=professional_user)

    def test_view_url_is_accessible(self):
        """ Test view url is accessible and returns a status code 200 """

        # Get the url
        url = reverse('app_accounts:user_signup')

        # Issue a get request
        response = self.client.get(url)

        # Test reachability
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_users_are_served_the_correct_template(self):
        #  Issue GET request
        response = self.client.get(reverse('app_accounts:user_signup'))

        # Check that correct template is used
        self.assertTemplateUsed(response, 'app_accounts/sign_up.html')

    def test_authenticated_client_user_is_redirected_to_the_correct_url(self):
        #  Login user
        self.client.login(username="test_client", password="1X<ISRUkw+tuK")
        
        #  Issue GET request
        response = self.client.get(reverse('app_accounts:user_signup'))

        # Check our user gets redirected to the correct url
        self.assertRedirects(response, reverse('homepage'))

    def test_authenticated_pro_user_is_redirected_to_the_correct_url(self):
        #  Login user
        self.client.login(username="test_pro", password="2HJ1vRV0Z&3iD")
        
        #  Issue GET request
        response = self.client.get(reverse('app_accounts:user_signup'))

        # Check our user gets redirected to the correct url
        self.assertRedirects(response, reverse('rehgien_pro:dashboard_home'))

class ValidatePhoneSendOtpTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create user
        User.objects.create_user(
            username='test_client', 
            password='1X<ISRUkw+tuK', 
            email="testclient@email.com",
            phone="+254123456789",
            user_type="CLIENT")

    def test_view_url_is_accessible(self):
        """ Test view url is accessible and returns a status code 200 """

        # Get the url
        url = reverse('app_accounts:validate_phone')

        # Issue a get request
        response = self.client.get(url)

        # Test reachability
        self.assertEqual(response.status_code, 200)

    def test_correct_response_when_phone_field_empty(self):  
        #  Issue POST request
        response = self.client.post(reverse('app_accounts:validate_phone'), {"phone":""})

        # Check correct json response is returned
        self.assertJSONEqual(force_text(response.content), {'status':False, 'detail':'Please enter a phone number!'})
    
    @mock.patch('app_accounts.views.utils.validate_phone_send_otp')
    def test_correct_response_returned_when_process_is_successful(self, mock_validate_phone_send_otp):
        # Configure the mock validate_phone_send_otp function to return a successful response
        mock_validate_phone_send_otp.return_value = {'status': True}

        # Issue POST request with a phone number that is not associated with an account
        response = self.client.post(reverse('app_accounts:validate_phone'), {"phone":"+254123476789"})

        # Check true value exist in the json response. Meaning validation request was successful
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], True)

        # Check that the validate_phone_send_otp function was called with the correct arguments
        mock_validate_phone_send_otp.assert_called_once_with('+254123476789')

    def test_correct_response_returned_when_process_is_unsuccessful(self):
        #  Issue POST request with to generate an unsuccessful validation i.e issue a phone number associated with an account
        response = self.client.post(reverse('app_accounts:validate_phone'), {"phone":"+254123456789"})

        # Check false value exist in the json response. Meaning validation request was unsuccessful
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], False)  # or False

"""
The corresponding view is incomplete and functionality is likely to fail.
These tests will be ignored until setup wizard is complete
"""
"""
class UserAccountSetupWizardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
         # Create user
        User.objects.create_user(
            username='test_client', 
            password='1X<ISRUkw+tuK', 
            email="testclient@email.com",
            phone="+254123456789",
            user_type="CLIENT")        

    def test_user_account_setup_wizard_view(self):
        # Issue a get request to the wizard view
        url = reverse('app_accounts:UserAccountSetupWizard')
        response = self.client.get(url)

        # Test reachability and form template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/phone_number.html")
        
        # Issue a post request to the wizard view with invalid phone number
        data = {'0-phone': 'invalid'}
        response = self.client.post(url, data)

        # Test that the form displays errors and stays on the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/phone_number.html")
        self.assertFormError(response, 'form0', 'phone', 'Enter a valid phone number.')
        
        # Issue a post request to the wizard view with valid phone number
        data = {'0-phone': '+254712345678'}
        response = self.client.post(url, data)

        # Test that the phone verification code template is used in the next step
        self.assertEqual(response.status_code, 302)  # 302 indicates redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/phone_verification.html")
        
        # Issue a post request to the wizard view with invalid verification code
        data = {'1-verification_code': 'invalid'}
        response = self.client.post(url, data)

        # Test that the form displays errors and stays on the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/phone_verification.html")
        self.assertFormError(response, 'form1', 'verification_code', 'Enter a valid verification code.')
        
        # Issue a post request to the wizard view with valid verification code
        verification_code = '123456'
        data = {'1-verification_code': verification_code}
        response = self.client.post(url, data)

        # Test that the password template is used in the next step
        self.assertEqual(response.status_code, 302)  # 302 indicates redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/password.html")
        
        # Issue a post request to the wizard view with invalid password
        data = {'2-password': 'short'}
        response = self.client.post(url, data)

        # Test that the form displays errors and stays on the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_accounts/sign_up/password.html")
        self.assertFormError(response, 'form2', 'password', 'Ensure this value has at least 8 characters (it has 5).')
        
        # Issue a post request to the wizard view with valid password
        password = 'mypassword123'
        data = {'2-password': password}
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, "app_accounts/sign_up/password.html")

         # Test that the user has been created successfully
        self.assertEqual(response.status_code, 302)  # 302 indicates redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'test_client')
        self.assertEqual(user.email, 'testclient@email.com')
        self.assertEqual(user.phone, '+254712345678')
        self.assertEqual(user.user_type, 'CLIENT')
        self.assertTemplateUsed(response, "app_accounts/sign_up/done.html")

"""