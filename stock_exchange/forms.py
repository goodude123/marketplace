from django import forms
from .models import Currency


class CurrencyConverterForm(forms.Form):
    all_currencies = [(currency.unit, currency.code) for currency in Currency.objects.all()]
    from_currency = forms.ChoiceField(choices=all_currencies)
    to_currency = forms.ChoiceField(choices=all_currencies)
