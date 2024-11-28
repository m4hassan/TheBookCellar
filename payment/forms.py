from django import forms
from .models import ShippingAddress

class ShippingInfoForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
    shipping_email = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shipping_phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=True)
    shipping_address1 = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=True)
    shipping_address2 = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
    shipping_city = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    shipping_state = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    shipping_zipcode = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}), required=False)
    shipping_country = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['shipping_user']


class PaymentForm(forms.Form):
    card_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}), required=True)
    card_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiry Date'}), required=True)
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV'}), required=True)
    card_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 1'}), required=True)
    card_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 2'}), required=False)
    card_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing City'}), required=True)
    card_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing State'}), required=False)
    card_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Zip Code'}), required=False)
    card_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Country'}), required=True)