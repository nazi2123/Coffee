
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from bonus.models import Employee, User


def login_view(request):
    if request.method == 'POST':
        print(request.POST['username'], request.POST['password'])
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        print(user)
        if user is not None:
            login(request, user)
            return redirect('personal_account')
        else:
            #
            return render(request, 'bonus/login.html', {'login_error': True, 'users': Employee.objects.values_list("id", "username")})
    return render(request, 'bonus/login.html', {'users': Employee.objects.values_list("id", "username")})

@login_required
def personal_account(request):
    try:
        user_name = request.user.name
    except AttributeError:
        user_name = request.user.username

    return render(request, 'bonus/personal_account.html', {
        'user_name': user_name
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get("phone")
        if name and phone:
            User.objects.create(name=name, phone=phone)
            return redirect('personal_account')
    return render(request, 'bonus/add_client.html')