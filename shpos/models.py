from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category}'


class Unit(models.Model):
    unit=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.unit}'

class Product(models.Model):
    pid=models.CharField(max_length=15)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    unitperreceipt=models.FloatField()
    buying_price=models.FloatField()
    saleing_price=models.FloatField()
    wholesale_price=models.FloatField()
    alart=models.FloatField()
    discount=models.FloatField()
    img=models.ImageField(upload_to="media/products/")
    point=models.FloatField(null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)
    entry_by=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pid} {self.category} {self.product_name} {self.unit}'
    
