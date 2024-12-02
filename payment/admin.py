from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.unregister(ShippingAddress)
admin.site.register(ShippingAddress)

admin.site.register(Order)
admin.site.register(OrderItem)

# mix order and order items info
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]

admin.site.unregister(Order)
admin.site.unregister(OrderItem)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)