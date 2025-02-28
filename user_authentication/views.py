from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from user_authentication.models import CustomUser


def user_registration(request):
    User = get_user_model()
    all_user = User.objects.values_list("username", flat=True)
    all_numbers = CustomUser.objects.values_list("phone_number", flat=True)
    all_emails = User.objects.values_list("email", flat=True)
    if request.method == 'POST':
        user_name = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phonenumber")
        address = request.POST.get("address")
        profile_picture = request.FILES.get("profilepicture")
        confirm_password = request.POST.get("confirmpassword")

        if user_name in all_user:
            messages.error(request, "Username already exists!!")
        elif email in all_emails:
            messages.error(request, "Email already exists!!")
        elif phone_number in all_numbers:
            messages.error(request, "Phonenumber already exists!!")
        elif password != confirm_password:
            messages.error(request, "Password and confirm password doesn't match!!")
        else:
            User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, email=email,password=password, phone_number=phone_number, profile_picture=profile_picture, address=address)
            messages.success(request, "Account created successfully")
            return redirect('user_authentication:userlogin')
    return render(request, "registration.html")


def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=user_name, password=password)
        if user:
            login(request, user)
            return redirect("product_management:viewproducts")
        else:
            messages.error(request, "Incorrect User Name or Password ")
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("user_authentication:userlogin")


def user_view(request):
    user = request.user
    return render(request, "view_user.html", {"user": user})


def user_update(request):
    user = request.user
    if request.method == 'POST':
        profile_picture = request.FILES.get("profilepicture")
        user_name = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        phone_number = request.POST.get("phonenumber")

        if profile_picture:
            user.profile_picture = profile_picture
        else:
            pass
        user.username = user_name
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.phone_number = phone_number
        user.save()
        return redirect("user_authentication:userview")

    return render(request, "user_update.html")
