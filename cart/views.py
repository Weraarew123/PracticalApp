from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import _cart_id

class AddCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        user = request.user
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))# get the cart using cart_id present in session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
    
        cart_item = CartItem.objects.get_or_create(product=product, cart = cart)
        cart_item.user = user
        return redirect('cart')

class CartView(LoginRequiredMixin, View):
    def get(self, request, total=0, cart_items=None):
        tax=0
        grand_total=0
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total+=cart_item.product.price
            tax = (12 * total)/100
            grand_total = total+tax
        except ObjectDoesNotExist:
            pass
        
        context = {
            'total':total,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
        }
        return render(request, 'shop/cart.html', context)

class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, product_id, cart_item_id):
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(Cart, product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        return redirect('cart')