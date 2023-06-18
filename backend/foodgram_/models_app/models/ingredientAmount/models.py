from django.core.validators import MinValueValidator
from django.db import models


class IngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(0, 'Значение должно быть больше нуля')],
        verbose_name='Количество ингредиентов',
    )
    ingredient = models.ForeignKey(
        "Ingredient", on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )

    def __str__(self):
        return f"{self.amount} - {self.ingredient}"

    class Meta:
        db_table = 'ingredient_amounts'
        app_label = "models_app"
        verbose_name = 'Количество ингридиентов'
        verbose_name_plural = 'Количества ингридиентов'
