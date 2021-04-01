from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    description = models.CharField()
    stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.text