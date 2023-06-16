from django.contrib import admin

from models_app.models import ShoppingList


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("id", )
    filter_horizontal = ["recipes", ]
    pass
