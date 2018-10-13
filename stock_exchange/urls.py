from stock_exchange import views
from django.urls import path

app_name = 'exchange'

urlpatterns = [
    path('currencies/', views.Currencies.as_view(), name='currencies'),
    path('table/', views.TableCurrenciesPage.as_view(), name='table'),
    path('currency/<str:abbr>/', views.single_currency_page, name='currency'),
    path('converter/', views.currency_converter, name='converter'),
    path('api/chart/<str:abbr>/', views.api_chart_data, name='api-data'),
    path('chart/<str:abbr>', views.chart, name='chart')
]
