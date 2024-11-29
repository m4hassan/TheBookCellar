from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from core.models import Product



class ShippingAddress(models.Model):
    shipping_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=12)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Shipping Address - {str(self.shipping_user.id)}'
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'    

# Create a user shipping address by default when user signs up
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        shipping_address = ShippingAddress(shipping_user=instance)
        shipping_address.save()

post_save.connect(create_shipping_address, sender=User)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    shipping_address = models.TextField(max_length=500)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.user:
            return f'User {self.user.id} Order {str(self.id)}'
        else:
            return f'User {self.user} Order {str(self.id)}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'