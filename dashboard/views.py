from django.forms import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import OrderProduct

from products.models import Product, Session
from .forms import EditUserForm, ProductsForm, SessionsForm
from django.contrib import messages

@login_required
def info(request):
        user = request.user
        if user.is_active == False:
                return Http404('Nie masz uprawnień do przeglądania tej strony')
        else:
                orders = OrderProduct.objects.filter(user=user).order_by('-upadated_at')[:10]
                context = {
                        'orders':orders,
                }  
                return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_data(request):
        user = request.user
        if user.is_active == False:
                return Http404('Nie masz uprawnień do przeglądania tej strony')
        else:
                return render(request, 'dashboard/user_data.html')

@login_required
def users(request):
          users = User.objects.all()
          context = {
                'users':users,
          }
          return render(request, 'dashboard/users.html', context)

@login_required
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

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Użytkownik pomyślnie usunięty')
    return redirect('users')


@login_required
def courses(request):
        products = Product.objects.all()
        sessions = Session.objects.all()
        context = {
                'products':products,
                'sessions':sessions,
        }
        return render(request, 'dashboard/courses.html', context)

@login_required
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

@login_required
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

@login_required
def delete_course(request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, 'Produkt pomyślnie usunięty')
        return redirect('courses')

@login_required
def add_session(request):
        errors = ''
        if request.method == 'POST':
                form = SessionsForm(request.POST, request.FILES)
                if form.is_valid():
                        product = form.save(commit=False) # temporarily saving the form
                        product.save()
                        messages.success(request, 'Dodano kurs')
                        return redirect('courses')
                else:
                        errors = form.errors
                        print(errors)
        form = SessionsForm()
        context = {
                'form': form,
                'errors': errors,
        }
        return render(request, 'dashboard/add_session.html', context)

@login_required
def edit_session(request, pk):
        session = get_object_or_404(Session, pk=pk)
        if request.method == 'POST':
                form = SessionsForm(request.POST, request.FILES, instance=session)
                if form.is_valid():
                        session = form.save()
                        session.save()
                        messages.success(request, 'Zapisano zmiany')
                        return redirect('courses')
        form = SessionsForm(instance=session)
        context = {
                'form': form,
                'session': session,
        }
        return render(request, 'dashboard/edit_session.html', context)

@login_required
def delete_session(request, pk):
        session = get_object_or_404(Session, pk=pk)
        session.delete()
        messages.success(request, 'Sesja pomyślnie usunięta')
        return redirect('courses')

@login_required
def my_courses(request):
        user = request.user
        if user.is_active == False:
                return Http404('Nie masz uprawnień do przeglądania tej strony')
        else:
                orders = OrderProduct.objects.filter(user=user, ordered=True)
                context = {
                        'orders':orders,
                }
                return render(request, 'dashboard/my_courses.html', context)

@login_required
def my_course_details(request, pk):
        user = request.user
        if user.is_active == False:
                return Http404('Nie masz uprawnień do przeglądania tej strony')
        else:
                product = Product.objects.get(pk=pk)
                sessions = Session.objects.filter(product=product)
                context = {
                        'product':product,
                        'sessions':sessions,
                }
                return render(request, 'dashboard/my_course_details.html', context)