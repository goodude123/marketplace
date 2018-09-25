from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello on the index page.")


def currency_diagram(request, currency_abbr):
    response = "You're looking for currency: %s."
    return HttpResponse(response % currency_abbr)


def currency_converter(request):
    return HttpResponse("You're looking for currency converter.")
