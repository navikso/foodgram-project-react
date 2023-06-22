from models_app.models import (
    Favorites,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingList,
    Subscription,
    Tag
)
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from models_app.models import User


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user"
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_filter = (
        "name",
    )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "amount",
        "ingredient",
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
    )
    filter_horizontal = (
        "ingredients",
        "tags"
    )
    list_filter = (
        "name",
        "author",
        "tags"
    )

    readonly_fields = (
        "favorite_count",
        "created_at"
    )

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "name",
                "favorite_count",
                "image",
                "text",
                "cooking_time",
                "ingredients",
                "tags",
                "author",
                "created_at",
            ),
        }),
    )

    def favorite_count(self, instance):
        return instance.recipes_favorites.count()

    favorite_count.short_description = "Добавили в избранное"


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user"
    )
    filter_horizontal = (
        "recipes",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user"
    )
    filter_horizontal = (
        "authors",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug"
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_blocked"
    )
    list_filter = (
        "email",
        "first_name"
    )

    change_list_template = "admin/users.html"

    def get_urls(self):
        urls = super().get_urls()
        return [
                   path("administration/", self.administration),
               ] + urls

    def administration(self, request):
        if request.method == "POST":
            user = User.objects.get(id=request.POST.dict()["user"])
            user.set_password(request.POST.dict()["new_pass"])
            user.save()
            self.message_user(
                request,
                "Вы успешно поменяли пароль пользователю"
            )
            return redirect("..")
        return render(
            request,
            "admin/administaration.html",
            context={
                "users": User.objects.all(),
            }
        )
