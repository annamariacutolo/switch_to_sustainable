from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages, admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Item, Product
from .forms import NewProductForm, NewUserForm
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def home(request):
    return render(request, 'home.html')

def products(request):
    product_list = Product.objects.filter(is_approved=True)
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

    single_use_product = form.cleaned_data['item_name'].lower().capitalize()
    replacement = form.cleaned_data['product_name']
    description = form.cleaned_data['description']

    if Item.objects.filter(name = single_use_product):
        item = Item.objects.filter(name = single_use_product).first()
        item_id = item.id

        if Product.objects.filter(name = replacement, item_id = item_id, is_approved=True):
            messages.warning(request, f'Product "{replacement}" for {single_use_product} already on our website.')
            return render(request, 'new_product.html', {'form': form})

        new_product = Product(name = replacement, description = description, item_id = item_id)
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

# @login_required
# def new_product_form_two(request):
#     # i think this methods only works with GET here, if its post i think it keeps looping round this 
#     # and continually just displaying the form on the page
#     if request.method == 'GET':
#         form = NewProductFormTwo()
#         return render(request, 'new_product_two.html', {'form': form})

#     form = NewProductFormTwo(request.POST)
#     if not form.is_valid():
#         return render(request, 'new_product_two.html', {'form': form})
    
#     # thinking if we could somehow get the id using this if we create a new instace of Item first?
#     single_use_product = form.cleaned_data['name']
#     # information for adding a new product
#     replacement = form.cleaned_data['product_name']
#     description = form.cleaned_data['description']

#     if Item.objects.filter(name = single_use_product):
#         # get id of the item that the product could be used instead of
#         item = Item.objects.filter(name = single_use_product).first()
#         item_id = item.id

#         # check if product already exists under that item, otherwise add it
#         if Product.objects.filter(name = replacement, item_id = item_id):
#             messages.warning(request, f'Product "{replacement}" for {single_use_product} already on our website.')
#             return render(request, 'new_product_two.html', {'form': form})

#         # adding product for the item which already exists on the databases
#         new_product = Product(name = replacement, description = description, item_id = item_id)
#         new_product.save()
#         messages.success(request, f'Thank you for your suggestion: "{replacement}", we will review whether it replaces {single_use_product} and then add it to our database.')
#         return render(request, 'new_product_two.html', {'form': form})

#     # adding the sustainable product to the database if the item doesn't already exist
#     # make new instance of item since it doesn't exist
#     item = Item(name = single_use_product)
#     item.save()
#     item_id = item.id
#     new_product = Product(name = replacement, description = description, item_id = item_id)
#     new_product.save()

#     return HttpResponse('Thank you for your suggestion we will review it then add it to our database.')

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
            for product in Product.objects.filter(item_id=item_id)
        ]
        #print(products)
        return Response(products)
