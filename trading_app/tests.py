from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class MainPageTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='usernameindb', password='zaq1@WSX')
        user.save()

    def test_login_redirect_pass(self):
        "Unlogged client doesnt get user view"
        response = self.client.get(reverse('trading_app:user'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/user/')
        response = self.client.post(reverse('trading_app:user'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/user/')

    def test_logging_form_with_user_in_database(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': 'usernameindb',
                                        'password': 'zaq1@WSX'
                                    },
                                    follow=True)
        self.assertRedirects(response, reverse('trading_app:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_loggin_form_without_user_in_database(self):
        "Client without account can't login"
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': 'usernamenotindb',
                                        'password': 'zaq1@WSX'
                                    },
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logged_client_user_view(self):
        "Logged client gets user view"
        self.client.login(username='usernameindb', password='zaq1@WSX')
        response = self.client.get(reverse('trading_app:user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user.html')
