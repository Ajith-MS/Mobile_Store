from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

admin.site.register(CustomUser)


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("phone_number", "address")
#
#
# admin.site.register(CustomUserAdmin, CustomUser)

