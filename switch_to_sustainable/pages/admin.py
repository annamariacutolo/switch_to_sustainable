from django.contrib import admin
from .models import Item, Product, OrderProduct, Order


# Register your models here.
admin.site.register(Item)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
