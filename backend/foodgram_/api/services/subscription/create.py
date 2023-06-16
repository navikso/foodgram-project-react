from functools import lru_cache

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Subscription
from models_app.models import User


class SubscriptionCreateService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        subs = self._create
        self._add_authors(subs)
        self.result = self._user
        return self

    @property
    def _create(self):
        return Subscription.objects.get_or_create(
            user=self.cleaned_data["user"]
        )[0]

    def _add_authors(self, subs: Subscription):
        subs.authors.add(self._user)

    @property
    @lru_cache
    def _user(self):
        return User.objects.get(id=self.cleaned_data["id"])
