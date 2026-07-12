from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Budget._meta.fields]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields]


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SavingsGoal._meta.fields]