from django.db import models

# from django.contrib.auth.models import User
# from ..prod.models import Products
# from ..product_management.models import Products
from product_management.models import Products
from user_authentication.models import CustomUser

# Create your models here.
# from ..product_management.models import Products


class CartProduct(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

