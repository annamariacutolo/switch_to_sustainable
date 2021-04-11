from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages, admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Item, Product, OrderProduct, Order, Customer, Shipping
from .forms import NewProductForm, NewUserForm, CheckoutForm
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import datetime
from ukpostcodeutils import validation
from django.forms import ValidationError


def home(request):
    return render(request, 'home.html')


def products(request):
    if request.method == 'GET':
        items = Item.objects.filter(is_approved=True)
        item_id = request.GET.get('item_id')  
        context = {'item_id': item_id, 'items':items}
    
    return render(request, 'products.html', context)


@login_required
def new_product_form(request):
    if request.method == 'GET':
        form = NewProductForm()
        return render(request, 'new_product.html', {'form': form})

    form = NewProductForm(request.POST)
    if not form.is_valid():
        return render(request, 'new_product.html', {'form': form})

    single_use_product = form.cleaned_data['item_name'].lower().capitalize().strip()
    single_use_product = check_for_match(single_use_product)
    replacement = form.cleaned_data['product_name'].lower().capitalize().strip()
    description = form.cleaned_data['description'].strip()

    if Item.objects.filter(name = single_use_product).exists():
        item = Item.objects.filter(name = single_use_product).first()
        item_id = item.id

        if Product.objects.filter(name = replacement, item_id = item_id, is_approved=True).exists():
            messages.warning(request, f'Product "{replacement}" for {single_use_product} already on our website.')
            return render(request, 'new_product.html', {'form': form})

        if Product.objects.filter(name = replacement, item_id = item_id, is_approved=False).exists():
            messages.warning(request, f'We are already reviewing the product "{replacement}" for use instead of {single_use_product}, but thanks for your suggestion!')
            return render(request, 'new_product.html', {'form': form})

        new_product = Product(name = replacement, description = description, item_id = item_id, is_approved=False)
        new_product.save()
        messages.success(request, f'Thank you for your suggestion: "{replacement}". We will review whether it replaces {single_use_product} and then add it to our website.')
        return render(request, 'new_product.html', {'form': form})

    item = Item(name = single_use_product, is_approved = False)
    item.save()
    item_id = item.id
    new_product = Product(name = replacement, description = description, item_id = item_id, is_approved = False)
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

'''
class ListProductsForItems(APIView):
    def get(self, request, format=None):
        item_id = request.GET.get('item_id')
        get_object_or_404(Item, pk=item_id)

        products = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
                'price': product.price
            }
            for product in Product.objects.filter(item_id=item_id, is_approved=True)
        ]
        return Response(products)
'''

def check_for_match(string):
    item_list_names = Item.objects.filter().all()

    string2 = string + "s"

    for item in item_list_names:
        if item.name == string2:
            return item.name
        elif item.name == string:
            return item.name

    return string


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        products = order.orderproduct_set.all()

        for product in products:
            order.products.add(product)

        context = {'products': products, 'order': order}
        return render(request, 'cart.html', context)
    else:
        messages.warning(request, 'Please log in to make a purchase. (From cart)')
        return HttpResponseRedirect('/accounts/login')

def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    products = order.orderproduct_set.all()
    cartProducts = order.get_cart_items
    
    if request.method == 'GET':
        form = CheckoutForm()
        context = {'products': products, 'order': order, 'cartProducts': cartProducts, 'form': form}
        return render(request, 'checkout.html', context)

    form = CheckoutForm(request.POST)
    context = {'products': products, 'order': order, 'cartProducts': cartProducts, 'form': form}
    if not form.is_valid():
        return render(request, 'checkout.html', context)
    
    name = form.cleaned_data['name'].strip()
    street_address = form.cleaned_data['street_address'].strip()
    city = form.cleaned_data['city'].strip()
    state = form.cleaned_data['state'].strip()
    postcode = form.cleaned_data['postcode'].strip().upper()
    phone_number = form.cleaned_data['phone_number'].strip()
    postcode = ''.join(postcode.split())

    if len(phone_number) != 11:
        messages.warning(request, 'Please enter a valid phone number')
        return render(request, 'checkout.html', context)

    if not phone_number.isdecimal():
        messages.warning(request, 'Please enter a valid phone number')
        return render(request, 'checkout.html', context)

    if not validation.is_valid_postcode(postcode):
        messages.warning(request, 'Please enter a valid postcode')
        return render(request, 'checkout.html', context)

    order.order_date = datetime.datetime.today().strftime('%Y-%m-%d')
    order.order_id = datetime.datetime.now().timestamp()
    order.complete = True
    order.save()

    new_shipping = Shipping(customer = customer, order = order, street_address = street_address, 
    city = city, state = state, postcode = postcode, phone_number = phone_number)
    new_shipping.save()

    messages.success(request, f'Thanks for your order')
    return HttpResponseRedirect('/')


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print('action:', action, 'product:', productId, 'product name:', product)
    orderProduct, created = OrderProduct.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        print(product.stock)
        if product.stock>0:
            orderProduct.quantity = (orderProduct.quantity + 1)
            product.stock -= 1
        else:
            messages.warning(request, 'Sorry, this product is out of stock')
            return JsonResponse('Error', safe=False, status=400)
        print(product.stock)
        
    elif action == 'remove':
        if orderProduct.quantity > 0:
            orderProduct.quantity = (orderProduct.quantity - 1)
            product.stock += 1
        else:
            messages.warning(request, 'Sorry, the product is unavailable')
            return JsonResponse('Error', safe=False, status=400)
    if orderProduct.quantity <= 0:
        orderProduct.delete()   
         
    orderProduct.save()
    product.save()

    dict = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
                'price': product.price
            }

    return JsonResponse(dict, safe=False)


def eco_shop(request):
    item_id = request.GET.get('item_id')
    items = Item.objects.filter(is_approved=True)
    products = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'stock': product.stock,
            'price': product.price
        }
        for product in Product.objects.filter(item_id=item_id, is_approved=True)
    ]

    context = {'item_id': item_id, 'products': products, 'items':items}

    return render(request, 'eco_shop.html', context)

