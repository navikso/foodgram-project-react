from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    email = models.EmailField(max_length=255, verbose_name="Почта")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
