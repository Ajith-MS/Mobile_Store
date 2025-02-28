from django.urls import path
from .views import create_cart, list_cart, delete_cart_item, product_total_price, contact, about, add_to_cart, remove_from_cart, single_product_price      #add_to_cart
app_name = "shopping_cart"

urlpatterns = [
    # path("cart_view/<int:product_id>", add_to_cart, name="addtocart"),
    path("cart_create/<int:id>", create_cart, name="cartcreate"),
    path("cart_list/", list_cart, name="listcart"),
    path("delete_item/<int:id>", delete_cart_item, name="deleteitem"),
    path("total_price/", product_total_price, name="totalprice"),
    path("contact/", contact, name="contactus"),
    path("about/", about, name="aboutpage"),
    path("add_button/<int:id>", add_to_cart, name="addtocart"),
    path("remove_button/<int:id>", remove_from_cart, name="removefromcart"),
    path("single_product_price/<int:id>", single_product_price, name="singleitemprice"),
]
