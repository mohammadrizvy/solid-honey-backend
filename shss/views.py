from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import *
import json
from django.contrib import auth
from django.contrib.auth.models import Group, User
# Create your views here.
from .models import *


def login(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        phone_number=data.get('email')
        password=data.get('password')
        user=auth.authenticate(username=phone_number, password=password)
        if user is not None:
            auth.login(request, user)

            # if user.is_superuser:
            #     return JsonResponse({'success':'Admin'})
            # else:
            #     obj_gp=Group.objects.get(user=user)
            #     return JsonResponse({'success':obj_gp.name})
        else:
            return JsonResponse({"fail":"You don't have access"})
    return JsonResponse({"fail":"You don't have access"})
    



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
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        name=data.get('name')
        email=data.get('email')
        password=data.get('password')
        new_user=User(username=email, email=email, first_name=name)
        new_user.set_password(password)
        new_user.save()
    return JsonResponse({"successfull":'date entry successfully'})





def add_to_card_entry(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        product_id= data.get('product_id')
        qt= data.get('qt')
        Product_Add_TO_Card.objects.create(user=request.user,
                                           product_id=product_id,
                                           qt=qt)
        return JsonResponse({'message':'succesfully entry'})
    return JsonResponse({'message':'Pending'})


def add_to_card_list(request):
    pcs=Product_Add_TO_Card.objects.filter(user=request.user, 
                                           active=True)
    context={
        'pcs':list(pcs.values())
    }
    return JsonResponse(context)


def add_to_card_view(request, id):
    pcs=Product_Add_TO_Card.objects.filter(user=request.user, 
                                           active=True)
    context={
        'pcs':list(pcs.values())
    }
    return JsonResponse(context)