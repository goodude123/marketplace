from stock_exchange import views
from django.urls import path

app_name = 'exchange'

urlpatterns = [
    path('currencies/', views.Currencies.as_view(), name='currencies'),
    path('table/', views.TableCurrenciesPage.as_view(), name='table'),
    path('currency/<str:abbr>/', views.SingleCurrencyView.as_view(), name='currency'),
    path('converter/', views.CurrencyConverterView.as_view(), name='converter'),
    path('api/chart/<str:abbr>/', views.ChartDataApiView.as_view(), name='api-data'),
    path('chart/<str:abbr>', views.chart, name='chart'),
]
