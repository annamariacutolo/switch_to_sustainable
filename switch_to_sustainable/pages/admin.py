from django.contrib import admin
from .models import Item, Product, NewProduct

# Register your models here.
admin.site.register(Item)
admin.site.register(Product)
admin.site.register(NewProduct)