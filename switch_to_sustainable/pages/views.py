from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Item, Product, NewProduct
from .forms import NewProductForm, NewUserForm, NewProductFormTwo
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
    if request.method == 'GET':
        form = NewProductForm()
        return render(request, 'new_product.html', {'form': form})

    form = NewProductForm(request.POST)
    if not form.is_valid():
        return render(request, 'new_product.html', {'form': form})

    name = form.cleaned_data['name']

    if Product.objects.filter(name=name):
        messages.warning(request, f'Product "{name}" already on our website.')
        return render(request, 'new_product.html', {'form': form})

    product = NewProduct(name=name)
    product.save()
    
    messages.success(request, f'Thank you for your suggestion: "{name}".')
    return HttpResponseRedirect('/new_product')


def new_product_form_two(request):
    # i think this methods only works with GET here, if its post i think it keeps looping round this 
    # and continually just displaying the form on the page
    if request.method == 'GET':
        form = NewProductFormTwo()
        return render(request, 'new_product_two.html', {'form': form})

    form = NewProductFormTwo(request.POST)
    if not form.is_valid():
        return render(request, 'new_product_two.html', {'form': form})
    
    # thinking if we could somehow get the id using this if we create a new instace of Item first?
    single_use_product = form.cleaned_data['name']
    # information for adding a new product
    replacement = form.cleaned_data['product_name']
    description = form.cleaned_data['description']

    # adding the sustainable product to the database
    new_product = Product(name = replacement, description = description, item_id = 1)
    new_product.save()

    return HttpResponse('Thank you for your suggestion.')

   


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
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
            for product in Product.objects.filter(item_id=item_id)
        ]
        return Response(products)
