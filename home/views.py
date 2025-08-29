from django.shortcuts import render
from product.models import Product



def index(request):

    context = {'product' : Product.objects.all()}
    return render(request , 'index.html' , context)