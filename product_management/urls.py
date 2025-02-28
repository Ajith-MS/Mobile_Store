from django.conf import settings
from django.urls import path
from .views import view_products, view_product_details
from django.conf.urls.static import static
app_name = "product_management"

urlpatterns = [
    path('viewproducts/', view_products, name='viewproducts'),
    path('product_details/<int:id>', view_product_details, name="productdetails"),
]


