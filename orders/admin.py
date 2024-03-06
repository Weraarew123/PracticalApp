from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInLine(admin.TabularInline):
        model = OrderProduct
        readonly_fields = ('payment', 'user', 'product', 'prdouct_price', 'ordered')
        extra = 0


class OrderAdmin(admin.ModelAdmin):
          list_display = ['order_number', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
          list_filter = ['status', 'is_ordered']
          search_fields = ['order_number',]
          list_per_page = 20
          inlines = [OrderProductInLine]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)