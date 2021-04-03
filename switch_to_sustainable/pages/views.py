from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Item, Product, NewProduct
from .forms import NewProductForm, NewUserForm
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response


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

    product = NewProduct(name=name)
    product.save()

    return HttpResponse('Thank you for your suggestion.')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = NewUserForm()

    return render(request, 'new_user.html', {'form': form})


class ListProductsForItems(APIView):
    def get(self, request, format=None):
        item_id = request.GET.get('item_id')
        get_object_or_404(Item, pk=item_id)

        products = [
            {
                'text': product.text,
                'description': product.description,
                'stock': product.stock,
                'price': product.price
            }
            for product in Product.objects.filter(item_id=item_id)
        ]
        print(products)
        return Response(products)
