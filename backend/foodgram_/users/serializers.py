from rest_framework import serializers

from models_app.models import (
    Subscription, User
)


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        if self.context.get("user"):
            return bool(Subscription.objects.get_or_create(
                user=self.context["user"]
            )[0].authors.filter(id=obj.id))
        return False
