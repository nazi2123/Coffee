from django.db import models

# Create your models here.
class User(models.Model):
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    balance = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Card {self.id} – User {self.user.name}'

class Employee(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
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

    def __str__(self):
        return f"{self.type} – {self.amount} руб на карту {self.card.amount}"







