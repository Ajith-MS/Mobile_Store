from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='uploaded_profile_pictures/', blank=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=False)
    address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username