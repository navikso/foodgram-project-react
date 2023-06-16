from django.contrib import admin

from models_app.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ["ingredients", "tags"]
    list_display = ("id", )
