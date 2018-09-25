from stock_exchange import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('currency/<str:currency_abbr>/', views.currency_diagram, name='diagram'),
    path('converter/', views.currency_converter, name='converter'),
]
