from rest_framework.response import Response
from rest_framework.decorators import api_view
from stock_exchange.models import Currency


@api_view()
def api_currencies(request):
    currencies = Currency.objects.all()
    currency_codes = []
    currency_rates = []
    currency_units = []
    for currency in currencies:
        currency_codes.append(currency.code)
        currency_units.append(currency.unit)
        last_rate = currency.rate_and_date_set.all().order_by('-date')[0].rate
        currency_rates.append(last_rate)

    currency_codes_and_rates = {
        'currencies': {
            'codes': currency_codes,
            'rates': currency_rates,
            'units': currency_units,
        }
    }

    return Response(currency_codes_and_rates)
