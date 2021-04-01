from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item, Product


# Create your views here.
def index(request):
    return render(request, 'index.html')

def books_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'books.html', context)
