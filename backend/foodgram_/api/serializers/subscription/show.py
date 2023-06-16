from rest_framework import serializers

from models_app.models import Subscription


class SubscriptionShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
