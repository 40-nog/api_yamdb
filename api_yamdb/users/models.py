from django.db import models
from django.contrib.auth.models import AbstractUser


#CHOICES = (
#    ('user', 'Пользователь'),
#    ('moderator', 'Модератор'),
#    ('admin', 'Администратор')
#)


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

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
    role = models.CharField(max_length=16, choices=CHOICES, default=USER,)
    confirmation_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR