from django.contrib import admin

from bonus.models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created_at')
    search_fields = ('name', 'phone')
    ordering = ('-created_at',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'created_at','used_at')
    search_fields = ('id', 'user__name')
    ordering = ('-used_at',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'employee', 'amount', 'type', 'created_at')
    search_fields = ('card__user__name','card__id', 'employee__name')
    list_filter = ('type',)
    ordering = ('-created_at',)


