from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    TYPE_CHOICES = [('INCOME', 'Доход'), ('EXPENSE', 'Растраты')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Тип')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('user', 'name', 'type')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions', verbose_name='Категория')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Сумма')
    date = models.DateField(default=timezone.now, verbose_name='Дата операции')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ('-date', '-created_at',)

    def __str__(self):
        return f"{self.date}: {self.category.name} ({self.amount})"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets', verbose_name='Категория')
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))], verbose_name='Лимит')

    class Meta:
        verbose_name = 'Лимит'
        verbose_name_plural = 'Лимиты'
        unique_together = ('user', 'category')

    @property
    def current_spent(self) -> Decimal:
        from django.apps import apps
        Transaction = apps.get_model('finance', 'Transaction')

        now = timezone.now()

        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            date__year=now.year,
            date__month=now.month
        ).aggregate(total=models.Sum('amount'))['total']

        return spent or Decimal('0.00')

    @property
    def is_exceeded(self) -> bool:
        return self.current_spent > self.limit_amount


class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goal')
    title = models.CharField(max_length=150, verbose_name='Название цели')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))], verbose_name='Цель')
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], verbose_name='Накоплено')
    deadline = models.DateField(verbose_name='Срок выполнения')

    class Meta:
        verbose_name = 'Цель накопления'
        verbose_name_plural = 'Цели накоплений'
        ordering = ['deadline']

    @property
    def progress_percent(self) -> int:
        if self.target_amount <= 0:
            return 100
        pct = (self.current_amount / self.target_amount) * 100
        return min(int(pct), 100)




