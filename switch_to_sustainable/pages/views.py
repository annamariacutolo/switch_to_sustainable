from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages, admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Item, Product
from .forms import NewProductForm, NewUserForm
from rest_framework.views import APIView
from rest_framework.response import Response
import re

# Create your views here.
def home(request):
    return render(request, 'home.html')


def products(request):
    product_list = Product.objects.filter(is_approved=True).all()
    items = []
    for product in product_list:
        if not product.item in items:
            items.append(product.item)
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)


# @login_required
def new_product_form(request):
    if request.method == 'GET':
        form = NewProductForm()
        return render(request, 'new_product.html', {'form': form})

    form = NewProductForm(request.POST)
    if not form.is_valid():
        return render(request, 'new_product.html', {'form': form})

    #  should we do .strip() on these ?
    single_use_product = form.cleaned_data['item_name'].lower().capitalize()
    #print("before single use is: " + single_use_product)
    single_use_product = check_for_match(single_use_product)
    replacement = form.cleaned_data['product_name'].lower().capitalize()
    description = form.cleaned_data['description']

    # apparently if checking if it exists then it is more efficient to use .exists()
    if Item.objects.filter(name = single_use_product):
        item = Item.objects.filter(name = single_use_product).first()
        item_id = item.id

        if Product.objects.filter(name = replacement, item_id = item_id, is_approved=True):
            messages.warning(request, f'Product "{replacement}" for {single_use_product} already on our website.')
            return render(request, 'new_product.html', {'form': form})

        if Product.objects.filter(name = replacement, item_id = item_id, is_approved=False):
            messages.warning(request, f'We are already reviewing the product "{replacement}" for use instead of {single_use_product}, but thanks for your suggestion!')
            return render(request, 'new_product.html', {'form': form})

        new_product = Product(name = replacement, description = description, item_id = item_id, is_approved=False)
        new_product.save()
        messages.success(request, f'Thank you for your suggestion: "{replacement}". We will review whether it replaces {single_use_product} and then add it to our website.')
        return render(request, 'new_product.html', {'form': form})
        return HttpResponseRedirect('/new_product')

    item = Item(name = single_use_product)
    item.save()
    item_id = item.id
    new_product = Product(name = replacement, description = description, item_id = item_id)
    new_product.save()
    
    messages.success(request, f'Thank you for your suggestion: "{replacement}".')
    return HttpResponseRedirect('/new_product')


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Registration successful.')
            return HttpResponseRedirect('/accounts/login')
    else:
        form = NewUserForm()

    return render(request, 'new_user.html', {'form': form})


class ListProductsForItems(APIView):
    def get(self, request, format=None):
        item_id = request.GET.get('item_id')
        get_object_or_404(Item, pk=item_id)

        products = [
            {
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
                'price': product.price
            }
            for product in Product.objects.filter(item_id=item_id, is_approved=True)
        ]
        return Response(products)


def check_for_match(string):
    item_list_names = Item.objects.filter().all()
    print(item_list_names)

    string2 = string + "s"

    for item in item_list_names:
        if item.name == string2:
            return item.name
        elif item.name == string:
            return item.name

    return string
def cart(request):
    context = {}
    return render(request, 'cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
