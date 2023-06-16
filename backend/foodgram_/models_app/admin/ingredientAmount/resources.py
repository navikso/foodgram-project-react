from django.contrib import admin

from models_app.models import IngredientAmount


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    pass
