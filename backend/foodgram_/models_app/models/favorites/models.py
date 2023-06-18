from django.db import models


class Favorites(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE,
        related_name="list_recipes_favorites",
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f"{self.recipe.name} {self.user.username}"

    class Meta:
        db_table = 'favorites'
        app_label = "models_app"
        unique_together = ("recipe", "user")
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
