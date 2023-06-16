from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from models_app.models import User


class UserGetService(ServiceWithResult):
    id = forms.IntegerField()

    custom_validations = ["user_presence"]

    def process(self):
        self.run_custom_validations()
        self.result = self._user
        return self

    @property
    @lru_cache
    def _user(self):
        try:
            return User.objects.get(id=self.cleaned_data["id"])
        except ObjectDoesNotExist:
            return None

    def user_presence(self):
        if not self._user:
            raise NotFound(message="Пользователь не найден.", response_status=status.HTTP_404_NOT_FOUND)
