from stock_exchange import views
from django.urls import path


urlpatterns = [
    path('', views.MainPage.as_view(), name='index'),
    path('currency/<str:abbr>/', views.single_currency_page, name='currency'),
    path('converter/', views.currency_converter, name='converter'),
    path('converter/currency_valid/')
]
