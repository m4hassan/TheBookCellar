from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
import datetime


# Create Customer Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True) # type: ignore
    phone = models.CharField(max_length=12, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


# Create User Profile automatically when User signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(receiver=create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


# All of our products
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/') 
    is_sales = models.BooleanField(default=False)
    sales_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return self.name


# Customers' orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product.name