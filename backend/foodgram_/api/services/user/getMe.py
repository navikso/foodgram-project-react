from service_objects.errors import ForbiddenError
from service_objects.services import ServiceWithResult
from models_app.models import User


class UserGetMeService(ServiceWithResult):

    def process(self):
        self.result = self._user_me
        return self

    @property
    def _user_me(self):
        if self.cleaned_data["id"] != self.user.id:
            raise ForbiddenError(
                message=(
                    "У вас недостаточно прав для выполнения данного действия."
                )
            )
        return User.objects.get(id=self.cleaned_data["id"])
