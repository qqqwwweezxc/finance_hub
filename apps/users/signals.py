from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.finance.models import Category


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """Генерирует базовый набор категорий для новозарегистрированного пользователя"""
    if created:
        defaults = [
            ('Зарплата', 'INCOME'), ('Инвестиции', 'INCOME'),
            ('Продукты', 'EXPENSE'), ('Транспорт', 'EXPENSE'),
            ('Жилье', 'EXPENSE'), ('Развлечения', 'EXPENSE')
        ]

        Category.objects.bulk_create([
            Category(user=instance, name=name, type=cat_type) for name, cat_type in defaults
        ])