from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from models_app.models import Tag


class TagGetService(ServiceWithResult):
    id = forms.IntegerField()

    custom_validations = ["tag_presence"]

    def process(self):
        self.run_custom_validations()
        self.result = self._tag
        return self

    @property
    @lru_cache
    def _tag(self):
        try:
            return Tag.objects.get(id=self.cleaned_data["id"])
        except Exception:
            return None

    def tag_presence(self):
        if not self._tag:
            raise NotFound(message="Страница не найдена.", response_status=status.HTTP_404_NOT_FOUND)
