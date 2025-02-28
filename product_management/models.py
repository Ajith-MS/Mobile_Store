from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=50, blank=False, null=False)
    product_description = models.TextField(max_length=1000, null=True, blank=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=10, blank=False)
    product_image = models.ImageField(upload_to='added_images/', null=True, blank=True)
    product_stock_availability = models.PositiveIntegerField(default=0)
    product_tag = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "Products"