"""
URL configuration for SHSSSHPOS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("all/product", views.sale_all_product, name="sale_all_product"),
    path("all/product/<str:id>", views.sale_one_product, name="sale_one_product"),
    path("singup", views.create_new_account, name="create_new_account"),
    path("login/", views.login, name="login"),
    path("cart/entry/", views.add_to_card_entry, name="add_to_card_entry"),
    path("cart/list/", views.add_to_card_list, name="add_to_card_list"),
    path("cart/list/<str:id>/", views.add_to_card_view, name="add_to_card_view"),
    path("cart/remove/<str:id>/", views.add_to_card_remove, name="add_to_card_remove"),
    path("cart/increase/<str:id>/", views.card_increase, name="card_increase"),
    path("cart/decrease/<str:id>/", views.card_decrease, name="card_decrease"),
    path("payment/checkout", views.payment_checkout, name="payment_checkout"),


# **************************admin********************
    path("product/categories", views.product_categories, name="product_categories"),
    path("product/category/entry", views.product_category_entry, name="product_category_entry"),
    path("add/product", views.create_product, name="create_product"),
    path("admin/product/remove/<str:id>", views.product_delete, name="product_delete"),
    path("all/users/", views.all_users, name="all_users"),


]

