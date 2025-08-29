from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from product.models import Product

# Create your models here.
# class Profile(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     profile_image = models.ImageField(upload_to='profile')
#     phone_number = models.CharField(max_length=15)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     zip_code = models.CharField(max_length=10)

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        try:
            cart = self.user.carts  # This is already the Cart instance
            if not cart.is_paid:
                cart_items = cart.cart_items.all()
                return cart_items.count()
            else:
                return 0
        except Cart.DoesNotExist:
            return 0

class Cart(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="carts")
    total_price = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    def __str__(self) -> str:
        return str(self.user.username)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name="cart_items")
    product = models.ForeignKey("product.Product" , on_delete=models.CASCADE , related_name="cart_items")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.product.product_name)
    


    

@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)