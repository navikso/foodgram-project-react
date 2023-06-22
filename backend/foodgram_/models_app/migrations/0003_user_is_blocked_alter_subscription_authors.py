# Generated by Django 4.0 on 2023-06-20 15:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0002_remove_user_is_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='Блокировка'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='authors',
            field=models.ManyToManyField(null=True, related_name='list_authors', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи на которых подписан'),
        ),
    ]