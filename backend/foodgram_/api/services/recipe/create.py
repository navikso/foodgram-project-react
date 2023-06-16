import json
from json import JSONDecodeError

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.errors import ValidationError, NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User
from models_app.models import Recipe
from models_app.models import Ingredient
from models_app.models import Tag

from models_app.models import IngredientAmount


class RecipeCreateService(ServiceWithResult):
    ingredients = forms.CharField()
    tags = forms.CharField()
    image = forms.ImageField()
    name = forms.CharField(max_length=200)
    text = forms.CharField()
    cooking_time = forms.IntegerField(min_value=1)
    user = ModelField(User)

    def process(self):
        self.result = self._create
        self._add_ingredients(self.result)
        self._add_tags(self.result)
        return self

    @property
    def _create(self):
        return Recipe.objects.create(
            name=self.cleaned_data["name"],
            image=self.cleaned_data["image"],
            text=self.cleaned_data["text"],
            cooking_time=self.cleaned_data["cooking_time"],
            user=self.cleaned_data["user"]
        )

    def _add_ingredients(self, recipe):
        for element in self._list_ingredients:
            recipe.ingredients.add(
                IngredientAmount.objects.get_or_create(
                    ingredient=element[0],
                    amount=element[1]
                )[0]
            )

    def _add_tags(self, recipe):
        for element in self._tags:
            recipe.tags.add(element)

    @property
    def _list_ingredients(self):
        list_ingredients = []
        for id_ingredient, amount in self._ingredients:
            try:
                list_ingredients.append([Ingredient.objects.get(id=id_ingredient), amount])
            except ObjectDoesNotExist:
                raise NotFound(message=f"Страница не найдена. (Ингредиента с id {id_ingredient} не найдено)")
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
