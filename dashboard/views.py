from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from products.models import Product, Session
from .forms import EditUserForm, ProductsForm
from django.contrib import messages

@login_required(login_url='login')
def info(request):
          return render(request, 'dashboard/dashboard.html')

def user_data(request):
          return render(request, 'dashboard/user_data.html')

def users(request):
          users = User.objects.all()
          context = {
                  'users':users,
          }
          return render(request, 'dashboard/users.html', context)

def edit_user(request, pk):
          user = get_object_or_404(User, pk=pk)
          if request.method == "POST":
                    form = EditUserForm(request.POST, instance=user)
                    if form.is_valid():
                              form.save()
                              messages.success(request, 'Zmiany zostały zapisane')
                              return redirect('users')
          form = EditUserForm(instance=user)
          context = {
                  'form': form
          }
          return render(request, 'dashboard/edit_user.html', context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success('Użytkownik pomyślnie usunięty')
    return redirect('users')


def courses(request):
        products = Product.objects.all()
        sessions = Session.objects.all()
        context = {
                'products':products,
                'sessions':sessions,
        }
        return render(request, 'dashboard/courses.html', context)

def add_course(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) # temporarily saving the form
            product.save()
            messages.success(request, 'Dodano kurs')
            return redirect('courses')
        else:
            print('formularz jest błędny')
            print(form.errors)
    form = ProductsForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_course.html', context)

def edit_course(request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
                form = ProductsForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                        product = form.save()
                        product.save()
                        messages.success(request, 'Zapisano zmiany')
                        return redirect('courses')
        form = ProductsForm(instance=product)
        context = {
                'form': form,
                'product': product,
        }
        return render(request, 'dashboard/edit_course.html', context)


def delete_course(request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, 'Produkt pomyślnie usunięty')
        return redirect('courses')