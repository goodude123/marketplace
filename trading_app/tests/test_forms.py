from django.test import TestCase
from .. import forms # trading_app folder

class SignUpFormTestCase(TestCase):
    def test_valid_user_sign_up(self):
        form = forms.SignUpForm(data={
            'username': 'validusername',
            'first_name': 'name',
            'last_name': 'last_name',
            'email': 'validemail@email.com',
            'password1': 'validpassword',
            'password2': 'validpassword',
            })
        self.assertTrue(form.is_valid())

    def test_invalid_user_sign_up(self):
        form = forms.SignUpForm(data={
            'username': '',
            'first_name': '',
            'last_name': 'last_name',
            'email': '',
            'password1': 'invalidpassword',
            'password2': 'diffinvalidpassword',
            })
        self.assertFalse(form.is_valid())