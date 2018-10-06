from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Currency
from .forms import CurrencyConverterForm
from currencyUpdater._currency import Currency as SingleCurrency


# Create your views here.


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = []

        for currency in currencies:
            name = currency.name
            code = currency.code
            unit = currency.unit
            last_rate = currency.rate_and_date_set.all().latest('date').rate
            last_date = currency.rate_and_date_set.all().latest('date').date

            currenct_currency = SingleCurrency(
                name, unit, code, last_rate, last_date)

            # currencies in list ()
            currencies_to_template.append(currenct_currency)

        return render(request, 'index.html', { 'currencies': currencies_to_template})


def single_currency_page(request, abbr):
        print('You are looking for', abbr)
        currency = get_object_or_404(Currency, code=abbr.upper())
        print('======', currency, '====== Found')

        rate = currency.rate_and_date_set.all().latest('date').rate
        date = currency.rate_and_date_set.all().latest('date').date

        return render(request, 'single_currency.html',
                    {
                        'currency': currency, 'rate': rate, 'date': date
                    })


def currency_converter(request):
    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)

        if form.is_valid():
            print('Form is valid.')
            return HttpResponseRedirect(reverse('exchange:currency'))
        print('Form isn\'t valid')

    else:
        print('Else')
        form = CurrencyConverterForm()

    return render(request, 'converter.html', {'form': form})


def currency_diagram(request, currency_abbr):
    response = "You're looking for <b>currency</b>: %s."
    return HttpResponse(response % currency_abbr)

