from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import *
import json
from django.contrib import auth
from django.contrib.auth.models import Group, User
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


def login(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        phone_number=data.get('email')
        password=data.get('password')
        user=auth.authenticate(username=phone_number, password=password)
        if user is not None:
            auth.login(request, user)
            # if user.is_superuser:
            refresh = RefreshToken.for_user(request.user)
            # print(user, refresh.access_token)
            return JsonResponse({'success':'Login successfully', 
                                 'name':user.first_name,
                                 'email':user.email,
                                 'access_token':str(refresh.access_token)
                                 })
            # return JsonResponse({'success':'Admin'})
            
            # else:
            #     obj_gp=Group.objects.get(user=user)
            #     return JsonResponse({'success':obj_gp.name})
        else:
            return JsonResponse({"fail":"You don't have access"})
    return JsonResponse({"fail":"You don't have access"})
    


'''
    Response : 
	{
  "user_id": "62d0ff5f8e7b5b3f4e0c8b33",
  "username": "john_doe",
  "email": "john@example.com",
  "joined_date": "2024-07-16",
  "orders": [
    {
      "order_id": "order123",
      "status": "delivered",
      "total": 89.99,
      "order_date": "2024-09-01"
    }
  ]
}


'''
def profile(request):
    obj_user=User.objects.get(id=1)
    orders=My_Orders.objects.filter(cart__user__id=1)#obj_user.
    context={
            "user_id": obj_user.id,
            "username": obj_user.first_name,
            "email": obj_user.email,
            "joined_date": obj_user.date_joined,
            'orders':[ 
                {
                    "order_id": order.order_id,
                    "status": order.order_id,
                    "total": order.cart.total_price(),
                    "order_date": order.date.date()
                } for order in orders

            ]
    }
    return JsonResponse(context)


def sale_all_product(request):
    sps=Saleing_Product.objects.all()
    context={
        'sps':[{'id':sp.id, 'title':sp.title, 'category':sp.category.category, 
                'description':sp.discription,
                'price':sp.price, 
                'rating': sp.product_rating_set.all().aggregate(Avg('rating'))['rating__avg'],
                'images':[img.image.url for img in sp.product_images_set.all()]} for sp in sps]
    }
    return JsonResponse(context)

def sale_one_product(request, id):
    sp=Saleing_Product.objects.get(id=id)
    context={
        'id':sp.id, 
        'title':sp.title, 
        'category':sp.category.category, 
        'description':sp.discription,
        'price':sp.price, 
        'rating': sp.product_rating_set.all().aggregate(Avg('rating'))['rating__avg'],
        'images':[img.image.url for img in sp.product_images_set.all()]

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
    data = json.loads(request.body.decode('utf-8'))
    id=data['product']['id']
    check=Product_Add_TO_Card.objects.filter(user_id=1,#request.user,
                                    product_id=id,
                                    active=True
                                    )
    if check:
        ck=check.last()
        ck.qt+=1
        ck.save()
        return JsonResponse({'message':'Successfully'})
    else:
        Product_Add_TO_Card.objects.create(user_id=1,#request.user,
                                    product_id=id,
                                    )
        return JsonResponse({'message':'Successfully'})
    return JsonResponse({'message':'Pending'})


def add_to_card_list(request):
    print(request.user, 'here ima card list')
    patcs=Product_Add_TO_Card.objects.filter(user_id=1,#request.user, 
                                           active=True)
    context={
        'patcs':[{'img':patc.product.product_images_set.last().image.url if patc.product.product_images_set.all() else "None", 
                  'product_name':patc.product.title,
                  'price':patc.product.price*patc.qt, 
                  'qt':patc.qt, 
                  'id':patc.id,
                  'category':patc.product.category.category}
                     for patc in patcs]
    }
    return JsonResponse(context)

def add_to_card_view(request, id):
    pcs=Product_Add_TO_Card.objects.get(id=id)
    context={
        'pcs':list(pcs)
    }
    return JsonResponse(context)

def add_to_card_remove(request, id):#Product_Add_TO_Card table id
    pcs=Product_Add_TO_Card.objects.get(id=id)
    pcs.active=False
    pcs.save()
    return JsonResponse({})



def card_increase(request, id):#cart/increase/
    pcs=Product_Add_TO_Card.objects.get(id=id)
    pcs.qt += 1
    pcs.save()
    return JsonResponse({})

def card_decrease(request, id):#cart/increase/
    pcs=Product_Add_TO_Card.objects.get(id=id)
    pcs.qt -= 1
    pcs.save()
    return JsonResponse({})



