from django import forms
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Recipe

from models_app.models import Favorites


class FavoriteDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ["recipe_presence"]

    def process(self):
        self.run_custom_validations()
        self._delete()
        return self

    def _delete(self):
        Favorites.objects.get(recipe_id=self.cleaned_data["id"]).delete()

    def recipe_presence(self):
        if not Recipe.objects.filter(id=self.cleaned_data["id"]).exists():
            raise ValidationError(message="Такого рецепта не существует")
        if not Favorites.objects.filter(recipe_id=self.cleaned_data["id"]).exists():
            raise ValidationError(message="Рецепт не находится в избранном")
