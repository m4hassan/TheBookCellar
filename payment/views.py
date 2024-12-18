from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from core.models import Product, Profile
from payment.forms import ShippingInfoForm, PaymentForm


def checkout(request):
    cart = Cart(request)
    # print(request.content_params)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total
    if request.user.is_authenticated:
        # Checkout as logged in user
        shipping_user = ShippingAddress.objects.get(shipping_user_id=request.user.id)
        shipping_form = ShippingInfoForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities':quantities, 'totals': totals, 'shipping_form':shipping_form})
    else:
        # Checkout as guest user
        shipping_form = ShippingInfoForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities':quantities, 'totals': totals, 'shipping_form':shipping_form})


def billing_info(request):
    if request.POST:
        # get the cart 
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total

        # save shipping data to session
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # if user is logged in
        if request.user.is_authenticated:
            # Get the billing form
            billing_form = PaymentForm()
            context = {'cart_products':cart_products, 
                       'quantities':quantities, 
                       'totals':totals, 
                       'shipping_info': request.POST, 
                       'billing_form':billing_form,
                       }
            return render(request, 'payment/billing_info.html', context)
        # if user is a guest
        else:
            billing_form = PaymentForm() 
            context = {'cart_products':cart_products, 
                       'quantities':quantities, 
                       'totals':totals, 
                       'shipping_info': request.POST,
                       'billing_form':billing_form,
                       }
            return render(request, 'payment/billing_info.html', context)
    else:
        messages.success(request, ("Access Denied!"))
        return redirect('index')


def process_order(request):
    if request.POST:
        # get cart data
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants()
        totals = cart.cart_total()
        # get payment form
        payment_form = PaymentForm(request.POST or None)
        # get shipping info from session
        shipping_info = request.session.get('my_shipping')
        print(shipping_info)
        
        # Gather order info
        full_name = shipping_info['shipping_full_name']
        email = shipping_info.get('shipping_email')
        phone = shipping_info.get('shipping_phone')
        # create shipping address from session info
        shipping_address = f"{shipping_info['shipping_address1']}\n{shipping_info['shipping_address2']}\n{shipping_info['shipping_city']}\n{shipping_info['shipping_state']}\n{shipping_info['shipping_zipcode']}\n{shipping_info['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # logged in
            user = request.user
        else:
            # not logged in
            user = None

        # create order
        create_order = Order(user=user, 
                             full_name=full_name, 
                             email=email, 
                             phone=phone, 
                             shipping_address=shipping_address, 
                             amount_paid=amount_paid,
                             )
        create_order.save()

        # add order items
        # get order id
        order_id = create_order.pk
        # get product info
        for product in cart_products():
            product_id = product.id
            quantity = quantities[str(product_id)]
            if product.is_sales:
                price = product.sales_price
            else:
                price = product.price
            # create and save order item 
            create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=quantity, price=price)
            create_order_item.save()

        # clear cart items
        for key in list(request.session.keys()):
            if key == 'session_key':
                # delete the key
                del request.session[key]
        # clear cart from db if user is logged in
        if request.user.is_authenticated:
            current_user = Profile.objects.get(user_id=request.user.id)
            current_user.old_cart = ""
            current_user.save()

        messages.success(request, ("Order placed!"))
        return redirect('index')
    
    else:
        messages.error(request, ("Access Denied!"))
        return redirect('index')


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})