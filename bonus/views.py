
from django.shortcuts import render

from bonus.models import Employee


def login_view (request):
    users=Employee.objects.values_list("id", "name")
    return render(request, 'bonus/login.html', {"users":users})

# Create your views here.
