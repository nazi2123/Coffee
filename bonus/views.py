
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from bonus.models import Employee, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Card, Transaction
from django.urls import reverse
from django.utils import timezone


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


@login_required
def user_info(request):
    """
    1) При GET — просто отобразить форму поиска по телефону.
    2) При POST с action=search — найти пользователя по номеру, получить/создать его карту.
    3) При POST с action=deposit — начислить 5% от суммы заказа на баланс карты.
    4) При POST с action=withdraw — списать баллы при покупке.
    """
    context = {
        'user_obj': None,
        'card_balance': 0,
        'searched': False,
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        # ---------- Поиск пользователя ----------
        if action == 'search':
            phone_raw = request.POST.get('phone_search', '').strip()
            # Нормализация, чтобы сохранить формат "+7(123)456-78-90" и т.п.
            # Мы ищем без пробелов, дефисов и скобок: оставляем только цифры.
            digits = ''.join(filter(str.isdigit, phone_raw))
            if digits.startswith('7'):
                normalized = '+7' + digits[1:]
            else:
                normalized = '+7' + digits  # на всякий случай
            try:
                user_obj = User.objects.get(phone=normalized)
                # Если у пользователя нет карты, создаём с балансом "0"
                card, created = Card.objects.get_or_create(user=user_obj, defaults={'balance': '0'})
                context['user_obj'] = user_obj
                context['card_balance'] = int(card.balance)
            except User.DoesNotExist:
                context['user_obj'] = None
            context['searched'] = True

        # ---------- Начисление баллов ----------
        elif action == 'deposit':
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
            # Обновляем баланс на карте
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
            # После сохранения возвращаемся к форме поиска с отображением обновленного баланса
            return redirect(f"{reverse('user_info')}?phone={user_obj.phone}")


          # ---------- Списание баллов ----------
        elif action == 'withdraw':
            user_id = request.POST.get('user_id')
            order_sum = float(request.POST.get('order_sum', '0'))
            user_obj = get_object_or_404(User, id=user_id)
            card = Card.objects.filter(user=user_obj).first()
            if not card:
                # Если карты нет, не можем списать — просто перенаправим обратно
                return redirect(reverse('user_info'))
            current_balance = int(card.balance)
            # Сколько баллов используем
            use_points = min(current_balance, int(order_sum))
            final_price = order_sum - use_points
            if use_points >= order_sum:
                # Если баллов хватает на полную стоимость, клиент платит 1 рубль,
                # а остальные баллы списываются на сумму (order_sum - 1)
                final_price = 1
                use_points = int(order_sum) - 1
            # Обновляем новый баланс
            new_balance = current_balance - use_points
            card.balance = str(new_balance)
            card.save()
            # Создаем транзакцию списания
            Transaction.objects.create(
                card=card,
                employee=request.user,
                amount=str(use_points),
                type='withdraw',
                created_at=timezone.now()
            )
            return redirect(f"{reverse('user_info')}?phone={user_obj.phone}")

    else:
        # Если в GET есть параметр ?phone=..., автоматически ищем
        phone_param = request.GET.get('phone', '').strip()
        if phone_param:
            digits = ''.join(filter(str.isdigit, phone_param))
            if digits.startswith('7'):
                normalized = '+7' + digits[1:]
            else:
                normalized = '+7' + digits
            try:
                user_obj = User.objects.get(phone=normalized)
                card, created = Card.objects.get_or_create(user=user_obj, defaults={'balance': '0'})
                context['user_obj'] = user_obj
                context['card_balance'] = int(card.balance)
            except User.DoesNotExist:
                context['user_obj'] = None
            context['searched'] = True

    return render(request, 'bonus/user_info.html', context)