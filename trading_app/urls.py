from django.urls import path
from trading_app import views


app_name = 'trading_app'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user/', views.User.as_view(), name='user'),
    path('signup/', views.signup, name='signup'),
    path('owned/', views.owned_currencies, name='owned_currencies'),
    path('buy/', views.buy_currencies, name='buy')
]
