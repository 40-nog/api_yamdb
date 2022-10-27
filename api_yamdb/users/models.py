from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта пользователя',
        max_length=150,
        null=True,
        unique=True
    )
    bio = models.TextField(
        max_length=200, blank=True
    )
    role = models.CharField(max_length=16, choices=CHOICES)
    confirmation_code = models.CharField(max_length=50, blank=True)
