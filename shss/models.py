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

'''
    "id": 2,
    "title": "মধু (কাঁচের বোতল)",
    "category": "মধু",
    "description":
      "বিশুদ্ধ মধু একটি কাঁচের বোতলে পরিস্কার ও সুরক্ষিতভাবে সংরক্ষিত। এই মধু প্রাকৃতিক উপাদানে পূর্ণ, যা স্বাস্থ্যকর এবং তাজা স্বাদের নিশ্চিত করে।",
    "price": "500",
    "rating": 4.5,
    "image":
      "https://www.solidhoneybd.com/wp-content/uploads/2020/09/%E0%A7%A7%E0%A7%A6%E0%A7%A6-%E0%A6%97%E0%A7%8D%E0%A6%B0%E0%A6%BE%E0%A6%AE-%E0%A6%AE%E0%A6%A7%E0%A7%81-%E0%A6%95%E0%A6%BE%E0%A6%81%E0%A6%9A%E0%A7%87%E0%A6%B0-%E0%A6%AC%E0%A7%8B%E0%A6%A4%E0%A6%B2-%E0%A5%A4-01-300x225.jpg"
'''