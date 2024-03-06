import datetime
from django.shortcuts import redirect, render

from cart.models import CartItem
from .models import Order

def order(request, total=0):
          user = request.user

          cart_items = CartItem.objects.filter(user=user)
          cart_count = cart_items.count()
          if cart_count < 0:
                  return redirect('shop')
          
          grand_total = 0
          tax=0
          for item in cart_items:
                  total += item.product.price
          tax = (23*total)/100
          grand_total = total+tax
          data = Order()
          data.user = user
          data.ip = request.META.get('REMOTE_ADDR')
          data.tax = tax
          data.order_total = grand_total
          data.save()
          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,dt,mt)
          current_date = d.strftime('%Y%m%d')
          order_number = current_date + str(data.id)
          data.order_number = order_number
          data.save()

          order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
          context ={
                    'order':order,
                    'cart_items':cart_items,
                    'total':total,
                    'tax':tax,
                    'grand_total':grand_total,
          }

          return render(request, 'payments/PaySite.html', context)
