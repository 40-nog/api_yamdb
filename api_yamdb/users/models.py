from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        verbose_name='Почта пользователя',
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        max_length=200, blank=True
    )
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    confirmation_code = models.CharField(max_length=50, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    class Meta:
        ordering = ['id']
