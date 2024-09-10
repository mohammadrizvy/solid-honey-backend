from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.
from .models import *

'''
"_id": "1",
"barcode": "82736582934",
"category": "মধু",
"productName": "খাঁটি মধু",
"unitPerReceipt": 5,
"unit": "Jar",
"costPrice": "250.00",
"sellingPrice": "300.00",
"wholesalePrice": "280.00",
"stockAlert": "15",
"discount": "10",
"point": "20",
"image": null
'''

def products_entry(request):
    if request.method=='POST':
        datas = json.loads(request.body.decode('utf-8'))
        for data in datas:
            pid=data.get('password')
            category=data.get('category')
            obj_category=Category.objects.get(category=category)
            productName=data.get('productName')
            unitPerReceipt=data.get('unitPerReceipt')
            unit=data.get('unit')
            obj_unit=Unit.objects.get(unit=unit)
            costPrice=data.get('costPrice')
            sellingPrice=data.get('sellingPrice')
            wholesalePrice=data.get('wholesalePrice')
            stockAlert=data.get('stockAlert')
            discount=data.get('discount')
            point=data.get('point')
            image=data.get('image')
            new_p=Product(
                pid=pid,
                category=obj_category,
                product_name=productName,
                unit=obj_unit,
                unitperreceipt=unitPerReceipt,
                buying_price=costPrice,
                saleing_price=sellingPrice,
                wholesale_price=wholesalePrice,
                alart=stockAlert,
                discount=discount,
                img=image,
                point=point
                )
            new_p.save()

    return JsonResponse({})
