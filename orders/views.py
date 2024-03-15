import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from cart.models import CartItem
from products.models import Product
from .models import Order, OrderProduct, Payment

class PaymentsView(View):
        def post(self, request):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
                
                #Store transaction details inside Payment model
                payment = Payment(
                        user=request.user,
                        payment_id = body['transID'],
                        payment_method = body['payment_method'],
                        amount_paid = order.order_total,
                        status = body['status'],
                )
                payment.save()
                order.payment = payment
                order.is_ordered = True
                order.save()

                #Move the cart items to Order Product table
                cart_items = CartItem.objects.filter(user=request.user)

                for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.pk
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.prdouct_price = item.product.price
                        orderproduct.ordered = True
                        orderproduct.save()
                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.save()

                #Clear cart
                CartItem.objects.filter(user=request.user).delete()
                #Send order number and transaction id back to sendData method via JsonResponse
                data = {
                        'order_number': order.order_number,
                        'transID': payment.payment_id,
                }
                return JsonResponse(data)
        def get(self, request):
                return JsonResponse({'error' : 'Invalid request method'})

class OrderView(View):
        def get(self, request, total=0):
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

class OrderCompleteView(View):
        def get(self, request):
                order_number = request.GET.get('order_number')
                transID = request.GET.get('payment_id')

                try:
                        order = Order.objects.get(order_number=order_number, is_ordered=True)
                        ordered_products = OrderProduct.objects.filter(order_id=order.id)

                        subtotal = 0
                        for i in ordered_products:
                                subtotal+=i.prdouct_price

                        payment = Payment.objects.get(payment_id=transID)
                        context = {
                                'order':order,
                                'order_products': ordered_products,
                                'order_number': order.order_number,
                                'transID': payment.payment_id,
                                'payment': payment,
                                'subtotal':subtotal,
                        }
                        return render(request, 'payments/order_complete.html', context)
                except (Payment.DoesNotExist, Order.DoesNotExist):
                        return redirect('home')