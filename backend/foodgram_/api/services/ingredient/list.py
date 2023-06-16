from django import forms
from service_objects.services import ServiceWithResult
from models_app.models import Ingredient


class IngredientListService(ServiceWithResult):
    name = forms.CharField(required=False)

    def process(self):
        self.result = self._ingredients
        return self

    @property
    def _ingredients(self):
        return Ingredient.objects.filter(name__startswith=self.cleaned_data["name"])
