from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Profile
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingInfoForm, PaymentForm
# Create your views here.

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
        print(request.POST)   
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total
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

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})