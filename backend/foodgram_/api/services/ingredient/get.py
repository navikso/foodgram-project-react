from django import forms
from service_objects.services import ServiceWithResult
from models_app.models import Ingredient


class IngredientGetService(ServiceWithResult):
    id = forms.IntegerField()

    def process(self):
        self.result = self._ingredient
        return self

    @property
    def _ingredient(self):
        return Ingredient.objects.get(id=self.cleaned_data["id"])


