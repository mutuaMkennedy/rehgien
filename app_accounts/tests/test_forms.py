from  django.test import SimpleTestCase, Client
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
