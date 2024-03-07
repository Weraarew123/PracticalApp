from django.urls import path
from . import views


urlpatterns = [
    path('', views.order, name="order"),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
