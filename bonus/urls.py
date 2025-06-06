from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from bonus.views import login_view, personal_account, add_client, user_info

urlpatterns = [
    path('login/', login_view, name="login"),
    path("",personal_account, name="personal_account"),
    path("add_client/",  add_client, name="add_client"),
    path("user_info/", user_info, name="user_info", )
]
