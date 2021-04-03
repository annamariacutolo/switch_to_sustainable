from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewProductForm(forms.Form):
    name = forms.CharField(max_length=200)

class NewProductFormTwo(forms.Form):
    name = forms.CharField(max_length=200)
    text = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)

class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
