from django.db import models
from shpos.models import  User

class Web_Category(models.Model):
    category=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category}'

# Create your models here.
class Saleing_Product(models.Model):
    category=models.ForeignKey(Web_Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    discription=models.TextField(max_length=2500)
    price=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    entry_by=models.ForeignKey(User, on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    '''
    true mean sale able products
    false meaning not sale able products
    '''
    def __str__(self):
        return f'{self.category} {self.title}'


class Product_Discount(models.Model):
    sp=models.OneToOneField(Saleing_Product, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    amount=models.FloatField()
    active=models.BooleanField(default=True)
    '''
        if active then discount aviable else not
    '''

    def ratio(self):
        ratio=self.amount*100/self.ap.price
        return ratio

class Stock_Saleing_Product(models.Model):
    sp=models.ForeignKey(Saleing_Product, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    qt=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.sp} {self.date} {self.qt}'


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
    amount=models.FloatField(null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    '''
    if active then add to card are active
    else false
    '''

    def total_price(self):
        return self.amount*self.qt
         

    def __str__(self):
        return f'{self.product} {self.qt} {self.user}'
    

class My_Check_Out(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart=models.ForeignKey(Saleing_Product, on_delete=models.CASCADE)
    price=models.FloatField(null=True, blank=True)
    qt=models.FloatField()

    address=models.TextField(max_length=500)
    phone_number=models.CharField(max_length=40, null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    companyname=models.CharField(max_length=250, null=True, blank=True)
    payment_method=models.CharField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(max_length=40)
    accept=models.BooleanField(default=False)
    deny=models.BooleanField(default=False)

    '''
    if true then order accepted by admin
    else dainy the order
    '''
    status=models.BooleanField(default=False)
    '''
    if false then pending
    else delivarid
    '''

    def total_amount(self):
        return self.qt * self.price
    

    def __str__(self):
        return f'{self.cart} {self.date} {self.order_id}'