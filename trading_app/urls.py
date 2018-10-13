from django.urls import path
from trading_app import views


app_name = 'trading_app'

urlpatterns = [
    path('', views.home_view, name='home'),
]
