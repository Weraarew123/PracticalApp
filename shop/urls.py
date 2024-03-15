from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('product_details/<int:pk>', views.ProductDetailsView.as_view(), name='product_details'),
    path('cart/', include('cart.urls')),
]
