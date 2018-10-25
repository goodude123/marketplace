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
    all_currencies = [(currency.pk, currency.code) for currency in Currency.objects.all()]
    currency_code = forms.ChoiceField(label='From', choices=all_currencies)
    quantity = forms.IntegerField(min_value=1)
