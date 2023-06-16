from django.contrib import admin

from models_app.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", )
    filter_horizontal = ["authors", ]
