from django import forms
from django.contrib.auth.models import User
from products.models import Product, Session

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'is_published')

class SessionsForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('name', 'image', 'film', 'file', 'product')