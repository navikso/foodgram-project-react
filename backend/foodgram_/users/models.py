from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    email = models.EmailField(max_length=255, verbose_name="�����")

    class Meta:
        verbose_name = '������������'
        verbose_name_plural = '������������'

    def __str__(self):
        return self.username
