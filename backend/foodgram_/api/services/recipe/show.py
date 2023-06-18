from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from models_app.models import Recipe


class RecipeGetService(ServiceWithResult):
    id = forms.IntegerField()

    custom_validations = ["recipe_presence"]

    def process(self):
        self.run_custom_validations()
        self.result = self._recipe
        return self

    @property
    @lru_cache
    def _recipe(self):
        try:
            return Recipe.objects.get(id=self.cleaned_data["id"])
        except Exception:
            return None

    def recipe_presence(self):
        if not self._recipe:
            raise NotFound(
                message="Страница не найдена.",
                response_status=status.HTTP_404_NOT_FOUND
            )
