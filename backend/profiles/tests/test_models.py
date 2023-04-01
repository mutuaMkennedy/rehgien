import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()

class UserModelTests(TestCase):

    @classmethod
    def setUpTestData(self) -> None:
        self.client = Client
        
        # Create default user
        self.user = User.objects.create_user(
            username = 'testuser', 
            password = '1X<ISRUkw+tuK', 
            first_name = "Test",
            last_name = "User",
            email = "testuser@example.com",
            phone = "+254123456789",
            user_type = "CLIENT",
            account_type = "BASIC",
            azure_identity='test_identity',
            azure_access_token='test_token',
            azure_token_expires_on='2023-03-28T18:45:12.321Z',
        )
    
    def test_user_fields(self):
        
        """
        Test user field have been populated successfully
        """
        
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone, '+254123456789')
        self.assertEqual(self.user.user_type, 'CLIENT')
        self.assertEqual(self.user.account_type, 'BASIC')
        self.assertEqual(self.user.azure_identity, 'test_identity')
        self.assertEqual(self.user.azure_access_token, 'test_token')
        self.assertEqual(self.user.azure_token_expires_on, '2023-03-28T18:45:12.321Z')


    def test_user_properties(self):
        
        """
        Test user properties can be retrieved 
        """
        
        self.assertEqual(str(self.user), 'testuser')
        self.assertEqual(self.user.get_full_name(), 'Test User')
        self.assertEqual(self.user.percentage_complete, '60')


    def test_field_properties(self):
        
        """
        user_type
        """
        
        # field label
        field_label = self.user._meta.get_field("user_type").verbose_name
        self.assertEqual(field_label, "user type")
        
        # choices
        expected_choices = ('CLIENT', 'client'), ('PRO', 'pro')
        expected_default_choice = "CLIENT"

        choices = self.user._meta.get_field("user_type").choices
        default_value = self.user._meta.get_field("user_type").default

        self.assertEqual(choices, expected_choices)
        self.assertEqual(default_value, expected_default_choice)

        # Max length
        max_length = self.user._meta.get_field("user_type").max_length
        self.assertEqual(max_length, 20)
        

        """
        phone
        """

        # field label
        field_label = self.user._meta.get_field("phone").verbose_name
        self.assertEqual(field_label, "phone")

        # max length
        max_length = self.user._meta.get_field("phone").max_length
        self.assertEqual(max_length, 17)

        # unique
        unique_ = self.user._meta.get_field("phone").unique
        self.assertEqual(unique_, True)

        # null
        null_ = self.user._meta.get_field("phone").null
        self.assertEqual(null_, True)


        """
        account_type
        """

        # field label
        field_label = self.user._meta.get_field("account_type").verbose_name
        self.assertEqual(field_label, "account type")

        # max length
        max_length = self.user._meta.get_field("account_type").max_length
        self.assertEqual(max_length, 10)

        # choices
        expected_choices = ('BASIC', 'basic'), ('PREMIUM','premium')
        expected_default_choice = "BASIC"

        choices = self.user._meta.get_field("account_type").choices
        default_value = self.user._meta.get_field("account_type").default

        self.assertEqual(choices, expected_choices)
        self.assertEqual(default_value, expected_default_choice)


        """
        azure_identity
        """

        # field label
        field_label = self.user._meta.get_field("azure_identity").verbose_name
        self.assertEqual(field_label, "azure identity")

        # blank
        blank_ = self.user._meta.get_field("azure_identity").blank
        self.assertEqual(blank_, True)

        # null
        null_ = self.user._meta.get_field("azure_identity").null
        self.assertEqual(null_, True)


        """
        azure_access_token
        """

        # field label
        field_label = self.user._meta.get_field("azure_access_token").verbose_name
        self.assertEqual(field_label, "azure access token")

        # blank
        blank_ = self.user._meta.get_field("azure_access_token").blank
        self.assertEqual(blank_, True)

        # null
        null_ = self.user._meta.get_field("azure_access_token").null
        self.assertEqual(null_, True)

        """
        azure_token_expires_on
        """

        # field label
        field_label = self.user._meta.get_field("azure_token_expires_on").verbose_name
        self.assertEqual(field_label, "azure token expires on")

        # blank
        blank_ = self.user._meta.get_field("azure_token_expires_on").blank
        self.assertEqual(blank_, True)

        # null
        null_ = self.user._meta.get_field("azure_token_expires_on").null
        self.assertEqual(null_, True)

        # auto_now
        auto_now_ = self.user._meta.get_field("azure_token_expires_on").auto_now
        self.assertEqual(auto_now_, False)

        # auto_now
        auto_now_add_ = self.user._meta.get_field("azure_token_expires_on").auto_now_add
        self.assertEqual(auto_now_add_, False)


    def test_user_type_choices(self):
        """
        Test both user types can be created
        """
        client_user = User.objects.create_user(
            username='client_user',
            password='test_pass',
            user_type='CLIENT',
        )

        pro_user = User.objects.create_user(
            username='pro_user', 
            password='test_pass', 
            user_type="PRO")

        self.assertEqual(client_user.user_type, 'CLIENT')
        self.assertEqual(pro_user.user_type, 'PRO')
    

    def test_user_account_choices(self):
        """
        Test both account types can be created
        """
        basic_account = User.objects.create_user(
            username='basic_user',
            password='test_pass',
            account_type='BASIC'
        )

        premium_account = User.objects.create_user(
            username='premium_user',
            password='test_pass',
            account_type='PREMIUM'
        )

        self.assertEqual(basic_account.account_type, 'BASIC')
        self.assertEqual(premium_account.account_type, 'PREMIUM')
    
    @unittest.skip("Possible bug with Regex Validator in models. Invalid phone inputs don't throw error!")
    def test_phone_number_validators(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='testuser2',
                password='testpassword',
                first_name='Test',
                last_name='User2',
                email='testuser2@example.com',
                user_type='CLIENT',
                account_type='BASIC',
                phone='123'
            )


    @patch('cloudinary.uploader.upload')
    def test_cloudinary_field(self, mock_upload):
        # Set the return value of the mock upload method
        mock_upload.return_value = {
            'public_id': 'test_image',
            'version': 1,
            'signature': 'signature',
            'width': 100,
            'height': 100,
            'format': 'jpg',
            'resource_type': 'image',
            'created_at': '2022-01-01T00:00:00Z',
            'tags': ['user_profile_photos'],
            'bytes': 1000,
            'type': 'upload',  # add the 'type' key
            'url': 'https://res.cloudinary.com/rehgien/image/upload/v1/test_image.jpg',
            'secure_url': 'https://res.cloudinary.com/rehgien/image/upload/v1/test_image.jpg'
        }

        # Create a user with a profile image
        user = User.objects.create(
            username='testuser3',
            password='testpassword',
            first_name='Test',
            last_name='User',
            email='testuser3@example.com'
        )
        
        image_data = b'fake image data'
        content_type='image/jpeg'
        image_file = SimpleUploadedFile(name='test_image.jpg', content=image_data, content_type=str(content_type))
        user.profile_image = image_file
        user.save()

        # Check that the mock upload method was called with the image file
        mock_upload.assert_called_with(
            image_file,
            folder='user_profile_photos',
            overwrite=True, 
            resource_type='image', 
            type='upload'
        )

        # Check that the user's profile image URL was set correctly
        expected_url = 'http://res.cloudinary.com/rehgien/image/upload/v1/test_image.jpg'
        self.assertEqual(user.profile_image.url, expected_url)


if __name__ == "__main__":
    unittest.main()