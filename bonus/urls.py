from django.contrib import admin
from django.urls import path

from bonus.views import login_view, personal_account

urlpatterns = [
    path('login/', login_view, name="login"),
    path("account/",personal_account, name="personal_account")
]
