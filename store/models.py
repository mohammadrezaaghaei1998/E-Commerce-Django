from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import secrets
import string




CART_SESSION_ID = 'cart'


# Create your models here.


class Categories (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

    
class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    
    def __str__(self):
        return self.name


class Filter_price(models.Model):
    FİLTER_PRİCE = (
        ('50 to 100' , '50 to 100'),
        ('100 to 200' , '100 to 200'),
        ('200 to 300' , '200 to 300'),
        ('300 to 400' , '300 to 400'),
        ('400 to 500' , '400 to 500'),
        ('500 to 600' , '500 to 600'),
        ('600 to 700' , '600 to 700'),
        ('700 to 800' , '700 to 800'),

    )
    price = models.CharField(choices=FİLTER_PRİCE,max_length=200)


    def __str__(self):
        return self.price
    


    
class Product(models.Model):
    
    CONDİTİON = (('New','New'),('Old','Old'))
    STOCK = ('İN STOCK','İN STOCK'),('OUT OF STOCK','OUT OF STOCK')
    STATUS = ('Publish','Publish'),('Draft','Draft')


    unique_id = models.CharField(unique=True, max_length=200, null=True,blank=False)
    image = models.ImageField(upload_to='product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDİTİON,max_length=100)
    information = models.TextField()
    description = models.TextField()
    stock = models.CharField(choices=STOCK,max_length=200)
    status = models.CharField(choices=STATUS,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_price,on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args,**kwargs)
    

    
    def __str__(self):
        return self.name


   
    

class Images(models.Model):
    image = models.ImageField(upload_to='product_images/img')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)



class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

    

class Contact_us(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self): 
        return f"{self.name} - {self.email}"








class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"Cart for {self.user.username}"
    

  

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def get_total_item_price(self):
        return self.quantity * self.product.price
    

    def get_total_item_quantity(self):
        return self.quantity




class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='userinfo', on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state = models.TextField()
    street = models.CharField(max_length=100)
    zipcode = models.PositiveIntegerField(default=0) 
    email = models.EmailField()
    phone_number = models.PositiveIntegerField(default=0)
    cart_item = models.ForeignKey(CartItem , on_delete=models.CASCADE, default=None, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100,default=None,null=True)

    
    def __str__(self):
        return f"User Information for {self.user.username}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=None, null=True)



    def __str__(self):
        cart_items = ', '.join(cart_item.product.name for cart_item in self.cart.cartitem_set.all())
        return f"Order for {self.user_info.get_full_name()} - Cart Items: {cart_items}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,default=None,null=True)
    payment_method = models.CharField(max_length=20, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    card_number = models.CharField(max_length=16, verbose_name='Credit Card Number')
    card_cvv = models.CharField(max_length=4, verbose_name='Card CVV')
    exp_month = models.CharField(max_length=2, choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)], verbose_name='Expiration Month')
    exp_year = models.CharField(max_length=4, choices=[(str(i), str(i)) for i in range(2023, 2030)], verbose_name='Expiration Year')
    reference_code = models.CharField(max_length=8, unique=True, blank=True, null=True, editable=False)


    

    def __str__(self):
        user_full_name = self.order.user_info.get_full_name() if self.order and self.order.user_info else "Unknown User"
        
        cart_items_info = []
        if self.order and self.order.cart:
            for cart_item in self.order.cart.cartitem_set.all():
                item_info = f"Product: {cart_item.product.name} ({cart_item.quantity} units) - Price: ${cart_item.get_total_item_price()}"
                cart_items_info.append(item_info)
        cart_items = ', '.join(cart_items_info) if cart_items_info else "No Items"
        
        return f"Payment for {user_full_name} - Payment Method: {self.payment_method} - Cart Items: {cart_items}"



    def generate_reference_code(self):
        self.reference_code = secrets.token_hex(4).upper()
        self.save()





class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)







 