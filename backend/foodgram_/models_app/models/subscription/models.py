from django.db import models


class Subscription(models.Model):
    authors = models.ManyToManyField("User", verbose_name='Пользователи на которых подписан', related_name="list_authors")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='Пользователь', related_name="list_user_subs")

    def __str__(self):
        return f"Вы подписаны на рецепты"

    class Meta:
        db_table = 'subscriptions'
        app_label = "models_app"
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
