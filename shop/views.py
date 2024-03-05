from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product, Session

@login_required(login_url='login')
def shop(request):
    products = Product.objects.filter(is_published=True)
    context = {
        'products':products,
    }
    return render(request, 'shop/products.html', context)

@login_required(login_url='login')
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    sessions = Session.objects.filter(product=product)
    context = {
        'product':product,
        'sessions': sessions,
    }
    return render(request, 'shop/product_details.html', context)