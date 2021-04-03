from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.text

class NewProduct(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
        