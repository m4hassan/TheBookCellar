from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .cart import Cart
from core.models import Product, Profile


def cart_summary(request):
    cart = Cart(request)
    # print(request.content_params)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total

    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, 'quantities':quantities, 'totals': totals})


def cart_add(request):
    # Get the cart for current user
    cart = Cart(request)
    # Test for POST request
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # product = Product.objects.get(pk=product_id)
        # Look product in DB
        product = get_object_or_404(Product, id=product_id) 
        # Save to session
        cart.add(product=product, product_qty=product_qty)
        cart_quantity = cart.__len__()
        messages.success(request, ("Product added to cart..."))
        # Return a response
        response = JsonResponse({
            'product_name': product.name,
            'price': product.price,
            'product_qty': product_qty,
            'cart_quantity': cart_quantity
        })

        return response
   

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        cart.delete(product=product_id)
        messages.success(request, ("Product removed from cart..."))

    return JsonResponse({'product_id':product_id})
    

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, ("Product updated in cart..."))
        
    
    return JsonResponse({'product_id':product_id, 'quantity':product_qty})
    # return redirect('cart_summary')