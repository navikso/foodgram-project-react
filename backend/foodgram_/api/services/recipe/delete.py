from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.errors import NotFound, ForbiddenError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import Recipe
from models_app.models import User


class RecipeDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ["presence_recipe", "access_user"]

    def process(self):
        self.run_custom_validations()
        self._delete()
        return self

    def _delete(self):
        return self._recipe.delete()

    @property
    def _recipe(self):
        try:
            return Recipe.objects.get(id=self.cleaned_data["id"])
        except ObjectDoesNotExist:
            return None

    def presence_recipe(self):
        if not self._recipe:
            raise NotFound(message="Страница не найдена.")

    def access_user(self):
        if self.cleaned_data["user"] != self._recipe.user:
            raise ForbiddenError(message="У вас недостаточно прав для выполнения данного действия.")
