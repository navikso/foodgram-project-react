from rest_framework.authtoken.models import Token
from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import User


class TokenGetService(ServiceWithResult):
    email = forms.EmailField()
    password = forms.CharField()

    def process(self):
        self.result = self._token
        return self

    @property
    def _token(self):
        user = User.objects.get(email=self.cleaned_data["email"])
        user_pass = self.cleaned_data["password"]
        if user.check_password(user_pass) or user.password == user_pass:
            return Token.objects.get(user=user)
