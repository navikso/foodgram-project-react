import json
from functools import lru_cache
from json import JSONDecodeError

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.errors import NotFound, ForbiddenError, ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import Recipe, Tag, Ingredient
from models_app.models import User
from models_app.models import IngredientAmount


class RecipeUpdateService(ServiceWithResult):
    id = forms.IntegerField()
    ingredients = forms.CharField()
    tags = forms.CharField()
    image = forms.ImageField()
    name = forms.CharField(max_length=200)
    text = forms.CharField()
    cooking_time = forms.IntegerField(min_value=1)
    user = ModelField(User)

    custom_validations = ["presence_recipe", "access_user", "_list_ingredients"]

    def process(self):
        self.run_custom_validations()
        self.result = self._update
        return self

    @property
    def _update(self):
        recipe = self._recipe
        recipe.name = self.cleaned_data["name"]
        recipe.image = self.cleaned_data["image"]
        recipe.text = self.cleaned_data["text"]
        recipe.cooking_time = self.cleaned_data["cooking_time"]
        for ingredient, amount in self._list_ingredients():
            try:
                ing = recipe.ingredients.get(ingredient=ingredient)
                ing.amount = amount
                ing.save()
            except ObjectDoesNotExist:
                ing = IngredientAmount.objects.create(ingredient=ingredient, amount=amount)
                recipe.ingredients.add(ing)
        for tag in self._tags:
            try:
                recipe.tags.get(slug=tag.slug)
            except ObjectDoesNotExist:
                recipe.tags.add(tag)
        return recipe

    @property
    def _recipe(self):
        try:
            return Recipe.objects.get(id=self.cleaned_data["id"])
        except ObjectDoesNotExist:
            return None

    @lru_cache
    def _list_ingredients(self):
        errors = []
        list_ingredients = []
        for id_ingredient, amount in self._ingredients:
            if amount <= 0:
                errors.append(
                    {
                        "id": id_ingredient,
                        "amount": "Убедитесь, что это значение больше либо равно 1."
                    }
                )
            try:
                list_ingredients.append([Ingredient.objects.get(id=id_ingredient), amount])
            except ObjectDoesNotExist:
                raise NotFound(message=f"Страница не найдена. (Ингредиента с id {id_ingredient} не найдено)")
        if errors:
            raise ValidationError(message={
                "ingredients": errors
            })
        return list_ingredients

    @property
    def _ingredients(self):
        try:
            return json.loads(self.cleaned_data["ingredients"])
        except JSONDecodeError:
            raise ValidationError(message="Передайте корректный список ингредиентов")

    @property
    def _tags(self):
        list_tags = []
        for id_tag in self.cleaned_data["tags"].split(","):
            try:
                list_tags.append(Tag.objects.get(id=id_tag))
            except ObjectDoesNotExist:
                raise NotFound(message=f"Страница не найдена. (Тега с id {id_tag} не найдено)")
        return list_tags

    def presence_recipe(self):
        if not self._recipe:
            raise NotFound(message="Страница не найдена.")

    def access_user(self):
        if self.cleaned_data["user"] != self._recipe.user:
            raise ForbiddenError(message="У вас недостаточно прав для выполнения данного действия.")
