from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.shop, name='shop'),
    path('product_details/<int:pk>', views.product_details, name='product_details'),
    path('cart/', include('cart.urls')),
]
