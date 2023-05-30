# Generated by Django 3.2 on 2023-04-11 10:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20230410_1336'),
    ]

    # operations = [
    #     # migrations.CreateModel(
    #     #     name='Ingredient',
    #     #     fields=[
    #     #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #     #         ('name', models.TextField(choices=[('Абрикос', 'Абрикос'), ('Авокадо', 'Авокадо'), ('Амарант', 'Амарант'), ('Амарантовое масло', 'Амарантовое масло'), ('Ананас', 'Ананас'), ('Апельсин', 'Апельсин'), ('Арахис', 'Арахис'), ('Арбуз', 'Арбуз'), ('Айва', 'Айва'), ('Бананы', 'Бананы'), ('Бананы сушёные', 'Бананы сушёные'), ('Банана цветок', 'Банана цветок'), ('Батат', 'Батат'), ('Бразильский орех', 'Бразильский орех'), ('Брусника', 'Брусника'), ('Булгур', 'Булгур'), ('Ваниль', 'Ваниль'), ('Виноград', 'Виноград'), ('Вишня', 'Вишня'), ('Гранат', 'Гранат'), ('Грецкий орех', 'Грецкий орех'), ('Гречка', 'Гречка'), ('Гречка зелёная', 'Гречка зелёная'), ('Грейпфрут', 'Грейпфрут'), ('Грибы', 'Грибы'), ('Груша', 'Груша'), ('Дайкон', 'Дайкон'), ('Дуриан', 'Дуриан')], default='Соль', null=True)),
    #     #         ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
    #     #         ('measurement_unit', models.TextField(choices=[('Г', 'Грамм'), ('КГ', 'Килограмм'), ('Л', 'Литр'), ('МЛ', 'Милилитр'), ('Ч.Л.', 'Чайная ложка'), ('СТ.Л.', 'Столовая ложка'), ('СТ.', 'Стакан'), ('ШТ.', 'Штука')], default='г')),
    #     #         ('amount', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, 'Значение должно быть больше нуля')], verbose_name='Количество')),
    #     #     ],
    #     #     options={
    #     #         'verbose_name': 'Ингредиент',
    #     #         'verbose_name_plural': 'Ингредиенты',
    #     #     },
    #     # ),
    #     # migrations.AddField(
    #     #     model_name='recipe',
    #     #     name='cooking_time',
    #     #     field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Время приготовления, мин'),
    #     # ),
    #     migrations.RemoveField(
    #         model_name='recipe',
    #         name='tags',
    #     ),
    #     migrations.AddField(
    #         model_name='recipe',
    #         name='tags',
    #         field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.tag', verbose_name='Тэг'),
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
    #         model_name='follow',
    #         constraint=models.UniqueConstraint(fields=('user', 'following'), name='Подписчик'),
    #     ),
    # ]
