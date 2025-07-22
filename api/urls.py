from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('menu/', views.menu),
    path('orders/', views.create_order),
    path('orders/history/', views.order_history),
]


