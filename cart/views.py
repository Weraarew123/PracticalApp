from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))# get the cart using cart_id present in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        id =[]
        for item in cart_item:
            id.append(item.id)
    else:
        cart_item= CartItem.objects.create(
            product=product,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def cart(request, total=0, cart_items=None):
    try:
        tax=0
        grand_total=0
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

@login_required(login_url='login')
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')