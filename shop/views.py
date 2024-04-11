from django.shortcuts import render
from django.views import View
from orders.models import OrderProduct
from products.models import Product, Session

class ShopView(View):
    def get(self, request):
        not_ordered_products = list()
        products = Product.objects.filter(is_published=True)
        user = request.user
        for product in products:
            if user.is_authenticated:
                if not OrderProduct.objects.filter(user=user, ordered=True, product=product).exists():
                    not_ordered_products.append(product)
            else:
                not_ordered_products.append(product)
                
        context = {
            'products':not_ordered_products,
        }
        return render(request, 'shop/products.html', context)

class ProductDetailsView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        sessions = Session.objects.filter(product=product)
        context = {
            'product':product,
            'sessions': sessions,
        }
        return render(request, 'shop/product_details.html', context)
