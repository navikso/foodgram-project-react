# Generated by Django 3.2 on 2023-04-14 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_ingredientamount_amount'),
    ]

    # operations = [
    #     migrations.RenameField(
    #         model_name='ingredientamount',
    #         old_name='recipe_ingredient',
    #         new_name='name',
    #     ),
    #     migrations.RemoveField(
    #         model_name='ingredient',
    #         name='amount',
    #     ),
    #     migrations.AddField(
    #         model_name='recipe',
    #         name='tags',
    #         field=models.ManyToManyField(to='recipes.Tag', verbose_name='Список тегов'),
    #     ),
    #     migrations.AlterField(
    #         model_name='ingredient',
    #         name='measurement_unit',
    #         field=models.TextField(choices=[('Г', 'Грамм'), ('КГ', 'Килограмм'), ('Л', 'Литр'), ('МЛ', 'Милилитр'), ('Ч.Л.', 'Чайная ложка'), ('СТ.Л.', 'Столовая ложка'), ('СТ.', 'Стакан'), ('ШТ.', 'Штука')], null=True, verbose_name='Единица измерения'),
    #     ),
    #     migrations.AlterField(
    #         model_name='ingredient',
    #         name='name',
    #         field=models.TextField(choices=[('Абрикос', 'Абрикос'), ('Авокадо', 'Авокадо'), ('Амарант', 'Амарант'), ('Амарантовое масло', 'Амарантовое масло'), ('Ананас', 'Ананас'), ('Апельсин', 'Апельсин'), ('Арахис', 'Арахис'), ('Арбуз', 'Арбуз'), ('Айва', 'Айва'), ('Бананы', 'Бананы'), ('Бананы сушёные', 'Бананы сушёные'), ('Банана цветок', 'Банана цветок'), ('Батат', 'Батат'), ('Бразильский орех', 'Бразильский орех'), ('Брусника', 'Брусника'), ('Булгур', 'Булгур'), ('Ваниль', 'Ваниль'), ('Виноград', 'Виноград'), ('Вишня', 'Вишня'), ('Гранат', 'Гранат'), ('Грецкий орех', 'Грецкий орех'), ('Гречка', 'Гречка'), ('Гречка зелёная', 'Гречка зелёная'), ('Грейпфрут', 'Грейпфрут'), ('Грибы', 'Грибы'), ('Груша', 'Груша'), ('Дайкон', 'Дайкон'), ('Дуриан', 'Дуриан')], null=True, unique=True, verbose_name='Название'),
    #     ),
    #     migrations.AlterField(
    #         model_name='ingredientamount',
    #         name='amount',
    #         field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, 'Значение должно быть больше нуля')], verbose_name='Количество ингредиентов'),
    #     ),
    # ]
