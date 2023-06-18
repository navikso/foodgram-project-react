from django import forms
from django.core.paginator import Paginator
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Recipe


class RecipeListService(ServiceWithResult):
    URL = "http://127.0.0.1:8000/api/recipes/"

    page = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    is_favorited = forms.IntegerField(required=False)
    is_in_shopping_cart = forms.IntegerField(required=False)
    author = forms.IntegerField(required=False)
    tags = forms.CharField(required=False)

    def process(self):
        self._recipes()
        return self

    def _recipes(self):
        author = self.cleaned_data.get("author")
        tags = self.cleaned_data.get("tags")

        recipes = Recipe.objects.all()

        if author:
            recipes = recipes.filter(user_id=author)

        if tags:
            recipes = recipes.filter(tags__name__in=tags.split(","))

        page = self.cleaned_data.get("page") or 1
        paginator = Paginator(
            recipes,
            self.cleaned_data.get("limit") or REST_FRAMEWORK["PAGE_SIZE"]
        )
        self.result = {
            "count": recipes.count(),
            "next":
                self.URL +
                + f"?page={page + 1}" if paginator.get_page(page).has_next()
                else None,
            "previous":
                self.URL +
                + f"?page={page - 1}"
                if paginator.get_page(page).has_previous()
                else None,
            "results": paginator.get_page(page).object_list,
        }
