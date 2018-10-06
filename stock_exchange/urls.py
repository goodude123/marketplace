from stock_exchange import views
from django.urls import path

app_name = 'exchange'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('table/', views.TableCurrenciesPage.as_view(), name='table'),
    path('currency/<str:abbr>/', views.single_currency_page, name='currency'),
    path('converter/', views.currency_converter, name='converter'),
]
