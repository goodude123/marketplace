from django.urls import path
from trading_app import views
from trading_app import api_views


app_name = 'trading_app'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user/', views.User.as_view(), name='user'),
    path('sign_up/', views.SignUpView.as_view(), name='signup'),
    path('owned/', views.OwnedCurrenciesView.as_view(), name='owned_currencies'),
    path('buy/<str:initial>/', views.BuyCurrencyView.as_view(), name='buy'),
    path('sell/<str:initial>/', views.SellCurrencyView.as_view(), name='sell'),
    path('api/currencies/', api_views.api_currencies, name='api-currencies'),
]
