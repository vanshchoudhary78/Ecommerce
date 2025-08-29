from django.shortcuts import render

# Create your views here.
# from pydoc import render_doc
# from tkinter import E
from product.models import Product
from accounts.models import Cart, CartItems 
from django.http import HttpResponseRedirect, HttpResponse




def get_product(request , slug):
    try:
        product = Product.objects.get(slug =slug)
        context = {'product' : product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['updated_size'] = size
            context['updated_price'] = price
            # print(price) 
        
        # if request.GET.get('color'):
        #     color = request.GET.get('color')
        #     price = product.get_product_price_by_color(color)
        #     context['updated_color'] = color
        #     context['updated_price'] = price
        #     print(price)
        
        return render(request  , 'product/product.html' , context = context)
    except Exception as e:
        print(f"Error in get_product view: {e}")
        return render(request, 'product/product.html', context={'error': 'Product not found.'})


# def add_to_cart(request , slug):
#     variant = request.GET.get('variant')
#     product = Product.objects.get(slug = slug)
#     user = request.user
#     cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
#     cart_items = CartItem.objects.create(cart = cart , product = product)

#     if variant:
#         variant = request.GET.get('variant')
#         size_variant = product.size_variant.get(size_name = variant)
#         cart_items.size_variant = size_variant
#         cart_item.save()
#     return HttpResponseRedirect(request.path_info)

# def cart(request):
#     user = request.user
#     # cart = Cart.objects.get(user = user , is_paid = False)
#     cart_items = cart.cart_items.all()
#     total_price = 0
#     for item in cart_items:
#         total_price += item.price * item.quantity

#     context = {
#         'cart_items' : cart_items,
#         'total_price' : total_price,
#     }
#     return render(request , 'accounts/cart.html' , context)

# def cart_items(request , slug):
#     user = request.user
#     cart = cart.objects.get(user = user , is_paid = False)
#     cart_item = cart_item.objects.get(cart = cart , product__slug = slug)
#     cart_item.delete()
#     return HttpResponseRedirect(request.path_info)
      