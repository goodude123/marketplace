from django.urls import path
from trading_app import views


app_name = 'trading_app'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user/', views.User.as_view(), name='user')
]
