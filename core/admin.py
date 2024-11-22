from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)


# Mix Profile and User Info
class ProfileInline(admin.StackedInline):
    model = Profile


#Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    # fields = ['__all__']
    fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'user_permissions', 'last_login']
    inlines = [ProfileInline]


# Unregister the User model and register again
admin.site.unregister(User)
admin.site.register(User, UserAdmin)