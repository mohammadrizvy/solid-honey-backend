from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import *
import json
# Create your views here.
from .models import *

def sale_all_product(request):
    sps=Saleing_Product.objects.all()
    context={
        'sps':[{'id':sp.id, 'title':sp.title, 'category':sp.category.category, 'description':sp.discription,
                'price':sp.price, 
                'rating': sp.product_rating_set.all().aggregate(Avg('rating'))['rating__avg'],
                'images':[img.image.url for img in sp.product_images_set.all()]} for sp in sps]
    }
    return JsonResponse(context)

# name, number/email, password
def create_new_account(request):
    print('called success')
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        name=data.get('name')
        email=data.get('email')
        password=data.get('password')
        new_user=User(username=email, email=email, first_name=name)
        new_user.set_password(password)
        new_user.save()
    return JsonResponse({"successfull":'date entry successfully'})
