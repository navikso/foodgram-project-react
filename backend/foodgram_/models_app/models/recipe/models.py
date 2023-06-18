from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="image/recipe", verbose_name="Изображение"
    )
    text = models.TextField(verbose_name="Описание рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        default=1, verbose_name='Время приготовления (в минутах)'
    )
    ingredients = models.ManyToManyField(
        "IngredientAmount", verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField("Tag", verbose_name='Теги')
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE,
        related_name="user_recipes",
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        db_table = 'recipes'
        ordering = ('-created_at',)
        app_label = "models_app"
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'