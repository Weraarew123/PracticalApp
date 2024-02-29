from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def products(request):
    #produkt
    return render(request, 'shop/products.html')

def home(request):
    return render(request, 'index.html')