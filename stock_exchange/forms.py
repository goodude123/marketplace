from django import forms
from .models import Currency


class CurrencyConverterForm(forms.Form):
    all_currencies = [(currency.pk, currency.code) for currency in Currency.objects.all()]
    amount = forms.IntegerField(min_value=1)
    from_currency = forms.ChoiceField(label='From', choices=all_currencies)
    to_currency = forms.ChoiceField(label='To', choices=all_currencies)
