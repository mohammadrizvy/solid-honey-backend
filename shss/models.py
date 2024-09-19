from django.db import models
from shpos.models import Category, User

# Create your models here.
class Saleing_Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    discription=models.TextField(max_length=2500)
    price=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    entry_by=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.category} {self.title}'


class Product_Images(models.Model):
    sp=models.ForeignKey(Saleing_Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="meida/product/images")

class Product_Rating(models.Model):
    sp=models.ForeignKey(Saleing_Product, on_delete=models.CASCADE)
    rating=models.FloatField()

    def __str__(self):
        return f'{self.sp} {self.rating}'

class Product_Add_TO_Card(models.Model):
    product=models.ForeignKey(Saleing_Product, on_delete=models.CASCADE)
    qt=models.FloatField(default=1,null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    '''
    if active then add to card are active
    else false
    '''

    def total_price(self):
        return self.product.price*self.qt
         

    def __str__(self):
        return f'{self.product} {self.qt} {self.user}'
    

class My_Orders(models.Model):
    cart=models.OneToOneField(Product_Add_TO_Card, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(max_length=12)
    status=models.BooleanField(default=False)
    '''
    if false then pending
    else delivarid
    '''

    def __str__(self):
        return f'{self.cart} {self.date} {self.order_id}'