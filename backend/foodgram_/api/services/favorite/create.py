from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Favorites
from models_app.models import User
from models_app.models import Recipe


class FavoriteCreateService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ["recipe_presence"]

    def process(self):
        self.run_custom_validations()
        self._create()
        self.result = self._recipe
        return self

    def _create(self):
        return Favorites.objects.create(
            recipe=self._recipe,
            user=self.cleaned_data["user"]
        )

    @property
    def _recipe(self):
        return Recipe.objects.get(
            id=self.cleaned_data['id']
        )

    def recipe_presence(self):
        if not Recipe.objects.filter(id=self.cleaned_data["id"]).exists():
            raise ValidationError(message="Такого рецепта не существует")
        if Favorites.objects.filter(recipe_id=self.cleaned_data["id"]).exists():
            raise ValidationError(message="Рецепт уже находится в избранном")
