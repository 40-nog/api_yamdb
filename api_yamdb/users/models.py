from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=16, choices=CHOICES)
    confirmation_code = models.CharField(max_length=50, blank=True)
