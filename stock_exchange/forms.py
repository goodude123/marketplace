from django import forms
from models import Currency


class CurrencyConverter(forms.Form):
    from_currency = forms.ChoiceField(Currency.objects.all())
    to_currency = forms.ChoiceField(Currency.objects.all())
