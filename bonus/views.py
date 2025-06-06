from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from bonus.models import Employee
from .models import User, Card, Transaction


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('personal_account')
        else:
            return render(request, 'bonus/login.html', {
                'login_error': True,
                'users': Employee.objects.values_list("id", "username")
            })
    return render(request, 'bonus/login.html', {
        'users': Employee.objects.values_list("id", "username")
    })


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


@login_required
def user_info(request):
    """
    1) При GET — получить параметр phone, найти пользователя и его карту (или создать).
    2) При POST с action=deposit — начислить 5% от суммы заказа на баланс карты.
    3) При POST с action=withdraw — списать баллы при покупке.
    """
    context = {
        'user_obj': None,
        'card_balance': 0,
        'searched': False,
    }
    print(request.method)
    if request.method == 'GET':

        phone_raw = request.GET.get('phone', '').strip()
        phone_raw = "+" + phone_raw if not phone_raw.startswith("+") else phone_raw
        try:
            print(phone_raw)
            user_obj = User.objects.get(phone=phone_raw)
            print(user_obj)
            card, created = Card.objects.get_or_create(user=user_obj, defaults={'balance': '0'})
            context['user_obj'] = user_obj
            context['card_balance'] = int(card.balance)
        except User.DoesNotExist:
            context['user_obj'] = None

        context['searched'] = True
        return render(request, 'bonus/user_info.html', context)

    # ---------- Обработка POST-запросов для модальных окон ----------
    elif request.method == 'POST':
        action = request.POST.get('action')
        print(action)

        # ---------- Начисление баллов ----------
        if action == 'deposit':
            user_id = request.POST.get('user_id')
            order_sum = float(request.POST.get('order_sum', '0'))
            user_obj = get_object_or_404(User, id=user_id)
            card = Card.objects.filter(user=user_obj).first()
            if not card:
                card = Card.objects.create(user=user_obj, balance='0')
            # Рассчитываем 5% бонуса
            bonus = int(order_sum * 0.05)
            current_balance = int(card.balance)
            new_balance = current_balance + bonus
            card.balance = str(new_balance)
            card.save()
            # Создаем запись транзакции
            Transaction.objects.create(
                card=card,
                employee=request.user,
                amount=str(bonus),
                type='deposit',
                created_at=timezone.now()
            )
            # Перенаправляем обратно на GET с тем же номером
            return redirect(f"{reverse('user_info')}?phone={user_obj.phone}")

        # ---------- Списание баллов ----------
        elif action == 'withdraw':
            user_id = request.POST.get('user_id')
            order_sum = float(request.POST.get('order_sum', '0'))
            user_obj = get_object_or_404(User, id=user_id)
            card = Card.objects.filter(user=user_obj).first()
            if not card:
                return redirect(reverse('user_info'))
            current_balance = int(card.balance)
            # Сколько баллов используем
            use_points = min(current_balance, int(order_sum))
            final_price = order_sum - use_points
            if use_points >= order_sum:
                # Если баллов хватает на полную стоимость, клиент платит 1 рубль,
                # а остальные баллы списываются (order_sum - 1)
                final_price = 1
                use_points = int(order_sum) - 1
            new_balance = current_balance - use_points
            card.balance = str(new_balance)
            card.save()
            Transaction.objects.create(
                card=card,
                employee=request.user,
                amount=str(use_points),
                type='withdraw',
                created_at=timezone.now()
            )
            return redirect(f"{reverse('user_info')}?phone={user_obj.phone}")

    # На всякий случай рендерим страницу (хотя сюда обычно не попадут)
    return render(request, 'bonus/user_info.html', context)
