from django.contrib import admin

from .models import Product, Session

admin.site.register(Product)
admin.site.register(Session)