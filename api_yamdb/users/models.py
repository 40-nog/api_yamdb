from django.contrib.auth.models import AbstractUser
from django.db import models

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
    
    bio = models.TextField(
        'Биография',
        blank=True,
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