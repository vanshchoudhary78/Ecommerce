from cmath import log

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required


from .models import Profile
from product.models import *
from accounts.models import Cart, CartItems  
from product.models import Product

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email) 

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)
        #user_obj = User.objects.create(...)
        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    


@login_required(login_url='/accounts/login/')
def add_to_cart(request, slug):
    variant = request.GET.get('variant')
    product_obj = get_object_or_404(Product, slug=slug)
    user = request.user
    cart_obj, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItems.objects.create(cart=cart_obj, product=product_obj)

    if variant:
        size_variant = product_obj.size_variant.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()
    return HttpResponseRedirect(request.path_info)

@login_required(login_url='/accounts/login/')
def cart(request):
    user = request.user
    cart_obj = Cart.objects.get(user=user, is_paid=False)
    cart_items = cart_obj.cart_items.all()
    total_price = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity 
        total_price += item.total
        # total_price += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'accounts/cart.html', context)

def cart_items(request , slug):
    user = request.user
    cart_obj = Cart.objects.get(user=user, is_paid=False)
    # cart_item = cart.cart_items.get(cart=cart_obj, product__slug=slug)
    cart_item = CartItems.objects.get(cart=cart_obj, product__slug=slug)
    cart_item.delete()
    return HttpResponseRedirect(request.path_info)

# aaj ka 18jul ka kaam
def cart_view(request):
    cart_items = Cart.objects.all()
    total_price = ...
    # total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'accounts/cart.html', context)

def checkout(request):
    return render(request, 'accounts/checkout.html')