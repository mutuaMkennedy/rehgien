from  django.test import SimpleTestCase
import phonenumbers
from .. import forms

class UserPhoneNumberFormTest(SimpleTestCase):
    def test_invalid_data(self):
        empty_data = {"phone":""}
        invalid_data = {"phone":"+254123456"}

        form_1 = forms.UserPhoneNumber(data=empty_data)
        form_2 = forms.UserPhoneNumber(data=invalid_data)

        self.assertEqual(form_1.errors, {
            "phone":["This field is required."]
        })

        self.assertEqual(form_2.errors, {
            "phone":["Enter a valid phone number (e.g. +12125552368)."]
        })

    def test_valid_data(self):
        phone = phonenumbers.parse("0712345678", "KE")
        formatted_phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL )
        data = {"phone":formatted_phone}
 
        form = forms.UserPhoneNumber(data=data)

        self.assertTrue(form.is_valid())

class UserEmailFormTest(SimpleTestCase):
    def test_invalid_data(self):
        empty_data = {"email":""}
        invalid_data = {"email":"test_email"}

        form_1 = forms.UserEmail(data=empty_data)
        form_2 = forms.UserEmail(data=invalid_data)

        self.assertEqual(form_1.errors, {
            "email":["This field is required."]
        })

        self.assertEqual(form_2.errors, {
            "email":["Enter a valid email address."]
        })

    def test_valid_data(self):
        data = {"email":"test_email@email.com"}
 
        form = forms.UserEmail(data=data)
        
        self.assertTrue(form.is_valid())

class PhoneVerificationCodeTest(SimpleTestCase):
    def test_invalid_data(self):
        empty_data = {"code":""}
        invalid_data = {"code":"code"}

        form_1 = forms.PhoneVerificationCode(data=empty_data)
        form_2 = forms.PhoneVerificationCode(data=invalid_data)

        self.assertEqual(form_1.errors, {
            "code":["This field is required."]
        })

        self.assertEqual(form_2.errors, {
            "code":["Enter a whole number."]
        })

    def test_valid_data(self):
        data = {"code":1234}
 
        form = forms.PhoneVerificationCode(data=data)
        
        self.assertTrue(form.is_valid())

class PasswordTest(SimpleTestCase):
    def test_invalid_data(self):
        data = {"password":""}

        form_1 = forms.Password(data=data)

        self.assertEqual(form_1.errors, {
            "password":["This field is required."]
        })

    def test_valid_data(self):
        data = {"password":"password123*"}
 
        form = forms.Password(data=data)
        
        self.assertTrue(form.is_valid())