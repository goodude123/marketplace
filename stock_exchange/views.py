from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView
from .models import Currency
from .forms import CurrencyConverterForm
from .system.pack import pack_currencies


class Currencies(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'currencies.html', { 'currencies': currencies_to_template})


def chart(request, abbr):
    return render(request, 'charts.html', {'abbr': abbr.upper()})


class ChartDataApiView(APIView):
    def get(self, request, *args, **kwargs):
        currency = get_object_or_404(Currency, code=kwargs['abbr'].upper())
        valuations = currency.rate_and_date_set.all().order_by('-date')[:30]
        
        data = self.get_values_and_dates(valuations)
        return Response(data)
    
    def get_values_and_dates(self, valuations):
        data = {
            'rates': [],
            'dates': [],
        }

        for valuation in valuations:
            data['rates'].append(valuation.rate)
            data['dates'].append(valuation.date)

        return data

class TableCurrenciesPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()
        currencies_to_template = pack_currencies(currencies)

        return render(request, 'currencies_table.html', {'currencies': currencies_to_template})


class SingleCurrencyView(TemplateView):
    template_name = 'single_currency.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = get_object_or_404(Currency, code=kwargs['abbr'].upper())
        context['currency'] = currency
        context['valuation'] = self.get_valuations(currency)
        return context

    def get_valuations(self, currency):
        valuations = currency.rate_and_date_set.all().order_by('-date')[:30]
        return [{'date': valuation.date, 'rate': valuation.rate} for valuation in valuations]


class CurrencyConverterView(FormView):
    template_name = 'converter.html'
    form_class = CurrencyConverterForm

    def form_valid(self, form):
        from_currency = Currency.objects.get(pk=form.cleaned_data['from_currency'])
        to_currency = Currency.objects.get(pk=form.cleaned_data['to_currency'])
        amount = form.cleaned_data['amount']

        packed_from_currency = self.pack_currency(from_currency)
        packed_to_currency = self.pack_currency(to_currency)

        result = self.get_result(amount, packed_from_currency, packed_to_currency)

        data = {
            'form': form,
            'amount': amount,
            'from': from_currency.code,
            'to': to_currency.code,
            'result': result,
        }

        return render(self.request, 'converter.html', data)
    
    def pack_currency(self, currency):
        packed = {
            'valuation': currency.rate_and_date_set.all().order_by('-date')[0].rate,
            'unit': currency.unit
        }
        return packed

    def get_result(self, amount, from_currency, to_currency):
        real_from_currency_value = self.real_currency_value(from_currency)
        real_to_currency_value = self.real_currency_value(to_currency)
        return round(float(amount) * (real_from_currency_value / real_to_currency_value), 4)

    def real_currency_value(self, currency):
        real_value = currency['valuation'] * currency['unit']
        return real_value
