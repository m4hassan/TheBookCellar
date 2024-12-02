from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name="checkout"),
    path('billing_info/', views.billing_info, name="billing_info"),
    path('process_order/', views.process_order, name="process_order"),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('shipped_dashboard/', views.shipped_dashboard, name="shipped_dashboard"),
    path('not_shipped_dashboard/', views.not_shipped_dashboard, name="not_shipped_dashboard"),
    path('orders/<int:pk>', views.orders , name="orders"),
]