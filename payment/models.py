from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
