from django import forms
from rest_framework.authtoken.models import Token
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult
from models_app.models import User


class UserCreateService(ServiceWithResult):
    email = forms.EmailField(max_length=254, required=False)
    username = forms.CharField(max_length=150, required=False)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    password = forms.CharField(max_length=150, required=False)

    custom_validations = ["check_fields", ]

    def process(self):
        self.run_custom_validations()
        self.result = self._create
        self._create_token(self.result)
        return self

    @property
    def _create(self):
        return User.objects.create(
            email=self.cleaned_data["email"],
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self.cleaned_data["password"]
        )

    def _create_token(self, user):
        Token.objects.create(
            user=user
        )

    def check_fields(self):
        errors = {}
        for field, value in self.cleaned_data.items():
            if not value:
                errors[field] = "Обязательное поле."
        if errors:
            raise ValidationError(message=errors)
