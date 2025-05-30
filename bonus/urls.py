from django.contrib import admin
from django.urls import path

from bonus.views import login_view

urlpatterns = [
    path('login/', login_view, name="login"),
]
