from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    username = models.CharField(
        'username', max_length=150, blank=False, unique=True
    )
    first_name = models.CharField('first name', max_length=150, blank=False)
    password = models.CharField('password', max_length=150)
    is_subscribed = models.BooleanField('is_subscribed', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
