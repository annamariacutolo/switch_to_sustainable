from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewProductForm(forms.Form):
    item_name = forms.CharField(max_length=200)
    product_name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=7)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "street-address", "city", "state", "postcode", "phone_number"]



# class Shipping(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     street_address = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     postcode = models.CharField(max_length=20)

#     def __str__(self):
#         return self.address