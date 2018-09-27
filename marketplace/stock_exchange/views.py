from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from stock_exchange.models import Currency


# Create your views here.


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        currencies = Currency.objects.all()

        return render(request, 'index.html',{'currencies': currencies})


def currency_diagram(request, currency_abbr):
    response = "You're looking for currency: %s."
    return HttpResponse(response % currency_abbr)


def currency_converter(request):
    return HttpResponse("You're looking for currency converter.")
