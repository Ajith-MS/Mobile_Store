from django.urls import path
from .views import user_registration, user_login, user_logout, user_update, user_view
app_name = "user_authentication"
urlpatterns = [
    path('', user_login, name="userlogin"),
    path('registration/', user_registration, name="userregistration"),
    path('viewuser/', user_view, name="userview"),
    path('updateuser/', user_update, name="userupdate"),
    path('logout/', user_logout, name="userlogout"),
]
