from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError

from models_app.models import User


class UserSetPasswordService(ServiceWithResult):
    new_password = forms.CharField(required=False)
    current_password = forms.CharField(required=False)
    user = ModelField(User)

    custom_validations = ["check_fields", "_check_password"]

    def process(self):
        self.run_custom_validations()
        self._set_password()
        return self

    def _check_password(self):
        curent_user = self.cleaned_data["user"]
        old_pass = self.cleaned_data["current_password"]
        if not curent_user.check_password(old_pass) \
                and curent_user.password != old_pass:
            raise ValidationError(message="Текущий пароль не верный")

    def _set_password(self):
        self.cleaned_data["user"].set_password(
            self.cleaned_data["new_password"]
        )
        self.cleaned_data["user"].save()

    def check_fields(self):
        for field, value in self.cleaned_data.items():
            if not value:
                raise ValidationError(message=f"{field} - Обязательное поле.")