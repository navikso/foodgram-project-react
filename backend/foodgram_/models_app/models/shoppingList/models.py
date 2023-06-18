from django.db import models


class ShoppingList(models.Model):
    recipes = models.ManyToManyField("Recipe", verbose_name='Рецепт')
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, verbose_name='Пользователь'
    )

    def __str__(self):
        return f"{self.id} {self.user}"

    class Meta:
        db_table = 'shoppingLists'
        app_label = "models_app"
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
