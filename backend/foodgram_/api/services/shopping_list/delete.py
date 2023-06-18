from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import ShoppingList, User
from django import forms


class ShoppingListDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ["presence_shoppinglist", "presence_recipe"]

    def process(self):
        self.run_custom_validations()
        self.result = self._delete
        return self

    @property
    def _delete(self):
        return self._shoppinglist.recipes.remove(self._recipe)

    @property
    @lru_cache
    def _shoppinglist(self):
        try:
            return ShoppingList.objects.get(user=self.cleaned_data["user"])
        except ObjectDoesNotExist:
            return None

    @property
    @lru_cache
    def _recipe(self):
        try:
            return self._shoppinglist.recipes.get(id=self.cleaned_data["id"])
        except ObjectDoesNotExist:
            return None

    def presence_shoppinglist(self):
        if not self._shoppinglist:
            raise NotFound(
                message=(
                    "Учетные данные не были предоставлены. (В корзине пусто)"
                )
            )

    def presence_recipe(self):
        if not self._recipe:
            raise NotFound(
                message=(
                    "Учетные данные не были предоставлены. (Рецепт не найден)"
                )
            )
