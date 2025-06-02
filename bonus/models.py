from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(models.Model):
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural="Пользователи"

    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    balance = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Бонусная карта"
        verbose_name_plural = "Бонусные карты"
    def __str__(self):
        return f'Card {self.id} – User {self.user.name}'

class Employee(AbstractUser):
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def save(self, *args, **kwargs):
        # если пароль ещё не захэширован (не начинается с 'pbkdf2_…')
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
class  Transaction(models.Model):
    TYPE_CHOICES=  [
        ('deposit',"зачисление"),
        ("withdraw", "списание")
    ]
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="transactions")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="transactions")
    amount = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
    def __str__(self):
        return f"{self.type} – {self.amount} руб на карту {self.card.amount}"







