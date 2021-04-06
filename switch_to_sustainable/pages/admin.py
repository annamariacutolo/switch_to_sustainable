from django.contrib import admin
from .models import Item, Product, OrderProduct, Order, Customer, Shipping


admin.site.register(Item)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Shipping)
