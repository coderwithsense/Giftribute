from django import forms 
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

class checkoutForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Megan'
    }))
    surname = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Sharma'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'example@gmail.com'
    }))
    mobile = PhoneNumberField(widget=forms.TextInput(attrs={
        'placeholder': '+91 90123******'
    }))
    apartment_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': '123 Street'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123 Street'
    }))
    country = CountryField()
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Noida'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'State'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zip'
    }))
