from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(
        max_length=30, verbose_name="Единица измерения")

    class Meta:
        db_table = "ingredients"
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.id} {self.name} {self.measurement_unit}"


class IngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(0, "Значение должно быть больше нуля")],
        verbose_name="Количество ингредиентов", )
    ingredient = models.ForeignKey(
        "Ingredient", on_delete=models.CASCADE,
        verbose_name="Ингредиент")

    class Meta:
        db_table = "ingredient_amounts"
        verbose_name = "Количество ингридиентов"

    def __str__(self):
        return f"{self.amount} - {self.ingredient}"


class Recipe(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="image/recipe", verbose_name="Изображение")
    text = models.TextField(verbose_name="Описание рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        default=1, verbose_name="Время приготовления (в минутах)")
    ingredients = models.ManyToManyField(
        "IngredientAmount", verbose_name="Ингредиенты")
    tags = models.ManyToManyField("Tag", verbose_name="Теги")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="user_recipes",
        verbose_name="Пользователь")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "recipes"
        ordering = ("-created_at",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.id} - {self.name}"


class Favorites(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE,
        related_name="list_recipes_favorites", verbose_name="Рецепт")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        db_table = "favorites"
        unique_together = ("recipe", "user")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.recipe.name} {self.user.username}"


class ShoppingList(models.Model):
    recipes = models.ManyToManyField(
        "Recipe",
        verbose_name="Рецепт",
        blank=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        db_table = "shopping_lists"
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f"{self.id} {self.user}"


class Subscription(models.Model):
    authors = models.ManyToManyField(
        User,
        verbose_name="Пользователи, на которых подписан",
        related_name="list_authors",
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="list_user_subs")

    class Meta:
        db_table = "subscriptions"
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"Вы подписаны на рецепты {self.authors}"


class Tag(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название")
    color = models.CharField(
        max_length=7, default="#ffffff", verbose_name="Цвет")
    slug = models.SlugField(
        unique=True, db_index=True, verbose_name="Слаг")

    class Meta:
        db_table = "tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name} - {self.color}"
