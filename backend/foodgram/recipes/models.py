from django.db import models
from django.db.models import Count
from django.core.validators import MinValueValidator
from users.models import UserProfile


class Ingredient(models.Model):
    name = models.TextField(
        'Название',
        unique=True,
        null=True,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=1,
        validators=[
            MinValueValidator(0, 'Значение должно быть больше нуля')
        ]
    )
    measurement_unit = models.TextField(
        'Единица измерения',
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.TextField('Название', unique=True)
    color = models.CharField('Цвет', max_length=7, default="#ffffff")
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """Класс, представляющий модель рецепта."""

    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        default=1
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
    )
    name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Название',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True, db_index=True
    )
    tags = models.ManyToManyField(
        Tag,
        # related_name='recipes',
        verbose_name='Список тегов',
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Описание',
    )
    is_favorite = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                name='author_recipe_unique',
                fields=('author', 'name'),
            ),
        ]

    def __str__(self):
        return f'{self.name}'


class IngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=1,
        validators=[
            MinValueValidator(0, 'Значение должно быть больше нуля')
        ]
    )
    name = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    recipe_ingredient = Ingredient.objects.annotate(
        num_amount=Count('amount')
    )
    recipe_ingredient[0].amount__count

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.recipe}'


class TagRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тэг к рецепту'
        verbose_name_plural = 'Тэги к рецепту'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Список покупок'

    def __str__(self):
        return f'{self.recipe} добавлен в список покупок'


class Favorite(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Избранный рецепт',
        null=True
    )

    class Meta:
        verbose_name_plural = 'Избранное'
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Избранный рецепт'
            ),
        ]

    def __str__(self):
        return f'{self.recipe} добавлен в избранное'


class Subscription(models.Model):
    subsciber = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='subsciber',
        verbose_name='Подписчик',
        null=True
    )
    is_subscibed = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='is_subscibed',
        verbose_name='Автор',
        null=True
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=['subsciber', 'is_subscibed'],
                name='Подписчик'
            ),
        ]

    def __str__(self):
        return f'{self.subsciber} подписался на рецепты {self.is_subscibed}'
