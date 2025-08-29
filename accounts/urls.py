from django.urls import path
from accounts.views import login_page,register_page , add_to_cart , cart , activate_email
from accounts.views import cart_view, checkout

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   # path('cart/' , cart , name="cart"),
   path('add-to-cart/<slug>/' , add_to_cart , name="add_to_cart"),
   # path('add-to-cart/<slug:slug>/', add_to_cart, name="add_to_cart"),
   path('remove-from-cart/<slug>/' , add_to_cart , name="remove_from_cart"),
   path('cart/', cart_view, name='cart'),
   path('checkout/', checkout , name='checkout'),

]
