import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Currency
from .forms import CurrencyConverterForm
from .system.pack import pack_currencies
from .system.real_value import real_course_value
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'index.html', { 'currencies': currencies_to_template})


def chart(request, abbr):
    return render(request, 'charts.html', {'abbr': abbr.upper()})


@api_view()
def api_chart_data(request, abbr):
    currency = get_object_or_404(Currency, code=abbr.upper())
    courses_in_db = currency.rate_and_date_set.all().order_by('-date')[:30]
    rates = []
    dates = []

    for course in courses_in_db:
        rates.append(course.rate)
        dates.append(course.date)

    data = {
        'rates': rates,
        'dates': dates,

    }
    return Response(data)


class TableCurrenciesPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'currencies_table.html', {'currencies': currencies_to_template})


def single_currency_page(request, abbr):
        print('You are looking for', abbr)
        currency = get_object_or_404(Currency, code=abbr.upper())
        print('======', currency, '====== Found')

        courses_db = currency.rate_and_date_set.all().order_by('-date')[:30]
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
    # Operate on send data from form
    if request.method == 'GET':
        # if thats a first visit in converter
        if len(request.GET) == 0:
            form = CurrencyConverterForm()
            return render(request, 'converter.html', {'form': form})

        # if thats a submitted view
        else:
            form = CurrencyConverterForm(request.GET)
            if form.is_valid():
                # get values from db
                from_currency = Currency.objects.get(pk=request.GET['from_currency'])
                to_currency = Currency.objects.get(pk=request.GET['to_currency'])

                amount = request.GET['amount']

                from_course_unit = [
                    from_currency.rate_and_date_set.all().order_by('-date')[1].rate,
                    from_currency.unit
                ]

                to_course_unit = [
                    to_currency.rate_and_date_set.all().order_by('-date')[1].rate,
                    to_currency.unit
                ]

                print(from_course_unit)

                from_real_course_value = real_course_value(from_course_unit)
                to_real_course_value = real_course_value(to_course_unit)

                result = round(float(amount) * (from_real_course_value / to_real_course_value), 4)

                return render(request, 'converter.html', {'form': form, 'result': result})

        print('Form isn\'t valid')


def currency_diagram(request, currency_abbr):
    response = "You're looking for <b>currency</b>: %s."
    return HttpResponse(response % currency_abbr)

