from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from orders.models import OrderProduct
from products.models import Product, Session

class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        not_ordered_products = list()
        products = Product.objects.filter(is_published=True)
        user = request.user
        for product in products:
            if not OrderProduct.objects.filter(user=user, ordered=True, product=product).exists():
                print(user)
                print(product)
                not_ordered_products.append(product)

        print(not_ordered_products)  
        context = {
            'products':not_ordered_products,
        }
        return render(request, 'shop/products.html', context)

class ProductDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        sessions = Session.objects.filter(product=product)
        context = {
            'product':product,
            'sessions': sessions,
        }
        return render(request, 'shop/product_details.html', context)
