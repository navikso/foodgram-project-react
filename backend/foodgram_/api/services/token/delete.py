from django import forms
from rest_framework.authtoken.models import Token
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User


class TokenDeleteService(ServiceWithResult):
    user = ModelField(User)

    def process(self):
        self._delete()
        return self

    def _delete(self):
        Token.objects.get(user=self.cleaned_data["user"]).delete()
