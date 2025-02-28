from django.contrib import admin
from .models import CartProduct
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ("product_id", "product_quantity", "user")
admin.site.register(CartProduct, CartAdmin)
