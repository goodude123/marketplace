from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from stock_exchange.models import Currency
from currencyUpdater._currency import Currency as SingleCurrency


# Create your views here.


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_template = []

        for currency in currencies:
            name = currency.name
            code = currency.abbreviation
            unit = currency.unit
            last_rate = currency.rate_and_date_set.all().latest('date').rate
            last_date = currency.rate_and_date_set.all().latest('date').date

            currenct_currency = SingleCurrency(name, unit, code, last_rate, last_date)
            currencies_template.append(currenct_currency)

        return render(request, 'index.html', {'currencies': currencies_template})


def currency_diagram(request, currency_abbr):
    response = "You're looking for currency: %s."
    return HttpResponse(response % currency_abbr)


def currency_converter(request):
    return HttpResponse("You're looking for currency converter.")
