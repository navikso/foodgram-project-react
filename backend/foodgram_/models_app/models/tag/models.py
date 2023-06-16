from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    color = models.CharField(max_length=7, default="#ffffff", verbose_name='Цвет')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return f"{self.name} - {self.color}"

    class Meta:
        db_table = 'tags'
        app_label = "models_app"
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
