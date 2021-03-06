from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)  

    def __str__(self):
        return self.name


class Product(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    is_approved = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
    def customer_profile(sender, instance, created, **kwargs):
        user = instance
        if created:
            customer = Customer(user=user)
            customer.save()
   

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField('OrderProduct', related_name='orderproducts')
    order_date = models.DateTimeField(null=True)
    order_id = models.CharField(max_length=30, null=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([product.get_total for product in orderproducts])
        return total

    @property
    def get_cart_items(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([product.quantity for product in orderproducts])
        return total


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.street_address