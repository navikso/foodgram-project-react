from django import forms
from django.core.paginator import Paginator
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK


class SubscriptionListService(ServiceWithResult):
    URL = "http://127.0.0.1:8000/api/users/subscriptions"

    page = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    recipes_limit = forms.IntegerField(required=False)

    def process(self):
        self._subscriptions()
        return self

    def _subscription(self):
        recipes = Subscription.objects.filter()

        page = self.cleaned_data.get("page") or 1
        paginator = Paginator(
            recipes,
            self.cleaned_data.get("limit") or REST_FRAMEWORK["PAGE_SIZE"]
        )
        # recipes_limit =
        self.result = {
            "count": recipes.count(),
            "next": self.URL + f"?page={page + 1}" if paginator.get_page(page).has_next() else None,
            "previous": self.URL + f"?page={page - 1}" if paginator.get_page(page).has_previous() else None,
            "results": paginator.get_page(page).object_list,
        }
