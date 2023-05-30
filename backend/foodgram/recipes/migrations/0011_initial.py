# Generated by Django 3.2 on 2023-04-14 15:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0010_initial'),
    ]

    # operations = [
    #     migrations.CreateModel(
    #         name='Ingredient',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('name', models.TextField(choices=[('Абрикос', 'Абрикос'), ('Авокадо', 'Авокадо'), ('Амарант', 'Амарант'), ('Амарантовое масло', 'Амарантовое масло'), ('Ананас', 'Ананас'), ('Апельсин', 'Апельсин'), ('Арахис', 'Арахис'), ('Арбуз', 'Арбуз'), ('Айва', 'Айва'), ('Бананы', 'Бананы'), ('Бананы сушёные', 'Бананы сушёные'), ('Банана цветок', 'Банана цветок'), ('Батат', 'Батат'), ('Бразильский орех', 'Бразильский орех'), ('Брусника', 'Брусника'), ('Булгур', 'Булгур'), ('Ваниль', 'Ваниль'), ('Виноград', 'Виноград'), ('Вишня', 'Вишня'), ('Гранат', 'Гранат'), ('Грецкий орех', 'Грецкий орех'), ('Гречка', 'Гречка'), ('Гречка зелёная', 'Гречка зелёная'), ('Грейпфрут', 'Грейпфрут'), ('Грибы', 'Грибы'), ('Груша', 'Груша'), ('Дайкон', 'Дайкон'), ('Дуриан', 'Дуриан')], unique=True)),
    #             ('measurement_unit', models.TextField(choices=[('Г', 'Грамм'), ('КГ', 'Килограмм'), ('Л', 'Литр'), ('МЛ', 'Милилитр'), ('Ч.Л.', 'Чайная ложка'), ('СТ.Л.', 'Столовая ложка'), ('СТ.', 'Стакан'), ('ШТ.', 'Штука')])),
    #             ('amount', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, 'Значение должно быть больше нуля')], verbose_name='Количество')),
    #         ],
    #         options={
    #             'verbose_name': 'Ингредиент',
    #             'verbose_name_plural': 'Ингредиенты',
    #         },
    #     ),
    #     migrations.CreateModel(
    #         name='Recipe',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('cooking_time', models.PositiveSmallIntegerField(default=1, verbose_name='Время приготовления (в минутах)')),
    #             ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Картинка')),
    #             ('name', models.CharField(db_index=True, max_length=25, verbose_name='Название')),
    #             ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
    #             ('text', models.TextField(verbose_name='Описание')),
    #             ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
    #         ],
    #         options={
    #             'verbose_name': 'Рецепт',
    #             'verbose_name_plural': 'Рецепты',
    #             'ordering': ('-pub_date',),
    #         },
    #     ),
    #     migrations.CreateModel(
    #         name='Tag',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('name', models.TextField(unique=True, verbose_name='Название')),
    #             ('color', models.CharField(default='#ffffff', max_length=7, verbose_name='Цвет')),
    #             ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
    #         ],
    #         options={
    #             'verbose_name': 'Тэг',
    #             'verbose_name_plural': 'Тэги',
    #         },
    #     ),
    #     migrations.CreateModel(
    #         name='TagRecipe',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
    #             ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag')),
    #         ],
    #         options={
    #             'verbose_name': 'Тэг к рецепту',
    #             'verbose_name_plural': 'Тэги к рецепту',
    #         },
    #     ),
    #     migrations.CreateModel(
    #         name='ShoppingCart',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('title', models.CharField(default='Список покупок', max_length=255)),
    #             ('shop_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='recipes.ingredient')),
    #         ],
    #     ),
    #     migrations.CreateModel(
    #         name='IngredientAmount',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('amount', models.PositiveSmallIntegerField(default=1, verbose_name='Количество ингредиентов')),
    #             ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.ingredient', verbose_name='Ингредиент')),
    #             ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='Рецепт')),
    #         ],
    #         options={
    #             'verbose_name': 'Ингредиент',
    #             'verbose_name_plural': 'Ингредиенты',
    #         },
    #     ),
    #     migrations.CreateModel(
    #         name='Follow',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор блога')),
    #             ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
    #         ],
    #         options={
    #             'verbose_name': 'Подписка',
    #             'verbose_name_plural': 'Подписки',
    #         },
    #     ),
    #     migrations.AddConstraint(
    #         model_name='recipe',
    #         constraint=models.UniqueConstraint(fields=('author', 'name'), name='author_recipe_unique'),
    #     ),
    #     migrations.AddConstraint(
    #         model_name='follow',
    #         constraint=models.UniqueConstraint(fields=('user', 'following'), name='Подписчик'),
    #     ),
    # ]
