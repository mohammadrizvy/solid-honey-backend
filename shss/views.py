from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import *
import json
import string
import random
from django.contrib import auth
from django.contrib.auth.models import Group, User
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class Product_Calculation:
    def __init__(self, product_id):
        #self.product_id=product_id
        self.obj_sp=product_id#Saleing_Product.objects.get(id=product_id)


    def sale(self):
        total_sale=My_Check_Out.objects.filter(status=True,cart__id=
                                    self.obj_sp.id).aggregate(Sum('qt'))['qt__sum'] or 0
        return total_sale
    
    def buy(self):
        total_buy=Stock_Saleing_Product.objects.filter(sp__id=
                                    self.obj_sp.id).aggregate(Sum('qt'))['qt__sum'] or 0
        return total_buy

    def in_stock(self):
        return self.buy()-self.sale()
    
    def rating(self):
        rating=self.obj_sp.product_rating_set.all().aggregate(Avg('rating'))['rating__avg']
        return rating
    
    def images(self):
        images=[]
        for pi in Product_Images.objects.filter(sp=self.obj_sp):
            try:
                images.append(f"{pi.image.url}")
            except:
                images.append("")

        return images if images else [""]


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
    sps=Saleing_Product.objects.filter(active=True)
    sps_=[]
    for sp in sps:
        pc=Product_Calculation(sp)
        sps_.append({'id':sp.id, 'title':sp.title, 'category':sp.category.category, 
        'description':sp.discription,
        'price':sp.price, 
        'discount':Product_Discount.objects.get(sp=sp).amount if Product_Discount.objects.filter(sp=sp) else  00, 
        'stock': pc.in_stock(),
        'rating': pc.rating(),
        'images':pc.images()#[img.image.url for img in Product_Images.objects.filter(sp=sp)] # sp.product_images_set.all()]
                })
        
    context={
        'sps':sps_
    }
    return JsonResponse(context)

def sale_one_product(request, id):
    sp=Saleing_Product.objects.get(id=id)
    discount=Product_Discount.objects.filter(sp__id=id)
    pc=Product_Calculation(sp)
    context={
        'id':sp.id, 
        'title':sp.title, 
        'category':sp.category.category, 
        'description':sp.discription,
        'price':sp.price, 
        'discount': 00 if not discount else discount.last().amount,
        'stock': pc.in_stock(),
        'rating': pc.rating(),
        'images':pc.images()

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
        obj_group = Group.objects.get(id=2)
        obj_group.user_set.add(new_user)
    return JsonResponse({"successfull":'date entry successfully'})





def add_to_card_entry(request):
    data = json.loads(request.body.decode('utf-8'))
    id=data.get('productId')
    obj_sp=Saleing_Product.objects.get(id=id)
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
        discounts=Product_Discount.objects.filter(sp__id=id)
        Product_Add_TO_Card.objects.create(user_id=1,#request.user,
                                    product_id=id,
                                    amount=obj_sp.price if not discounts 
                                                        else obj_sp.price-discounts.last().amount
                                    )
        return JsonResponse({'message':'Successfully'})
    return JsonResponse({'message':'Pending'})


def add_to_card_list(request):
    patcs=Product_Add_TO_Card.objects.filter(user_id=1,#request.user, 
                                           active=True)
    
    total=0
    for patc in patcs:
        total+=patc.total_price()
    context={
        'patcs':[{'img':patc.product.product_images_set.last().image.url if patc.product.product_images_set.all() else "None", 
                  'product_name':patc.product.title,
                  'price':patc.total_price(),#patc.product.price*patc.qt, 
                  'qt':patc.qt, 
                  'id':patc.id,
                  'category':patc.product.category.category}
                     for patc in patcs],
        'total':total
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


def payment_checkout(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        cards=data.get('cart_id')
        payment_method=data.get('payment_method')
        email=data.get('email')
        phone_number=data.get('phone_number')
        companyname=data.get('companyName')
        shipping_address=data.get('shipping_address')
        order_id = ''.join([random.choice(string.ascii_letters
                + string.digits) for n in range(32)])
        for card in cards:
            obj_sp=Product_Add_TO_Card.objects.get(id=card)
            discount=Product_Discount.objects.filter(id=obj_sp.product.id)
            My_Check_Out.objects.create(
                user_id=1,#request.user.id
                email=email,
                phone_number=phone_number,
                companyname=companyname,
                cart_id=obj_sp.product.id,
                price=obj_sp.product.price if not discount else obj_sp.product.price-discount.last().amount,
                qt=obj_sp.qt,
                order_id=order_id,
                address=shipping_address,
                payment_method=payment_method,
                status=False
            )
            obj_sp.delete()
        return JsonResponse({
                    "order_id": order_id,
                    "message": "Payment processed successfully",
                    "status": "completed"
                    })
    return JsonResponse({})



#*************************************admin ****************************** 

def product_category_entry(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))

        category=data.get('category_name')
    
        new_cat=Web_Category(category=category)
        new_cat.save()
        context={
        "message": "Category added successfully",
        "category_id": new_cat.id
        }
        return JsonResponse(context)
    return JsonResponse({})

def product_categories(request):
    categorys=Web_Category.objects.all()
    context={
        'categories':[{'id':category.id, "name":category.category}
                       for category in categorys]
    }
    return JsonResponse(context)



def create_product(request):
    if request.method=="POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        obj_category=Web_Category.objects.get(category=category)

        new_sp=Saleing_Product(
            category=obj_category,
            title=title,
            discription=description,
            price=price,
            entry_by_id=1
        )
        new_sp.save()
        new_sp.stock_saleing_product_set.create(
            qt=stock
        )
        for i in range(1,5):
            image = request.FILES.get(f'image{i}')
            if not image:
                break
            new_sp.product_images_set.create(
                    image=image
                )
    return JsonResponse({})


def all_users(request):
    users=User.objects.all()#filter(is_staf=False)
    context={
        'users':[{
                  'id':user.id,
                  'name':user.first_name,
                  'email':user.email,
                  'created_date':user.date_joined,
                  'role':Group.objects.filter(user=user).last().name
                                                    } for user in users]
    }

    return JsonResponse(context)

def user_order_details(request, id):
    obj_user=User.objects.get(id=id)
    context={
    'name':obj_user.first_name,
    'orders':[{
                'phone_number':order.phone_number,
                'order_id':order.order_id,
                'address':order.address,
                'accepted':order.accept,
                'deny':order.deny,
                'status':order.status,
                'payment_method':order.payment_method,
                'date':order.date.date(),
                'qt':order.qt,
                'product_name':order.cart.title, 
                'product_price':order.price, 
                'total':order.price*order.qt
            }for order in obj_user.my_check_out_set.all()]
        }
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))


        name=data.get('name')
        email=data.get('email')
        phone_number=data.get('phone_number')
        role=data.get('role')
        obj_user.first_name=name
        obj_user.last_name=phone_number
        obj_user.email=email
        obj_role=Group.objects.get(name=role)
        
        obj_user.groups_set.add(obj_role)


    return JsonResponse(context)




def user_details(request, id):
    obj_user=User.objects.get(id=id)
    obj_groups=Group.objects.get(user=obj_user)
    context={
        'id':obj_user.id,
        'name':obj_user.first_name,
        'email':obj_user.email,
        'phone_number':obj_user.last_name,
        'role':obj_groups.name,
    }
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8'))
        name=data.get('name')
        email=data.get('email')
        phone_number=data.get('phone_number')
        role=data.get('role')
        obj_user.first_name=name
        obj_user.email=email
        obj_user.last_name=phone_number
        obj_role=Group.objects.get(name=role)
        obj_user.groups.clear()
        obj_user.groups.add(obj_role)
        obj_user.save()
        return JsonResponse({'message':"Successfully"})
    return JsonResponse(context)


def user_delete(request, id):
    User.objects.filter(id=id).delete()
    return JsonResponse({'message':"successfully remove"})

# def user_role_update(request, id):
#     # User.objects.filter(id=id).delete()
#     obj
#     return JsonResponse({'message':"successfully remove"})

def product_delete(request, id):
    Saleing_Product.objects.filter(id=id).update(active=False)
    return JsonResponse({'message':"Product delete sucessfully"})

def product_update(request, id):
    obj_sp=Saleing_Product.objects.get(id=id)
    if request.method == 'POST':
        title=request.POST.get('title')
        category=request.POST.get('category')
        obj_cat=Web_Category.objects.get(category=category)
        description=request.POST.get('description')
        price=request.POST.get('price')
        discount=request.POST.get('discount')
        stock=request.POST.get('stock')
        rating=request.POST.get('rating')
        image=request.POST.get('image')
        obj_sp.title=title
        obj_sp.category=obj_cat 
        obj_sp.discription=description
        obj_sp.price=price
        if discount:
            Product_Discount.objects.create(sp=obj_sp,
                                            amount=discount)
        if stock:
            Stock_Saleing_Product.objects.create(sp=obj_sp,
                                                 qt=stock)
        if rating:
            Product_Rating.objects.create(sp=obj_sp,rating=rating)
        if image:
            Product_Images.objects.create(sp=obj_sp, 
                                          image=image)
    return JsonResponse({'message':'successfully'})

def order_list(request):
    users=User.objects.all()
    output=[]
    for user in users:
        output.append({
        'name':user.first_name,
        'orders':[{
                    'phone_number':order.phone_number,
                    'order_id':order.order_id,
                    'address':order.address,
                    'accepted':order.accept,
                    'deny':order.deny,
                    'payment_method':order.payment_method,
                    'status':order.status,
                    'date':order.date.date(),
                    'qt':order.qt,
                    'product_name':order.cart.title, 
                    'product_price':order.price, 
                    'total':order.price*order.qt
                }for order in user.my_check_out_set.all()]
        })
    context={
        'orders':output
    }
    return JsonResponse(context)

def order_accept(request, id):
    My_Check_Out.objects.filter(order_id=id).update(accept=True)
    return JsonResponse({"Message":"Seccessfully "})


def order_deny(request, id):
    My_Check_Out.objects.filter(order_id=id).update(deny=True)
    return JsonResponse({"Message":"Seccessfully "})

def order_reinstate(request, id):
    My_Check_Out.objects.filter(order_id=id).update(deny=False)
    return JsonResponse({"Message":"Seccessfully "})



def order_delivered(request, id):
    My_Check_Out.objects.filter(order_id=id).update(status=True)
    return JsonResponse({"Message":"Seccessfully "})




def order_remove(request, id):
    My_Check_Out.objects.filter(id=id).delete()
    return JsonResponse({"Message":"Seccessfully remove"})

