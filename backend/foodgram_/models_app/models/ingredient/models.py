from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=30, verbose_name='Единица измерения')

    def __str__(self):
        return f"{self.id} {self.name} {self.measurement_unit}"

    class Meta:
        db_table = 'ingredients'
        app_label = "models_app"
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
