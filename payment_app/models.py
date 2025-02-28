from django.db import models
from user_authentication.models import CustomUser
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    payment_method = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_complete = models.BooleanField(default=False)
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True, unique=True)  # Store PayPal transaction ID

    def __str__(self):
        return f"{self.user.username} - {self.total_amount} - {'Paid' if self.payment_complete else 'Pending'}"
