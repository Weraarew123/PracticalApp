from django.forms import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from orders.models import OrderProduct

from products.models import Product, Session
from .forms import EditUserForm, ProductsForm, SessionsForm
from django.contrib import messages

class InfoView(LoginRequiredMixin, View):
        def get(self, request):
                user = request.user
                if not user.is_active:
                        return Http404('Nie masz uprawnień do przeglądania tej strony')
                else:
                        orders = OrderProduct.objects.filter(user=user).order_by('-upadated_at')[:10]
                        context = {
                                'orders':orders,
                        }  
                        return render(request, 'dashboard/dashboard.html', context)

class UserDataView(LoginRequiredMixin, View):
        def get(self, request):
                return render(request, 'dashboard/user_data.html')

class UsersView(LoginRequiredMixin, View):
          def get(self, request):
                users = User.objects.all()
                context = {
                        'users':users,
                }
                return render(request, 'dashboard/users.html', context)

class EditUserView(LoginRequiredMixin, View):
        def get(self, request, pk):
                user = get_object_or_404(User, pk=pk)
                form = EditUserForm(instance=user)
                context = {
                        'form': form
                }
                return render(request, 'dashboard/edit_user.html', context)
        def post(self, request, pk):
                user = get_object_or_404(User, pk=pk)
                form = EditUserForm(request.POST, instance=user)
                if form.is_valid():
                        form.save()
                        messages.success(request, 'Zmiany zostały zapisane')
                        return redirect('users')

class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, 'Użytkownik pomyślnie usunięty')
        return redirect('users')


class CoursesView(LoginRequiredMixin, View):
        def get(self, request):
                products = Product.objects.all()
                sessions = Session.objects.all()
                context = {
                        'products':products,
                        'sessions':sessions,
                }
                return render(request, 'dashboard/courses.html', context)

class AddCourseView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductsForm()
        context = {
                'form': form,
        }
        return render(request, 'dashboard/add_course.html', context)
    def post(self, request):
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) # temporarily saving the form
            product.save()
            messages.success(request, 'Dodano kurs')
            return redirect('courses')
        else:
            messages.error(request, 'Błąd dodawania kursu')
            return redirect('add_course')

class EditCourseView(LoginRequiredMixin, View):
        def get(self, request, pk):
                product = get_object_or_404(Product, pk=pk)
                form = ProductsForm(instance=product)
                context = {
                        'form': form,
                        'product': product,
                }
                return render(request, 'dashboard/edit_course.html', context)
        def post(self, request, pk):
                form = ProductsForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                        product = form.save()
                        product.save()
                        messages.success(request, 'Zapisano zmiany')
                        return redirect('courses')
                else:
                       messages.error('Błąd zapisu zmian')
                       return redirect('edit_course', pk=pk)

class DeleteCourseView(LoginRequiredMixin, View):
        def post(self, request, pk):
                product = get_object_or_404(Product, pk=pk)
                product.delete()
                messages.success(request, 'Produkt pomyślnie usunięty')
                return redirect('courses')

class AddSessionView(LoginRequiredMixin, View):
        def get(self, request):
                form = SessionsForm()
                context = {
                        'form': form,
                }
                return render(request, 'dashboard/add_session.html', context)
        def post(self, request):
                form = SessionsForm(request.POST, request.FILES)
                if form.is_valid():
                        product = form.save(commit=False) # temporarily saving the form
                        product.save()
                        messages.success(request, 'Dodano kurs')
                        return redirect('courses')
                else:
                        messages.error(request, 'Błąd dodawania kursu')
                        return redirect('add_session')

        
class EditSessionView(LoginRequiredMixin, View):
        def get(self, request, pk):
                session = get_object_or_404(Session, pk=pk)
                form = SessionsForm(instance=session)
                context = {
                        'form': form,
                        'session': session,
                }
                return render(request, 'dashboard/edit_session.html', context)
        
        def post(self, request, pk):
                session = get_object_or_404(Session, pk=pk)
                form = SessionsForm(request.POST, request.FILES, instance=session)
                if form.is_valid():
                        session = form.save()
                        session.save()
                        messages.success(request, 'Zapisano zmiany')
                        return redirect('courses')
                else:
                        messages.error(request, 'Błąd zapisu zmian')
                        return redirect('edit_session', pk=pk)

class DeleteSessionView(LoginRequiredMixin, View):
        def post(self, request, pk):
                session = get_object_or_404(Session, pk=pk)
                session.delete()
                messages.success(request, 'Sesja pomyślnie usunięta')
                return redirect('courses')

class MyCoursesView(LoginRequiredMixin, View):
        def get(self, request):
                user = request.user
                if user.is_active == False:
                        raise Http404('Nie masz uprawnień do przeglądania tej strony')
                else:
                        orders = OrderProduct.objects.filter(user=user, ordered=True)
                        context = {
                                'orders':orders,
                        }
                        return render(request, 'dashboard/my_courses.html', context)

class MyCourseDetailsView(LoginRequiredMixin, View):
        def get(self, request, pk):
                user = request.user
                if not user.is_active:
                        return Http404('Nie masz uprawnień do przeglądania tej strony')
                else:
                        product = Product.objects.get(pk=pk)
                        sessions = Session.objects.filter(product=product)
                        context = {
                                'product':product,
                                'sessions':sessions,
                        }
                        return render(request, 'dashboard/my_course_details.html', context)