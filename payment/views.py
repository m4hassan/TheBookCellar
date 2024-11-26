from django.shortcuts import render
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingInfoForm
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

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})