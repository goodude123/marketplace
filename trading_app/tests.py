from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from trading_app import errors
from stock_exchange.models import Currency


# every testing method must starts with 'test'

username = 'usernameindb'
password = 'zaq1@WSX'
first_name = 'john'
last_name = 'kowalski'
email = 'john@kowalski.com'


class UserViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
                                        username=username,
                                        password=password
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
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('trading_app:user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user.html')


class LoginTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username=username, password=password)
        user.save()

    def test_logging_form_with_user_in_database(self):
        "Valid loggin with user in database"
        response = self.client.post(reverse('login'),
                                    {
                                        'username': username,
                                        'password': password
                                    },
                                    follow=True)
        self.assertRedirects(response, reverse('trading_app:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_loggin_form_without_user_in_database(self):
        "Client without account can't login."
        response = self.client.post(reverse('login'),
                                    {
                                        'username': 'usernamenotindb',
                                        'password': 'zaq1@WSX'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout(self):
        "Logout redirect us to home page."
        self.client.login(
                        username=username,
                        password=password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('trading_app:home'))


class SignUpTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email
                                        )
        user.save()

    def test_valid_sign_up(self):
        "Valid registration."
        response = self.client.post(reverse('trading_app:signup'),
                                    {
                                        'username': 'unregistereduser',
                                        'first_name': first_name,
                                        'last_name': last_name,
                                        'email': email,
                                        'password1': password,
                                        'password2': password})
        self.assertRedirects(response, reverse('trading_app:home'))

    def test_invalid_sign_up_user_alread_in_database(self):
        "Invalid registration user already exists."
        response = self.client.post(reverse('trading_app:signup'),
                                    {
                                        'username': username,
                                        'password': password,
                                        'first_name': first_name,
                                        'last_name': last_name,
                                        'email': email
                                    })
        self.assertTemplateUsed(response, 'signup.html')

    def test_access_sign_up_logged_user(self):
        "Logged user is redirected to home trying access sign up view."
        self.client.login(
                        username=username,
                        password=password)
        response = self.client.get(reverse('trading_app:signup'))
        self.assertRedirects(response, reverse('trading_app:home'))

    def test_is_initial_money_equal_to_houndred(self):
        self.client.post(reverse('trading_app:signup'),
                        {
                            'username': 'unregistereduser',
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'password1': password,
                            'password2': password})
        user = User.objects.get(username='unregistereduser')
        self.assertEqual(user.profile.money, 100)


def create_user():
    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    user.save()


def create_currency():
    currency = Currency.objects.create(
                                        name='dolar',
                                        unit=1,
                                        code='USD')
    currency.save()

    currency.rate_and_date_set.create(rate=1, date=timezone.now())


def get_user():
    user = User.objects.get(username=username)

    return user


class BuyingCurrenciesTestCase(TestCase):

    def setUp(self):
        "Created user and new currency"
        create_user()
        create_currency()
        self.profile = get_user().profile

    def test_model_valid_currency_bought(self):
        "Valid bought test, user has enough money to buy."
        buys_quantity = 10
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)
        bought = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        self.assertEqual(bought.amount, 10)

    def test_model_buying_invalid_too_high_price(self):
        "Invalid bought test, user hasn't enought money."
        buys_quantity = 100000
        currency_primary_key = 1

        self.assertRaises(errors.BuyingError, lambda:
                self.profile.buy(currency_primary_key, buys_quantity))

    def test_model_buying_currencies_already_having(self):
        "Buying currencies already having. Bought currencies two times."
        buys_quantity = 5
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)
        self.profile.buy(currency_primary_key, buys_quantity)

        bought = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        self.assertEqual(bought.amount, 2 * buys_quantity)


class SellingCurrenciesTestCase(TestCase):

    def setUp(self):
        "Created user and new currency"
        create_user()
        create_currency()
        self.profile = get_user().profile

    def test_model_valid_sold_currencies(self):
        "Valid sold currencies."
        buys_quantity = 10
        sells_quantity = 8
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)

        self.profile.sell(currency_primary_key, sells_quantity)
        already_owned_currency = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        difference = buys_quantity - sells_quantity
        self.assertEqual(already_owned_currency.amount, difference)

    def test_model_invalid_sold_currencies_too_many(self):
        "Invalid test, tried to sell more currencies than had."
        buys_quantity = 2
        sells_quantity = 8
        currency_primary_key = 1

        self.profile.buy(currency_primary_key, buys_quantity)

        self.assertRaises(errors.SellingError, lambda:
                    self.profile.sell(currency_primary_key, sells_quantity))


class OwnedCurrenciesView(TestCase):
    def setUp(self):
        create_user()
        create_currency()

    def test_logged_user_acces_to_owned_currencies(self):
        "Logged user successfuly gets owned view."
        self.client.login(username=username, password=password)
        response = self.client.post(reverse('trading_app:owned_currencies'))
        self.assertTemplateUsed(response, 'owned_currencies.html')

    def test_unlogged_user_access_to_owned_currencies(self):
        "Invalid try to access owned page. Unlogged user is redirected to login view."
        response = self.client.post(reverse('trading_app:owned_currencies'))
        self.assertRedirects(response, '/login/?next=/owned/')
