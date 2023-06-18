from django import forms
from django.core.paginator import Paginator
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import User


class UserListService(ServiceWithResult):
    URL = "http://127.0.0.1:8000/api/users/"

    page = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)

    def process(self):
        self._users()
        return self

    def _users(self):

        users = User.objects.all()

        page = self.cleaned_data.get("page") or 1
        paginator = Paginator(
            users,
            self.cleaned_data.get("limit") or REST_FRAMEWORK["PAGE_SIZE"]
        )
        self.result = {
            "count": users.count(),
            "next": 
                self.URL + f"?page={page + 1}"
                if paginator.get_page(page).has_next()
                else None,
            "previous":
                self.URL + f"?page={page - 1}"
                if paginator.get_page(page).has_previous()
                else None,
            "results": paginator.get_page(page).object_list,
        }
