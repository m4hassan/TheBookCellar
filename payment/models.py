from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Shipping Address - {str(self.user.id)}'
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'    
