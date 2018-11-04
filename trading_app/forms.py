from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from stock_exchange.models import Currency


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class BuyCurrencyForm(forms.Form):
    def __init__(self, initial_code='USD', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial_code = initial_code

        self.fields['quantity'] = forms.IntegerField(min_value=1)
        self.fields['currency_code'] = forms.ChoiceField(choices=self.get_all_currencies(), initial=self.find_initial_index())

    def find_initial_index(self):
        '''Find index by currency code from url'''

        initial_index = 1
        for index, code in dict(self.get_all_currencies()).items():
            if code == self.initial_code:
                initial_index = index

        return initial_index

    def get_all_currencies(self):
        all_currencies = [(currency.pk, currency.code) for currency in Currency.objects.all()]

        return all_currencies


class SellCurrencyForm(forms.Form):
    def __init__(self, initial_code=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.initial_code = initial_code

        choices = self.create_index_code_pairs_in_list

        self.fields['quantity'] = forms.IntegerField(min_value=1)
        self.fields['currency_code'] = forms.ChoiceField(choices=choices)

    def create_index_code_pairs_in_list(self):
        '''Creates pairs index currency code in list'''

        owned_currencies = self.user.profile.boughtcurrency_set.all()
        choices = []
        i = 0
        for currency in owned_currencies:
            i += 1
            code = currency.currency_abbreviation
            choices.append((i, code))

        return choices
