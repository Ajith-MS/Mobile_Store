from django.shortcuts import render
from .models import Products
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
# Create your views here.


@login_required(login_url="user_authentication:userlogin")
def view_products(request):
    products = Products.objects.all()
    return render(request, "product_view.html", {"products": products})


@login_required(login_url="user_authentication:userlogin")
def view_product_details(request, id):
    product = Products.objects.get(id=id)
    return render(request, "product_details.html", {"product": product})
