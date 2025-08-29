from django.urls import path
from product.views import get_product


urlpatterns = [
    
   
    path('<slug>/' , get_product , name="get_product"),
    # path('' , get_product , name="get_product")
    path('product/<slug>/' , get_product , name="get_product"),
    # path('<slug:slug>/', get_product, name='get_product'),  # Example URL pattern for product detail page

]
