from django.contrib import admin

from .models import (
    Recipe, Tag,
    Ingredient,
    IngredientAmount,
    Favorite, ShoppingCart,
    Subscription
)


class IngredientInline(admin.StackedInline):
    model = IngredientAmount
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'id')
    search_fields = ('name',)
    list_filter = ('author', 'name',)
    inlines = [IngredientInline]
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscription)
