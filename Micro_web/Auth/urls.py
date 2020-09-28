from django.urls import path
from . import views


urlpatterns = [
    path('',views.Home, name ='home'),
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('change_password/',views.Change_Password,name='changepassword'),
]
