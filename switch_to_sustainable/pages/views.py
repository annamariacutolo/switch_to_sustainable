from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Item, Product
from .forms import NewProductForm, NewUserForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def products(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)

def new_product_form(request):
    if request.method == 'POST':
        form = NewProductForm()
        return render(request, 'new_product.html', {'form': form})

    form = NewProductForm(request.POST)
    if not form.is_valid():
        return render(request, 'new_product.html', {'form': form})

    name = form.cleaned_data['name']

    if Product.objects.filter(name=name):
        messages.warning(request, f'Product {name} already on our website')
        return render(request, 'new_product.html', {'form': form})

    # product = Product(name=name)
    # product.save()

    return HttpResponseRedirect('products')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = NewUserForm()

    return render(request, 'new_user.html', {'form': form})
