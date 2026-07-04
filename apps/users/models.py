from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CURRENCY_CHOICES = [('UAH', '₴'), ('USD', '$'), ('EUR', '€')]

    avatar = models.ImageField(upload_to='avatar/%Y/%m', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username