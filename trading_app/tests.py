from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserViewTestCase(TestCase):

    username = 'usernameindb'
    password = 'zaq1@WSX'

    def setUp(self):
        user = User.objects.create_user(
                                        username=UserViewTestCase.username,
                                        password=UserViewTestCase.password
                                        )
        user.save()

    def test_unlogged_client_access_to_user_page(self):
        "Unlogged client doesnt get user view"
        response = self.client.get(reverse('trading_app:user'), follow=True)
        self.assertRedirects(response, '/login/?next=/user/')
        response = self.client.post(reverse('trading_app:user'), follow=True)
        self.assertRedirects(response, '/login/?next=/user/')

    def test_logged_client_user_view(self):
        "Logged client gets user view"
        self.client.login(username='usernameindb', password='zaq1@WSX')
        response = self.client.get(reverse('trading_app:user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user.html')


class LoginTestCase(TestCase):

    username = 'usernameindb'
    password = 'zaq1@WSX'

    def setUp(self):
        user = User.objects.create_user(username=LoginTestCase.username, password=LoginTestCase.password)
        user.save()

    def test_logging_form_with_user_in_database(self):
        "Valid loggin with user in database"
        response = self.client.post(reverse('login'),
                                    {
                                        'username': LoginTestCase.username,
                                        'password': LoginTestCase.password
                                    },
                                    follow=True)
        self.assertRedirects(response, reverse('trading_app:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_loggin_form_without_user_in_database(self):
        "Client without account can't login."
        response = self.client.post(reverse('login'),
                                    {
                                        'username': 'usernamenotindb',
                                        'password': 'zaq1@WSX'
                                    },
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout(self):
        "Logout redirect us to home page."
        self.client.login(
                        username=LoginTestCase.username,
                        password=LoginTestCase.password
                        )
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('trading_app:home'))


class SignUpTestCase(TestCase):

    username = 'usernameindb'
    password = 'zaq1@WSX'
    first_name = 'john'
    last_name = 'kowalski'
    email = 'john@kowalski.com'

    def setUp(self):
        user = User.objects.create_user(username=SignUpTestCase.username,
                                        password=SignUpTestCase.password,
                                        first_name=SignUpTestCase.first_name,
                                        last_name=SignUpTestCase.last_name,
                                        email=SignUpTestCase.email
                                        )
        user.save()

    def test_valid_sign_up(self):
        "Valid registration."
        response = self.client.post(reverse('trading_app:signup'),
                                    {
                                        'username': 'unregistereduser',
                                        'first_name': SignUpTestCase.first_name,
                                        'last_name': SignUpTestCase.last_name,
                                        'email': SignUpTestCase.email,
                                        'password1': SignUpTestCase.password,
                                        'password2': SignUpTestCase.password
                                    })
        self.assertRedirects(response, reverse('trading_app:home'))

    def test_invalid_sign_up_user_alread_in_database(self):
        "Invalid registration user already exists."
        response = self.client.post(reverse('trading_app:signup'),
                                    {
                                        'username': SignUpTestCase.username,
                                        'password': SignUpTestCase.password,
                                        'first_name': SignUpTestCase.first_name,
                                        'last_name': SignUpTestCase.last_name,
                                        'email': SignUpTestCase.email
                                    })
        self.assertTemplateUsed(response, 'signup.html')

    def test_access_sign_up_logged_user(self):
        "Logged user is redirected to home trying access sign up view."
        self.client.login(
                        username=SignUpTestCase.username,
                        password=SignUpTestCase.password
                        )
        response = self.client.get(reverse('trading_app:signup'))
        self.assertRedirects(response, reverse('trading_app:home'))
