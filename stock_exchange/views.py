from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Currency
from .forms import CurrencyConverterForm
from .system.pack import pack_currencies


# Create your views here.


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'index.html', { 'currencies': currencies_to_template})


class TableCurrenciesPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'currencies_table.html', {'currencies': currencies_to_template})


def single_currency_page(request, abbr):
        print('You are looking for', abbr)
        currency = get_object_or_404(Currency, code=abbr.upper())
        print('======', currency, '====== Found')

        courses_db = currency.rate_and_date_set.all().order_by('date').reverse()[:30]
        courses_to_template = []

        for course_db in courses_db:
            course = {}
            course['date'] = course_db.date
            course['rate'] = course_db.rate

            courses_to_template.append(course)

        return render(request, 'single_currency.html',
                    {
                        'currency': currency, 'courses': courses_to_template,
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
