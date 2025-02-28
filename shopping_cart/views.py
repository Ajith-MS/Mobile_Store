from django.shortcuts import render, redirect, HttpResponse
from product_management.models import Products
from .models import CartProduct
from django.contrib.auth.decorators import login_required
from user_authentication.models import CustomUser
from .forms import ContactForm

# Create your views here.


@login_required(login_url="user_authentication:userlogin")
def create_cart(request, id):
    product = Products.objects.get(id=id)
    product_quantity = 1
    CartProduct.objects.create(product_id=product, user=request.user, product_quantity=product_quantity)
    return redirect("shopping_cart:listcart")


@login_required(login_url="user_authentication:userlogin")
def list_cart(request):
    cart_products = CartProduct.objects.all()
    return render(request, "cart_view.html", {"products": cart_products})


@login_required(login_url="user_authentication:userlogin")
def add_to_cart(request, id):
    cart_product = CartProduct.objects.get(id=id)
    cart_product.product_quantity += 1  # Increase the quantity
    cart_product.save()  # Save the updated quantity
    return redirect("shopping_cart:listcart")


@login_required(login_url="user_authentication:userlogin")
def remove_from_cart(request, id):
    cart_product = CartProduct.objects.get(id=id)
    if cart_product.product_quantity > 1:
        cart_product.product_quantity -= 1  # Decrease quantity by one
        print(cart_product.product_id.product_price,"??????????????????????????????????????????")
        cart_product.save()
    else:
        cart_product.delete()  # If quantity reaches zero, remove from cart
    return redirect("shopping_cart:listcart")


@login_required(login_url="user_authentication:userlogin")
def delete_cart_item(request, id):
    cart_product = CartProduct.objects.get(id=id)
    cart_product.delete()
    return redirect("shopping_cart:listcart")


@login_required(login_url="user_authentication:userlogin")
def product_total_price(request):
    total_price = 0
    cart_products = CartProduct.objects.all()
    for product in cart_products:
        price = product.product_id.product_price
        quantity = product.product_quantity
        total_price = total_price+(quantity*price)
    return render(request, "total_price.html", {"total": total_price})


def single_product_price(request, id):
    product = CartProduct.objects.get(id=id)
    total_price = product.product_quantity * product.product_id.product_price
    return render(request, "total_price.html", {"total": total_price})


def contact(request):
    form = ContactForm()
    context_data = {"form": form}
    return render(request, "contact.html", context_data)


def about(request):
    return render(request, "about.html")
